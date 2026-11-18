# Fedora Raspberry Pi 5 kernel RPM

This project builds the Raspberry Pi downstream kernel for the Raspberry Pi 5
as an RPM on Fedora. The spec follows Fedora kernel RPM conventions for kernel
release naming, module placement, and install-only package handling, but is a
small, Pi-specific spec; Fedora's full `kernel.spec` builds Fedora's different
kernel source and configuration and cannot be used unchanged.

The local build defaults to commit
[`b0b7d2006113562307ade2f6a075b03f3a781346`](https://github.com/raspberrypi/linux/commit/b0b7d2006113562307ade2f6a075b03f3a781346)
on Raspberry Pi's `rpi-6.18.y` branch. The Pi 5 defconfig is used, with 4 KiB
pages selected to match Fedora aarch64 userspace (the upstream Pi 5 defconfig
defaults to 16 KiB pages).

## Pi 5 driver coverage

Fedora's `kernel-aarch64-fedora.config` is a generic ARM64 config, not a Pi 5
config. In particular, it does not enable the Pi 5 RP1 MFD and firmware/PIO
stack. This RPM builds from Raspberry Pi's `bcm2712_defconfig` instead, which
includes the RP1, BCM2712 pin control, PCIe, Ethernet, SD, USB, Wi-Fi/Bluetooth,
and graphics/camera/audio driver selections. The kernel spec checks that the
essential built-in drivers, required modules, and Fedora Atomic security and
filesystem features remain enabled after `olddefconfig`; the build fails if
any of these options disappear or become disabled. This check is applied to
both supported kernel branches.

The Wi-Fi and Bluetooth drivers also need firmware blobs from Fedora's
`linux-firmware` package; those blobs are not part of this kernel RPM. Ensure
that package is present in the target Fedora or Atomic image.

## GitHub Actions and kernel branches

The workflow in [`.github/workflows/build-kernel-rpm.yml`](.github/workflows/build-kernel-rpm.yml)
builds `rpi-6.18.y` and `rpi-7.2.y` on native ARM64 GitHub-hosted runners in a
Fedora 45 container. It runs for pushes to `main`, pull requests, weekly, or
manually. Each run resolves the selected upstream branch to a commit and
uploads the RPM and source RPM as downloadable workflow artifacts. The
`rpi-7.2.y` branch currently reports kernel version 7.2.15.

The local spec defaults remain pinned; the workflow passes each branch's
resolved commit and version as RPM macros, so builds are reproducible for the
specific commit logged in the Actions run.

To locally build the currently resolved `rpi-7.2.y` revision, pass its commit
and kernel version to the same script:

```bash
KERNEL_COMMIT=69c2961f233d2a8e92c0a3cc068f4f5f88425e5f \
KERNEL_VERSION=7.2.15 ./scripts/build-rpm.sh
```

## Build

Build natively on an aarch64 Fedora machine (a Raspberry Pi 5 is suitable).
Install the build tools and dependencies:

```bash
sudo dnf install rpm-build gcc make bc bison flex openssl-devel \
  elfutils-libelf-devel dwarves perl python3 kmod curl
```

Then run:

```bash
./scripts/build-rpm.sh
```

The source archive is downloaded for the pinned commit. The resulting RPM is
written under `rpmbuild/RPMS/aarch64/`; the source RPM is under
`rpmbuild/SRPMS/`.

For local builds, the default source pin and version can be changed through the
`kernel_commit` and `kernel_version` defaults in
[`SPECS/kernel-rpi5.spec`](SPECS/kernel-rpi5.spec). The Actions workflow resolves
the branch tip and supplies those macros automatically.

## Installation and boot

On a regular Fedora aarch64 installation, install the RPM with `dnf`. It
installs the kernel image, modules, and device trees, but does not replace
Fedora's kernel or change Raspberry Pi firmware boot settings. Keep the
existing kernel as a fallback:

```bash
sudo dnf install ./rpmbuild/RPMS/aarch64/kernel-rpi5-*.rpm
```

Configure the device's boot chain to use `/boot/vmlinuz-<kernel-release>` and
the packaged device trees before rebooting.

An RPM being accepted by `rpm-ostree` does **not** by itself make its kernel
active on Fedora Atomic Desktop or Fedora IoT. Atomic deployments manage
bootable kernel artifacts as part of the OS deployment; layering this RPM onto
an already installed system does not configure Raspberry Pi firmware or make
the new kernel the deployment kernel. For Atomic, include the RPM and its
matching boot assets in the OS image build/compose, and test deployment and
rollback on the target Raspberry Pi 5. Do not remove the working kernel until
the new image has booted successfully.

The RPM is unsigned. Secure Boot systems require signing the kernel and any
modules with keys trusted by the target before deployment.
