%{!?kernel_commit:%global kernel_commit b005af6699cc67413be78028a201e87fe40dcb50}
%{!?kernel_version:%global kernel_version 7.3.5}

Name:           kernel
Version:        %{kernel_version}
Release:        300.rpi5%{?dist}
%global kernelrelease %{version}-%{release}.%{_target_cpu}
Summary:        Linux kernel for Raspberry Pi 5
License:        GPL-2.0-only AND GPL-2.0-or-later AND GPL-1.0-or-later AND MIT AND BSD-2-Clause AND BSD-3-Clause AND ISC AND X11
URL:            https://github.com/raspberrypi/linux
Source0:        https://github.com/raspberrypi/linux/archive/%{kernel_commit}.tar.gz
# Fedora f45 kernel-aarch64-fedora.config at commit 3393e4e0db8129398c14fed17e09abdd0d1d9822.
Source1:        kernel-aarch64-fedora.config
Source2:        kernel-rpi5.config
Source3:        kernel-rpi5-host-uapi-types.h
ExclusiveArch:  aarch64
BuildRequires:  bc
BuildRequires:  bison
BuildRequires:  dwarves
BuildRequires:  elfutils-libelf-devel
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  kmod
BuildRequires:  make
BuildRequires:  openssl
BuildRequires:  openssl-devel
BuildRequires:  perl
BuildRequires:  python3
BuildRequires:  xz

Provides:       installonlypkg(kernel)
Requires:       kernel-core-uname-r = %{kernelrelease}
Requires:       kernel-modules-core-uname-r = %{kernelrelease}
Requires:       kernel-modules-uname-r = %{kernelrelease}
Requires:       kernel-modules-extra-uname-r = %{kernelrelease}

%description
The kernel meta-package for the Raspberry Pi 5.

%package core
Summary:        Core kernel for Raspberry Pi 5
Provides:       installonlypkg(kernel)
Provides:       kernel-uname-r = %{kernelrelease}
Provides:       kernel-core-uname-r = %{kernelrelease}
Requires:       kernel-modules-core-uname-r = %{kernelrelease}
Requires(pre):  coreutils
Requires(pre):  systemd >= 203-2
Requires(pre):  /usr/bin/kernel-install
Requires(pre):  dracut >= 027
Requires(preun): systemd >= 200
AutoReq:        no
AutoProv:       yes

%description core
The kernel image, device trees, and configuration files for Raspberry Pi 5.

%package modules-core
Summary:        Core modules metadata for Raspberry Pi 5 kernel
Provides:       installonlypkg(kernel-module)
Provides:       kernel-modules-core-uname-r = %{kernelrelease}
Requires:       kernel-uname-r = %{kernelrelease}
AutoReq:        no
AutoProv:       yes

%description modules-core
Core module metadata required by the Raspberry Pi 5 kernel.

%package modules
Summary:        Kernel modules for Raspberry Pi 5
Provides:       installonlypkg(kernel-module)
Provides:       kernel-modules-uname-r = %{kernelrelease}
Requires:       kernel-uname-r = %{kernelrelease}
Requires:       kernel-modules-core-uname-r = %{kernelrelease}
AutoReq:        no
AutoProv:       yes

%description modules
The loadable kernel modules for Raspberry Pi 5.

%package modules-extra
Summary:        Additional kernel modules for Raspberry Pi 5
Provides:       installonlypkg(kernel-module)
Provides:       kernel-modules-extra-uname-r = %{kernelrelease}
Requires:       kernel-uname-r = %{kernelrelease}
Requires:       kernel-modules-core-uname-r = %{kernelrelease}
AutoReq:        no
AutoProv:       yes

%description modules-extra
Compatibility package for the Fedora kernel module package layout.

# RPM extracts module debug info before compressing the installed modules.
%define __rpi5_compress_modules \
  find "$RPM_BUILD_ROOT%{_prefix}/lib/modules/%{kernelrelease}" -type f -name '*.ko' -print0 | \
    xargs -0 -r xz --compress --check=crc32 --lzma2=dict=1MiB -f \
%{nil}
%define __spec_install_post \
  %{?__debug_package:%{__debug_install_post}}\
  %{__arch_install_post}\
  %{__os_install_post}\
  %{__rpi5_compress_modules}\
%{nil}

%prep
%setup -q -n linux-%{kernel_commit}
cp %{SOURCE1} fedora-aarch64.config
cp %{SOURCE2} kernel-rpi5.config
cp %{SOURCE3} scripts/include/kernel-rpi5-host-uapi-types.h
sed -i 's/uint8_t/__u8/g' include/uapi/linux/media/raspberrypi/pisp_be_config.h
sed -i \
    -e 's/uint8_t/__u8/g' \
    -e 's/uint16_t/__u16/g' \
    -e 's/uint32_t/__u32/g' \
    -e '/#include <linux\/ioctl.h>/a #include <linux/types.h>' \
    include/uapi/misc/rp1_pio_if.h

%build
cp fedora-aarch64.config .config
scripts/kconfig/merge_config.sh -m .config kernel-rpi5.config
scripts/config --disable ARM64_16K_PAGES \
    --enable ARM64_4K_PAGES \
    --disable MODULE_COMPRESS_ALL \
    --set-str LOCALVERSION -%{release}.%{_target_cpu} \
    --disable LOCALVERSION_AUTO
make ARCH=arm64 olddefconfig
grep -qx 'CONFIG_ARM64_4K_PAGES=y' .config
grep -qx 'CONFIG_DEBUG_INFO=y' .config
! grep -qx 'CONFIG_MODULE_COMPRESS_ALL=y' .config
grep -qx 'CONFIG_LOCALVERSION="-%{release}.%{_target_cpu}"' .config
for option in \
    ARCH_BCM ARCH_BCM2835 ARCH_BRCMSTB PCI PCIE_BRCMSTB MFD_RP1 \
    PINCTRL_BCM2712 PINCTRL_RP1 COMMON_CLK_RP1 BCMGENET USB_XHCI_HCD \
    USB_DWC2 USB_STORAGE \
    EXT4_FS RASPBERRYPI_FIRMWARE ARM_RASPBERRYPI_CPUFREQ BCM2711_THERMAL \
    BCM2835_THERMAL SERIAL_8250_BCM2835AUX SERIAL_AMBA_PL011 \
    BRCMFMAC_SDIO BT_HCIUART_BCM SECURITY AUDIT SECURITYFS SECURITY_NETWORK \
    SECURITY_PATH SECURITY_SELINUX SECCOMP NAMESPACES USER_NS CGROUPS \
    CGROUP_BPF DEVTMPFS DEVTMPFS_MOUNT; do
    if ! grep -qx "CONFIG_${option}=y" .config; then
        echo "Required built-in Fedora/Raspberry Pi option is disabled: CONFIG_${option}" >&2
        exit 1
    fi
done
for option in \
    FIRMWARE_RP1 RP1_PIO BRCMFMAC I2C_BCM2835 SPI_BCM2835 \
    MMC_BCM2835 MMC_BCM2835_MMC MMC_SDHCI_IPROC \
    SPI_BCM2835AUX SERIAL_RP1_PIO_UART BT_HCIUART DRM_V3D DRM_VC4 \
    VIDEO_RP1_CFE_DOWNSTREAM SND_RP1_AUDIO_OUT OVERLAY_FS SQUASHFS DM_VERITY; do
    if ! grep -Eq "^CONFIG_${option}=[ym]$" .config; then
        echo "Required Raspberry Pi 5 module is disabled: CONFIG_${option}" >&2
        exit 1
    fi
done
make ARCH=arm64 %{?_smp_mflags} \
    HOSTCFLAGS="-include ${PWD}/scripts/include/kernel-rpi5-host-uapi-types.h" \
    Image modules dtbs
test "$(make -s ARCH=arm64 kernelrelease)" = "%{kernelrelease}"

%install
moddir="%{buildroot}%{_prefix}/lib/modules/%{kernelrelease}"
install -D -m 0644 arch/arm64/boot/Image "${moddir}/vmlinuz"
install -D -m 0644 .config "${moddir}/config"
install -D -m 0644 System.map "${moddir}/System.map"
install -D -m 0755 vmlinux "${moddir}/vmlinux"
make ARCH=arm64 modules_install INSTALL_MOD_PATH=%{buildroot}%{_prefix}
find "${moddir}/kernel" -type f -name '*.ko' -exec chmod u+x {} +
rm -f "${moddir}/build" "${moddir}/source"
make ARCH=arm64 dtbs_install INSTALL_DTBS_PATH="${moddir}/dtb"

%post core
mkdir -p %{_localstatedir}/lib/rpm-state/%{name}
touch %{_localstatedir}/lib/rpm-state/%{name}/installing_core_%{kernelrelease}

%posttrans core
rm -f %{_localstatedir}/lib/rpm-state/%{name}/installing_core_%{kernelrelease}
/bin/kernel-install add %{kernelrelease} /lib/modules/%{kernelrelease}/vmlinuz || :

%preun core
/bin/kernel-install remove %{kernelrelease} || :

%post modules
/sbin/depmod -a %{kernelrelease}

%postun modules
/sbin/depmod -a %{kernelrelease}

%post modules-extra
/sbin/depmod -a %{kernelrelease}

%postun modules-extra
/sbin/depmod -a %{kernelrelease}

%posttrans modules-core
/sbin/depmod -a %{kernelrelease}

%files

%files core
%dir %{_prefix}/lib/modules
%dir %{_prefix}/lib/modules/%{kernelrelease}
%{_prefix}/lib/modules/%{kernelrelease}/vmlinuz
%{_prefix}/lib/modules/%{kernelrelease}/vmlinux
%{_prefix}/lib/modules/%{kernelrelease}/config
%{_prefix}/lib/modules/%{kernelrelease}/System.map
%{_prefix}/lib/modules/%{kernelrelease}/modules.builtin*
%{_prefix}/lib/modules/%{kernelrelease}/dtb
%ghost /boot/vmlinuz-%{kernelrelease}
%ghost /boot/System.map-%{kernelrelease}
%ghost /boot/config-%{kernelrelease}
%ghost /boot/initramfs-%{kernelrelease}.img
%ghost /boot/dtb-%{kernelrelease}

%files modules-core
%dir %{_prefix}/lib/modules/%{kernelrelease}
%{_prefix}/lib/modules/%{kernelrelease}/modules.order
%ghost %attr(0644, root, root) %{_prefix}/lib/modules/%{kernelrelease}/modules.alias
%ghost %attr(0644, root, root) %{_prefix}/lib/modules/%{kernelrelease}/modules.alias.bin
%ghost %attr(0644, root, root) %{_prefix}/lib/modules/%{kernelrelease}/modules.builtin.alias.bin
%ghost %attr(0644, root, root) %{_prefix}/lib/modules/%{kernelrelease}/modules.builtin.bin
%ghost %attr(0644, root, root) %{_prefix}/lib/modules/%{kernelrelease}/modules.dep
%ghost %attr(0644, root, root) %{_prefix}/lib/modules/%{kernelrelease}/modules.dep.bin
%ghost %attr(0644, root, root) %{_prefix}/lib/modules/%{kernelrelease}/modules.devname
%ghost %attr(0644, root, root) %{_prefix}/lib/modules/%{kernelrelease}/modules.softdep
%ghost %attr(0644, root, root) %{_prefix}/lib/modules/%{kernelrelease}/modules.symbols
%ghost %attr(0644, root, root) %{_prefix}/lib/modules/%{kernelrelease}/modules.symbols.bin
%ghost %attr(0644, root, root) %{_prefix}/lib/modules/%{kernelrelease}/modules.weakdep

%files modules
%{_prefix}/lib/modules/%{kernelrelease}/kernel

%files modules-extra
