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
[`b005af6699cc67413be78028a201e87fe40dcb50`](https://github.com/raspberrypi/linux/commit/b005af6699cc67413be78028a201e87fe40dcb50)
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
`kernel-modules`; `modules-core` owns `modules.order` and declares the
Fedora-style depmod-generated metadata files. Unlike Fedora's full kernel
build, this focused spec does not classify modules into Fedora's core,
standard, and extra tiers: all loadable modules are in `kernel-modules`, and
`kernel-modules-extra` is an empty compatibility package. Matching package
names alone does not guarantee RPM-OSTree compatibility; validate the exact
replacement transaction and boot on the target before relying on it.

The Wi-Fi and Bluetooth drivers also need firmware blobs from Fedora's
`linux-firmware` package; those blobs are not part of this kernel RPM. Ensure
that package is present in the target Fedora or Atomic image.

## GitHub Actions and kernel branches

The workflow in [`.github/workflows/build-kernel-rpm.yml`](.github/workflows/build-kernel-rpm.yml)
builds `rpi-6.18.y`, `rpi-7.2.y`, and `rpi-7.3.y` on native ARM64
GitHub-hosted runners in a Fedora 45 container. It runs for pushes to `main`,
pull requests, weekly, or manually. Each run resolves the selected upstream
branch to a commit and uploads the RPMs, including generated debuginfo and
debugsource packages, and source RPM as downloadable workflow artifacts. The
`rpi-7.3.y` branch currently reports kernel version 7.3.5.

The local spec defaults remain pinned; the workflow passes each branch's
resolved commit and version as RPM macros, so builds are reproducible for the
specific commit logged in the Actions run.

To locally build the currently resolved `rpi-7.3.y` revision, pass its commit
and kernel version to the same script:

```bash
KERNEL_COMMIT=b005af6699cc67413be78028a201e87fe40dcb50 \
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
