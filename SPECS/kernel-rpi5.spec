%{!?kernel_commit:%global kernel_commit b0b7d2006113562307ade2f6a075b03f3a781346}
%{!?kernel_version:%global kernel_version 6.18.64}

Name:           kernel-rpi5
Version:        %{kernel_version}
Release:        1%{?dist}
%global kernelrelease %{version}-rpi5
Summary:        Raspberry Pi 5 Linux kernel
License:        GPL-2.0-only AND GPL-2.0-or-later AND GPL-1.0-or-later AND MIT AND BSD-2-Clause AND BSD-3-Clause AND ISC AND X11
URL:            https://github.com/raspberrypi/linux
Source0:        https://github.com/raspberrypi/linux/archive/%{kernel_commit}.tar.gz
ExclusiveArch:  aarch64
BuildRequires:  bc
BuildRequires:  bison
BuildRequires:  dwarves
BuildRequires:  elfutils-libelf-devel
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  kmod
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  perl
BuildRequires:  python3

Provides:       installonlypkg(kernel)
Provides:       kernel-uname-r = %{kernelrelease}

%description
The Raspberry Pi downstream Linux kernel built with the Pi 5 device-tree
configuration for Fedora aarch64 systems.

%prep
%setup -q -n linux-%{kernel_commit}

%build
make ARCH=arm64 %{?_smp_mflags} bcm2712_defconfig
scripts/config --disable ARM64_16K_PAGES \
    --enable ARM64_4K_PAGES \
    --enable SECURITY \
    --enable AUDIT \
    --enable SECURITYFS \
    --enable SECURITY_NETWORK \
    --enable SECURITY_PATH \
    --enable SECURITY_SELINUX \
    --enable SECCOMP \
    --set-str LOCALVERSION -rpi5 \
    --disable LOCALVERSION_AUTO
make ARCH=arm64 olddefconfig
grep -qx 'CONFIG_ARM64_4K_PAGES=y' .config
grep -qx 'CONFIG_LOCALVERSION="-rpi5"' .config
for option in \
    ARCH_BCM ARCH_BCM2835 ARCH_BRCMSTB PCI PCIE_BRCMSTB MFD_RP1 \
    PINCTRL_BCM2712 PINCTRL_RP1 COMMON_CLK_RP1 BCMGENET MMC_BCM2835 \
    MMC_BCM2835_MMC MMC_SDHCI_IPROC USB_XHCI_HCD USB_DWC2 USB_STORAGE \
    EXT4_FS RASPBERRYPI_FIRMWARE ARM_RASPBERRYPI_CPUFREQ BCM2711_THERMAL \
    BCM2835_THERMAL SERIAL_8250_BCM2835AUX SERIAL_AMBA_PL011 \
    BRCMFMAC_SDIO BT_HCIUART_BCM SECURITY AUDIT SECURITYFS SECURITY_NETWORK \
    SECURITY_PATH SECURITY_SELINUX SECCOMP NAMESPACES USER_NS CGROUPS \
    CGROUP_BPF DEVTMPFS DEVTMPFS_MOUNT; do
    if ! grep -qx "CONFIG_${option}=y" .config; then
        echo "Required built-in Raspberry Pi 5 option is disabled: CONFIG_${option}" >&2
        exit 1
    fi
done
for option in \
    FIRMWARE_RP1 RP1_PIO BRCMFMAC I2C_BCM2835 SPI_BCM2835 \
    SPI_BCM2835AUX SERIAL_RP1_PIO_UART BT_HCIUART DRM_V3D DRM_VC4 \
    VIDEO_RP1_CFE_DOWNSTREAM SND_RP1_AUDIO_OUT OVERLAY_FS SQUASHFS DM_VERITY; do
    if ! grep -Eq "^CONFIG_${option}=[ym]$" .config; then
        echo "Required Raspberry Pi 5 module is disabled: CONFIG_${option}" >&2
        exit 1
    fi
done
make ARCH=arm64 %{?_smp_mflags} Image modules dtbs
test "$(make -s ARCH=arm64 kernelrelease)" = "%{kernelrelease}"

%install
install -D -m 0755 arch/arm64/boot/Image \
    %{buildroot}/boot/vmlinuz-%{kernelrelease}
install -D -m 0644 .config \
    %{buildroot}%{_prefix}/lib/modules/%{kernelrelease}/config
install -D -m 0644 System.map \
    %{buildroot}%{_prefix}/lib/modules/%{kernelrelease}/System.map
make ARCH=arm64 modules_install \
    INSTALL_MOD_PATH=%{buildroot}%{_prefix} \
    INSTALL_MOD_STRIP=1
rm -f %{buildroot}%{_prefix}/lib/modules/%{kernelrelease}/build \
      %{buildroot}%{_prefix}/lib/modules/%{kernelrelease}/source
make ARCH=arm64 dtbs_install \
    INSTALL_DTBS_PATH=%{buildroot}%{_prefix}/lib/firmware/raspberrypi-kernel/%{kernelrelease}
depmod -b %{buildroot}%{_prefix} %{kernelrelease}

%files
/boot/vmlinuz-%{kernelrelease}
%{_prefix}/lib/modules/%{kernelrelease}/
%{_prefix}/lib/firmware/raspberrypi-kernel/%{kernelrelease}/
