# Fedora Raspberry Pi 5 kernel RPM

This project builds the Raspberry Pi downstream kernel for the Raspberry Pi 5
as Fedora-style RPMs. It uses Fedora's aarch64 configuration as its base and
adds Raspberry Pi settings from `bcm2712_defconfig`. The runtime package names,
kernel release naming, module paths, dependencies, and kernel-install hooks
follow Fedora's kernel package layout so the packages can replace Fedora's
kernel packages with RPM-OSTree. This remains a focused spec, not a copy of
Fedora's full `kernel.spec`; it does not build a `kernel-devel` package or
sign the kernel and modules.

The kernel release uses Fedora's version-release-architecture format with an
`rpi5` release tag, keeping its module and boot paths distinct from the stock
Fedora kernel. The local build defaults to commit
[`1ef812a522e2a929f7a9a00f7e2ca0cff21086c7`](https://github.com/raspberrypi/linux/commit/1ef812a522e2a929f7a9a00f7e2ca0cff21086c7)
on Raspberry Pi's `rpi-7.3.y` branch (kernel version 7.3.5). The base
configuration is Fedora's `kernel-aarch64-fedora.config`, pinned to Fedora
kernel packaging commit
[`3393e4e0db8129398c14fed17e09abdd0d1d9822`](https://src.fedoraproject.org/rpms/kernel/c/3393e4e0db8129398c14fed17e09abdd0d1d9822).
The Pi-specific fragment is derived from the matching `bcm2712_defconfig`.
The 4 KiB page size is retained for Fedora aarch64 compatibility; the Pi
defconfig defaults to 16 KiB pages.

## Pi 5 driver coverage

Fedora's aarch64 config does not enable the Pi 5 RP1 MFD and firmware/PIO
stack. The build keeps Fedora's config as the base, then merges only the
Pi-related settings that differ in the Raspberry Pi `bcm2712_defconfig`.
The spec checks that essential Pi drivers, required modules, and Fedora
security/filesystem options remain enabled after `olddefconfig`; it fails if
these settings cannot be satisfied by a kernel branch.

The build produces Fedora-named `kernel`, `kernel-core`, `kernel-modules-core`,
`kernel-modules`, and `kernel-modules-extra` RPMs. Loadable modules are in
`kernel-modules`; their debug symbols are in `kernel-modules-debuginfo`.
`modules-core` owns `modules.order` and declares the Fedora-style
depmod-generated metadata files. Unlike Fedora's full kernel build, this
focused spec does not classify modules into Fedora's core, standard, and extra
tiers: all loadable modules are in `kernel-modules`, and
`kernel-modules-extra` is an empty compatibility package. Matching package
names alone does not guarantee RPM-OSTree compatibility; validate the exact
replacement transaction and boot on the target before relying on it.

The Wi-Fi and Bluetooth drivers also need firmware blobs from Fedora's
`linux-firmware` package; those blobs are not part of this kernel RPM. Ensure
that package is present in the target Fedora or Atomic image.

## Raspberry Pi firmware device tree

The kernel RPM configures U-Boot to use the Raspberry Pi firmware-provided
device tree so firmware overlays in `/boot/efi/config.txt` are passed to Linux.
After `kernel-install` creates the current-kernel `/boot/dtb` symlink, the RPM
removes that symlink and sets `FirmwareDT=True` in `/etc/u-boot.conf`. The
versioned DTBs remain packaged under `/usr/lib/modules/<kernelrelease>/dtb`.
Kernel updates repeat this setup because `kernel-install` may recreate the
symlink.

## Plasma Bigscreen slimline variant

The opt-in `bigscreen` flavor builds only against the `rpi-7.3.y` kernel line
and is intended for a Raspberry Pi 5 Plasma Bigscreen image. It is built in CI
alongside the standard 6.18 and 7.3 packages, without changing either standard
configuration. It uses Fedora's `kernel`, `kernel-core`, and module package
names so users can choose it as a replacement for the default kernel. Its
distinct `rpi5bs` release tag lets it coexist with the standard kernel when
desired.

The Bigscreen config retains Fedora's security and filesystem baseline,
Raspberry Pi HDMI/V3D graphics, general HDMI/RP1 audio, onboard Broadcom SDIO
Wi-Fi, Bluetooth, USB, Ethernet, Pi video playback/camera support, TV/radio
capture, and Pi add-ons including audio, PoE, and Sense HAT support. It drops
unrelated Wi-Fi vendors, non-Pi PCIe host controllers, discrete/virtual GPU
drivers, Ceph, hardware RAID/SAS/Fibre Channel and legacy SCSI adapters, and
non-Pi SoC platforms. The Pi PCIe host, PCIe core, generic SCSI, USB storage,
SD, NVMe, and software RAID remain available.

To build the current pinned 7.3.y Bigscreen flavor locally on an aarch64 Fedora
host:

```bash
KERNEL_FLAVOR=bigscreen \
KERNEL_COMMIT=1ef812a522e2a929f7a9a00f7e2ca0cff21086c7 \
KERNEL_VERSION=7.3.5 ./scripts/build-rpm.sh
```

The GitHub build workflow also builds this flavor from the live `rpi-7.3.y`
branch and uploads it as a separate artifact.

## Further kernel config slimming review

The current build starts with Fedora's broad aarch64 config and merges the
Pi-specific fragment; it is not a Pi-only config. At the current config
revision, the Fedora base has 7,829 enabled settings and the Pi fragment has
83. These counts include non-driver settings and are informational, not a
measure of the number of compiled drivers. Kconfig dependency resolution can
also change the final `.config`. This describes the standard flavor; the
Bigscreen flavor applies additional targeted exclusions in
`SOURCES/kernel-rpi5-bigscreen.config`.

Further reductions should focus on unsupported hardware inherited from
Fedora's broad aarch64 base. The Bigscreen flavor excludes non-Pi SoC
platforms, Ceph, and non-Pi storage-controller drivers while retaining Pi
add-ons, TV/radio capture, and generic storage support. Review unrelated
media drivers such as `VIDEO_CX18`, `VIDEO_CX88`, `VIDEO_EM28XX`,
`VIDEO_IVTV`, and `VIDEO_PVRUSB2` only if they are not needed by the target.

The build already disables `DRM_XE` because its display code failed to compile
on the older `rpi-7.2.y` branch. The current Cirrus audio configuration also
enables `MFD_ARIZONA_I2C` and `MFD_WM5102` to satisfy the `RPI_CIRRUS` sound-card
dependencies; if that card is removed, review those settings and their
assertions in the spec together. Any future pruning should preserve the
required Pi options checked by the spec and be validated across both supported
kernel branches before removing drivers from the shipped RPMs.

## Generating a kernel config reference

The script [`scripts/document-kernel-config.py`](scripts/document-kernel-config.py)
generates Markdown containing the options in one or more kernel config files,
their source values, Kconfig prompts, and Kconfig help text. The references in
`docs/` cover the standard config files and final `.config`. Run it against the
matching kernel source tree so symbols are documented from the exact kernel
revision. To document the Bigscreen fragment as well, run:

```bash
kernel_source=rpmbuild/BUILD/linux-1ef812a522e2a929f7a9a00f7e2ca0cff21086c7
python3 scripts/document-kernel-config.py \
  SOURCES/kernel-aarch64-fedora.config \
  --kernel-source "${kernel_source}" \
  --output docs/kernel-aarch64-fedora-config.md
python3 scripts/document-kernel-config.py \
  SOURCES/kernel-rpi5.config \
  --kernel-source "${kernel_source}" \
  --output docs/kernel-rpi5-config.md
python3 scripts/document-kernel-config.py \
  SOURCES/kernel-rpi5-bigscreen.config \
  --kernel-source "${kernel_source}" \
  --output docs/kernel-rpi5-bigscreen-config.md
python3 scripts/document-kernel-config.py \
  "${kernel_source}/.config" \
  --kernel-source "${kernel_source}" \
  --output docs/kernel-config-reference.md
```

Replace the example commit with the matching source directory under
`rpmbuild/BUILD/`. For options listed in multiple input files, the report shows
the value from each file. Options without Kconfig help are identified as such;
options missing from the supplied source tree are marked as undefined.
Regenerate all three references when the kernel pin or config files change.
The script uses only Python's standard library.

## GitHub Actions and kernel branches

The [packaging validation workflow](.github/workflows/validate-kernel-packaging.yml)
runs on pushes to `main` and pull requests. It checks shell syntax and validates
the kernel pin manifest against the RPM spec defaults without compiling the
kernel. The [build workflow](.github/workflows/build-kernel-rpm.yml) can be
manually dispatched to build the latest upstream branches and upload RPM
artifacts for testing. Release builds run in the
[release workflow](.github/workflows/release-kernel-rpm.yml), after a kernel-pin
sync pull request is merged or when that workflow is manually dispatched.

The [sync workflow](.github/workflows/sync-kernel-pin.yml) checks
`rpi-6.18.y` and `rpi-7.3.y` weekly and opens or updates a pull
request with each upstream commit and kernel version read from that commit's
`Makefile`. The branch pins are recorded in
[`SOURCES/kernel-branch-pins.json`](SOURCES/kernel-branch-pins.json), with the
`rpi-7.3.y` pin also used as the local spec default. Merging a sync pull request
runs the [release workflow](.github/workflows/release-kernel-rpm.yml), which
builds RPMs and an SRPM and publishes a separate GitHub Release for each new
pin and flavor. Both branches publish the standard flavor; 7.3.y also publishes
the Bigscreen flavor. Release tags include the branch, flavor (for Bigscreen),
actual kernel version, and commit prefix (for example,
`kernel-7.3.y-bigscreen-7.3.5-1ef812a522e2`), so updates are tracked even when
the upstream kernel version has not changed. The release workflow can also be
manually dispatched to publish any pins and flavors that do not already have
releases.

COPR builds are triggered after the GitHub release is published; no COPR API
token is needed in GitHub Actions. In the `dsedg/kernel-rpi5` COPR project,
configure two SCM packages using the repository URL
`https://github.com/dsedg/fedora-rpi5.git`, branch `main`, and the `make srpm`
source method:

| COPR package | Spec File |
| --- | --- |
| `kernel-rpi5-6.18` | `.copr/kernel-rpi5-6.18.spec` |
| `kernel-rpi5-7.3` | `.copr/kernel-rpi5-7.3.spec` |
| `kernel-rpi5-7.3-bigscreen` | `.copr/kernel-rpi5-7.3-bigscreen.spec` |

Enable auto-rebuild for all three packages and configure the project's
`fedora-44-aarch64`, `fedora-45-aarch64`, and `fedora-rawhide-aarch64`
chroots. The selector spec files identify the branch; the make target reads
the matching pin from `SOURCES/kernel-branch-pins.json` and generates an SRPM
from the shared kernel spec. COPR builds `rpi-6.18.y` with the standard flavor,
`rpi-7.3.y` with the standard config, and `rpi-7.3.y` with the Bigscreen
slimline config. The release workflow triggers each matching COPR build once.
In the COPR project settings, open
**Integrations** and use the ID and UUID from the project's webhook URL to
construct a custom webhook URL for each package:

```text
https://copr.fedorainfracloud.org/webhooks/custom/<ID>/<UUID>/kernel-rpi5-6.18/
https://copr.fedorainfracloud.org/webhooks/custom/<ID>/<UUID>/kernel-rpi5-7.3/
https://copr.fedorainfracloud.org/webhooks/custom/<ID>/<UUID>/kernel-rpi5-7.3-bigscreen/
```

Save these as the repository Actions secrets
`COPR_WEBHOOK_KERNEL_RPI5_618`, `COPR_WEBHOOK_KERNEL_RPI5_73`, and
`COPR_WEBHOOK_KERNEL_RPI5_73_BIGSCREEN`, respectively.
The release workflow POSTs to the matching package webhook only after its
GitHub Release has been created successfully. Remove any existing COPR GitHub
push webhook from the repository; push-triggered builds would start before the
GitHub release and duplicate the post-release trigger.
Remove any obsolete SCM package named `kernel` and keep the three
`kernel-rpi5-6.18`, `kernel-rpi5-7.3`, and
`kernel-rpi5-7.3-bigscreen` SCM entries. Do not configure a project-wide
GitHub push webhook.
COPR still builds from the configured repository; it does not use the SRPM
produced by the GitHub release workflow. See COPR's
[SCM and webhook documentation](https://docs.copr.fedorainfracloud.org/user_documentation.html#webhooks).

To locally build the currently resolved `rpi-7.3.y` revision, pass its commit
and kernel version to the same script:

```bash
KERNEL_COMMIT=1ef812a522e2a929f7a9a00f7e2ca0cff21086c7 \
KERNEL_VERSION=7.3.5 ./scripts/build-rpm.sh
```

## Build

Build natively on an aarch64 Fedora machine (a Raspberry Pi 5 is suitable).
Install the build tools and dependencies:

```bash
sudo dnf install rpm-build gcc make bc bison flex openssl-devel \
  openssl elfutils-libelf-devel dwarves perl python3 kmod curl
```

Then run:

```bash
./scripts/build-rpm.sh
```

The source archive is downloaded for the pinned commit. The resulting binary
RPMs are written under `rpmbuild/RPMS/aarch64/`; the source RPM is under
`rpmbuild/SRPMS/`.

For local builds, the default source pin and version can be changed through the
`kernel_commit` and `kernel_version` defaults in
[`SPECS/kernel-rpi5.spec`](SPECS/kernel-rpi5.spec). The Actions workflow resolves
the branch tip and supplies those macros automatically.

## Installation and boot

On a regular Fedora aarch64 installation, install the kernel meta-package and
its matching subpackages with `dnf`. Keep the existing kernel as a fallback:

```bash
sudo dnf install \
  ./rpmbuild/RPMS/aarch64/kernel-7.3.5-*.rpm \
  ./rpmbuild/RPMS/aarch64/kernel-core-7.3.5-*.rpm \
  ./rpmbuild/RPMS/aarch64/kernel-modules-core-7.3.5-*.rpm \
  ./rpmbuild/RPMS/aarch64/kernel-modules-7.3.5-*.rpm \
  ./rpmbuild/RPMS/aarch64/kernel-modules-extra-7.3.5-*.rpm
```

Configure the device's boot chain to use `/boot/vmlinuz-<kernel-release>` and
the packaged device trees before rebooting.

The package names and kernel-core/module layout are intended for an
RPM-OSTree override of Fedora's matching kernel packages. Verify the exact set
of installed kernel RPMs before replacing them, then test the resulting
deployment and rollback on a Raspberry Pi 5. The override does not configure
Raspberry Pi firmware boot settings; configure the boot chain to use the
deployed kernel and device trees, and retain a working fallback until the new
kernel has booted successfully.

The RPM is unsigned. Secure Boot systems require signing the kernel and any
modules with keys trusted by the target before deployment.
