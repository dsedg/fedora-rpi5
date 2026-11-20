%{!?kernel_commit:%global kernel_commit 1ef812a522e2a929f7a9a00f7e2ca0cff21086c7}
%{!?kernel_version:%global kernel_version 7.3.5}
%{!?kernel_flavor:%global kernel_flavor standard}

%if "%{kernel_flavor}" == "bigscreen"
Name:           kernel-rpi5-bigscreen
Release:        300.rpi5bs%{?dist}
%else
Name:           kernel
Release:        300.rpi5%{?dist}
%endif
Version:        %{kernel_version}
%global kernelrelease %{version}-%{release}.%{_target_cpu}
Summary:        Linux kernel for Raspberry Pi 5
License:        GPL-2.0-only AND GPL-2.0-or-later AND GPL-1.0-or-later AND MIT AND BSD-2-Clause AND BSD-3-Clause AND ISC AND X11
URL:            https://github.com/raspberrypi/linux
Source0:        https://github.com/raspberrypi/linux/archive/%{kernel_commit}.tar.gz
# Fedora f45 kernel-aarch64-fedora.config at commit 3393e4e0db8129398c14fed17e09abdd0d1d9822.
Source1:        kernel-aarch64-fedora.config
Source2:        kernel-rpi5.config
Source3:        kernel-rpi5-host-uapi-types.h
Source4:        kernel-rpi5-bigscreen.config
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

%package modules-debuginfo
Summary:        Debug information for Raspberry Pi 5 kernel modules
Requires:       kernel-modules-uname-r = %{kernelrelease}
AutoReq:        no
AutoProv:       no

%description modules-debuginfo
The debug information for loadable Raspberry Pi 5 kernel modules.

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
cp %{SOURCE4} kernel-rpi5-bigscreen.config
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
%if "%{kernel_flavor}" == "bigscreen"
scripts/kconfig/merge_config.sh -m .config kernel-rpi5-bigscreen.config
%endif
scripts/config --disable ARM64_16K_PAGES \
    --enable ARM64_4K_PAGES \
    --disable MODULE_COMPRESS_ALL \
    --disable DRM_KUNIT_TEST \
    --disable DRM_XE \
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
    FIRMWARE_RP1 RP1_PIO BRCMFMAC BLK_DEV_NVME I2C_BCM2835 SPI_BCM2835 \
    MMC_BCM2835 MMC_BCM2835_MMC MMC_SDHCI_IPROC \
    SPI_BCM2835AUX SERIAL_RP1_PIO_UART BT_HCIUART DRM_V3D DRM_VC4 \
    VIDEO_RP1_CFE_DOWNSTREAM SND_RP1_AUDIO_OUT OVERLAY_FS SQUASHFS DM_VERITY; do
    if ! grep -Eq "^CONFIG_${option}=[ym]$" .config; then
        echo "Required Raspberry Pi 5 module is disabled: CONFIG_${option}" >&2
        exit 1
    fi
done
%if "%{kernel_flavor}" == "bigscreen"
for option in \
    DRM_AMDGPU DRM_AST DRM_BOCHS DRM_MGAG200 DRM_NOUVEAU DRM_QXL \
    DRM_VIRTIO_GPU DRM_VMWGFX B43 B43LEGACY BRCMFMAC_PCIE BRCMFMAC_USB \
    WLAN_VENDOR_ATH WLAN_VENDOR_INTEL WLAN_VENDOR_MARVELL \
    WLAN_VENDOR_MEDIATEK WLAN_VENDOR_MICROCHIP WLAN_VENDOR_NXP \
    WLAN_VENDOR_QUANTENNA WLAN_VENDOR_RALINK WLAN_VENDOR_REALTEK \
    WLAN_VENDOR_RSI WLAN_VENDOR_ST WLAN_VENDOR_TI WLAN_VENDOR_ZYDAS \
    PCI_AARDVARK PCI_HISI PCI_HOST_GENERIC PCI_HOST_THUNDER_ECAM \
    PCI_HOST_THUNDER_PEM PCI_HYPERV PCI_HYPERV_INTERFACE PCI_IMX6 \
    PCI_IMX6_HOST PCI_J721E_HOST PCI_KEYSTONE_HOST PCI_LAYERSCAPE \
    PCI_MESON PCI_MVEBU PCI_SKY1_HOST PCI_TEGRA PCI_XGENE PCIE_APPLE \
    PCIE_ARMADA_8K PCIE_CADENCE_HOST PCIE_CADENCE_PLAT_HOST \
    PCIE_DW_HOST PCIE_DW_PLAT_HOST PCIE_HISI_STB PCIE_KIRIN \
    PCIE_LAYERSCAPE_GEN4 PCIE_MICROCHIP_HOST PCIE_MOBIVEIL \
    PCIE_MOBIVEIL_PLAT PCIE_NXP_S32G PCIE_QCOM \
    PCIE_RENESAS_RZG3S_HOST PCIE_ROCKCHIP_DW_HOST PCIE_ROCKCHIP_HOST \
    PCIE_TEGRA194_HOST PCIE_TEGRA264 PCIE_XILINX PCIE_XILINX_CPM \
    PCIE_XILINX_DMA_PL PCIE_XILINX_NWL CXL_PCI PCI_IOV PCI_P2PDMA \
    PCI_PASID PCI_PRI PCI_PF_STUB PCI_STUB VFIO_PCI \
    CRYPTO_DEV_QAT CRYPTO_DEV_QAT_C3XXX CRYPTO_DEV_QAT_C3XXXVF \
    CRYPTO_DEV_QAT_C62X CRYPTO_DEV_QAT_C62XVF \
    CRYPTO_DEV_QAT_DH895xCC CRYPTO_DEV_QAT_DH895xCCVF \
    CRYPTO_DEV_QAT_420XX CRYPTO_DEV_QAT_4XXX \
    CRYPTO_DEV_QAT_ERROR_INJECTION INFINIBAND_USNIC \
    BE2ISCSI BE2NET INFINIBAND_CXGB4 INFINIBAND_OCRDMA \
    INFINIBAND_ISER INFINIBAND_ISERT \
    ISCSI_BOOT_SYSFS ISCSI_IBFT ISCSI_TARGET ISCSI_TARGET_CXGB4 \
    ISCSI_TCP QEDI \
    BLK_DEV_RBD CEPH_FS CEPH_FS_POSIX_ACL \
    CEPH_FS_SECURITY_LABEL CEPH_FSCACHE CEPH_LIB \
    SCSI_3W_9XXX SCSI_3W_SAS SCSI_AACRAID SCSI_ESAS2R SCSI_HISI_SAS \
    SCSI_HPSA \
    MEGARAID_LEGACY MEGARAID_MAILBOX MEGARAID_MM MEGARAID_NEWGEN \
    MEGARAID_SAS SCSI_AM53C974 SCSI_ARCMSR SCSI_BNX2_ISCSI \
    SCSI_BNX2X_FCOE SCSI_CHELSIO_FCOE SCSI_CXGB3_ISCSI \
    SCSI_CXGB4_ISCSI SCSI_DC395x SCSI_DMX3191D SCSI_EFCT \
    SCSI_FDOMAIN_PCI SCSI_FC_ATTRS SCSI_HPTIOP SCSI_INIA100 SCSI_INITIO \
    SCSI_IPR SCSI_ISCSI_ATTRS SCSI_LEAPRAID SCSI_LPFC SCSI_LIB_KUNIT_TEST \
    SCSI_MPI3MR SCSI_MPT2SAS SCSI_MPT3SAS \
    SCSI_MVSAS SCSI_MVUMI SCSI_MYRB SCSI_MYRS SCSI_PMCRAID \
    SCSI_QLA_FC SCSI_QLA_ISCSI SCSI_QLOGIC_1280 SCSI_SMARTPQI \
    SCSI_SNIC SCSI_STEX SCSI_SYM53C8XX_2 SCSI_SAS_ATA SCSI_SAS_ATTRS \
    SCSI_SAS_HOST_SMP SCSI_SAS_LIBSAS SCSI_SPI_ATTRS SCSI_SRP_ATTRS \
    SCSI_DEBUG SCSI_PROTO_TEST SCSI_UFS_AMD_VERSAL2 \
    SCSI_UFS_CDNS_PLATFORM SCSI_UFS_HISI SCSI_UFS_QCOM \
    SCSI_UFS_ROCKCHIP SCSI_UFS_TI_J721E SCSI_VIRTIO SCSI_WD719X \
    SCSI_ENCLOSURE SCSI_UFSHCD SCSI_UFSHCD_PCI SCSI_UFSHCD_PLATFORM \
    ARCH_APPLE ARCH_BST ARCH_CIX ARCH_HISI ARCH_K3 ARCH_LAYERSCAPE \
    ARCH_MESON ARCH_MVEBU ARCH_MXC ARCH_NXP ARCH_QCOM ARCH_R8A774A1 \
    ARCH_R8A78000 ARCH_R9A07G043 ARCH_R9A07G044 ARCH_R9A07G054 \
    ARCH_R9A08G045 ARCH_R9A08G046 ARCH_R9A09G011 ARCH_R9A09G056 \
    ARCH_R9A09G057 ARCH_R9A09G077 ARCH_R9A09G087 ARCH_RENESAS \
    ARCH_ROCKCHIP ARCH_S32 ARCH_SEATTLE ARCH_SUNXI ARCH_SYNQUACER \
    ARCH_TEGRA ARCH_TEGRA_132_SOC ARCH_TEGRA_186_SOC ARCH_TEGRA_194_SOC \
    ARCH_TEGRA_210_SOC ARCH_TEGRA_234_SOC ARCH_TEGRA_238_SOC \
    ARCH_TEGRA_241_SOC ARCH_TEGRA_264_SOC ARCH_THUNDER ARCH_THUNDER2 \
    ARCH_VEXPRESS ARCH_XGENE ARCH_ZYNQMP SOC_IMX8M SOC_IMX9 \
    SOC_TEGRA_CBB SOC_TEGRA_FLOWCTRL SOC_TI; do
    if grep -Eq "^CONFIG_${option}=[ym]$" .config; then
        echo "Bigscreen kernel unexpectedly enables CONFIG_${option}" >&2
        exit 1
    fi
done
if ! grep -Eq '^CONFIG_MEDIA_SUPPORT=[ym]$' .config; then
    echo "Required Bigscreen media support is disabled: CONFIG_MEDIA_SUPPORT" >&2
    exit 1
fi
for option in MEDIA_ANALOG_TV_SUPPORT MEDIA_DIGITAL_TV_SUPPORT MEDIA_RADIO_SUPPORT; do
    if ! grep -qx "CONFIG_${option}=y" .config; then
        echo "Required Bigscreen media capture option is disabled: CONFIG_${option}" >&2
        exit 1
    fi
done
for option in SND_BCM2708_SOC_RPI_CIRRUS SND_BCM2708_SOC_HIFIBERRY_DAC \
    MFD_RASPBERRYPI_POE_HAT RPI_POE_POWER FB_RPISENSE; do
    if ! grep -qx "CONFIG_${option}=m" .config; then
        echo "Required Raspberry Pi add-on option is not a module: CONFIG_${option}" >&2
        exit 1
    fi
done
%endif
for option in MFD_ARIZONA MFD_ARIZONA_I2C MFD_WM5102; do
    if ! grep -qx "CONFIG_${option}=y" .config; then
        echo "Required built-in Cirrus audio dependency is disabled: CONFIG_${option}" >&2
        exit 1
    fi
done
for option in SND_SOC_ARIZONA SND_SOC_WM5102; do
    if ! grep -qx "CONFIG_${option}=m" .config; then
        echo "Required Cirrus audio dependency is not a module: CONFIG_${option}" >&2
        exit 1
    fi
done
! grep -Eq '^CONFIG_DRM_XE=[ym]$' .config
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

%files modules-debuginfo
%{_prefix}/lib/debug/usr/lib/modules/%{kernelrelease}/kernel

%files modules-extra
