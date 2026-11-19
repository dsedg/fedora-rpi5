# Kernel configuration reference

Generated from `kernel-rpi5.config` using `linux-1ef812a522e2a929f7a9a00f7e2ca0cff21086c7` Kconfig files (ARCH=arm64).

Options documented: 83 (83 config assignments).

## CONFIG_ARCH_BRCMSTB

- **Value in `kernel-rpi5.config`:** `y`
- **Prompt:** Broadcom Set-Top-Box SoCs

**Description**

This enables support for Broadcom's ARMv8 Set Top Box SoCs

## CONFIG_ARM_RASPBERRYPI_CPUFREQ

- **Value in `kernel-rpi5.config`:** `y`
- **Prompt:** Raspberry Pi cpufreq support

**Description**

This adds the CPUFreq driver for Raspberry Pi

If in doubt, say N.

## CONFIG_BACKLIGHT_RPI

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Raspberry Pi display firmware driven backlight

**Description**

If you have the Raspberry Pi DSI touchscreen display, say Y to
enable the mailbox-controlled backlight driver.

## CONFIG_BCM2711_THERMAL

- **Value in `kernel-rpi5.config`:** `y`
- **Prompt:** Broadcom AVS RO thermal sensor driver

**Description**

Support for thermal sensors on Broadcom BCM2711 SoCs.

## CONFIG_BCM2835_THERMAL

- **Value in `kernel-rpi5.config`:** `y`
- **Prompt:** Thermal sensors on bcm2835 SoC

**Description**

Support for thermal sensors on Broadcom bcm2835 SoCs.

## CONFIG_BCM2835_VCHIQ

- **Value in `kernel-rpi5.config`:** `y`
- **Prompt:** BCM2835 VCHIQ

**Description**

Broadcom BCM2835 and similar SoCs have a VPU called VideoCore.
This config enables the VCHIQ driver, which implements a
messaging interface between the kernel and the firmware running
on VideoCore. Other drivers use this interface to communicate to
the VPU. More specifically, the VCHIQ driver is used by
audio/video and camera drivers as well as for implementing MMAL
API, which is in turn used by several multimedia services on the
BCM2835 family of SoCs.

Defaults to Y when the Broadcom Videocore services are included
in the build, N otherwise.

## CONFIG_BCM2835_WDT

- **Value in `kernel-rpi5.config`:** `y`
- **Prompt:** Broadcom BCM2835 hardware watchdog

**Description**

Watchdog driver for the built in watchdog hardware in Broadcom
BCM2835 SoC.

To compile this driver as a loadable module, choose M here.
The module will be called bcm2835_wdt.

## CONFIG_BCMGENET

- **Value in `kernel-rpi5.config`:** `y`
- **Prompt:** Broadcom GENET internal MAC support

**Description**

This driver supports the built-in Ethernet MACs found in the
Broadcom BCM7xxx Set Top Box family chipset.

## CONFIG_BCM_VCIO

- **Value in `kernel-rpi5.config`:** `y`
- **Prompt:** Mailbox userspace access

**Description**

Gives access to the mailbox property channel from userspace.

## CONFIG_BRCMDBG

- **Value in `kernel-rpi5.config`:** `y`
- **Prompt:** Broadcom driver debug functions

**Description**

Selecting this enables additional code for debug purposes.

## CONFIG_BRCM_CHAR_DRIVERS

- **Value in `kernel-rpi5.config`:** `y`
- **Prompt:** Broadcom Char Drivers

**Description**

Broadcom's char drivers

## CONFIG_COMMON_CLK_RP1

- **Value in `kernel-rpi5.config`:** `y`
- **Prompt:** Raspberry Pi RP1-based clock support

**Description**

Enable common clock framework support for Raspberry Pi RP1.
This multi-function device has 3 main PLLs and several clock
generators to drive the internal sub-peripherals.

## CONFIG_COMMON_CLK_RP1_SDIO

- **Value in `kernel-rpi5.config`:** `y`
- **Prompt:** Clock driver for the RP1 SDIO interfaces

**Description**

SDIO clock driver for the RP1 support chip

## CONFIG_DMA_BCM2708

- **Value in `kernel-rpi5.config`:** `y`
- **Prompt:** BCM2708 DMA legacy API support

**Description**

No help text is defined for this option in Kconfig.

## CONFIG_DMA_BCM2835

- **Value in `kernel-rpi5.config`:** `y`
- **Prompt:** BCM2835 DMA engine support

**Description**

No help text is defined for this option in Kconfig.

## CONFIG_DRM_RP1_DPI

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** DRM Support for RP1 DPI

**Description**

Choose this option to enable DPI output on Raspberry Pi RP1

There is an optional dependency on RP1_PIO, as the PIO block
must be used to fix up interlaced sync. Interlaced DPI modes
will be unavailable when RP1_PIO is not selected.

## CONFIG_DRM_RP1_DSI

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** DRM Support for RP1 DSI

**Description**

Choose this option to enable DSI display on RP1

## CONFIG_DRM_RP1_VEC

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** DRM Support for RP1 VEC

**Description**

Choose this option to enable Video Out on RP1

## CONFIG_FB_BCM2708

- **Value in `kernel-rpi5.config`:** `y`
- **Prompt:** BCM2708 framebuffer support

**Description**

This framebuffer device driver is for the BCM2708 framebuffer.

If you want to compile this as a module (=code which can be
inserted into and removed from the running kernel), say M
here and read <file:Documentation/kbuild/modules.txt>.  The module
will be called bcm2708_fb.

## CONFIG_FB_RPISENSE

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Raspberry Pi Sense HAT framebuffer

**Description**

This is the framebuffer driver for the Raspberry Pi Sense HAT

## CONFIG_FIRMWARE_RP1

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** RP1 Firmware Driver

**Description**

The Raspberry Pi RP1 processor presents a firmware
interface using shared memory and a mailbox. To enable
the driver that communicates with it, say Y. Otherwise,
say N.

## CONFIG_GPIO_BCM_VIRT

- **Value in `kernel-rpi5.config`:** `y`
- **Prompt:** Broadcom Virt GPIO

**Description**

Turn on virtual GPIO support for Broadcom BCM283X chips.

## CONFIG_I2C_BCM2708

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** BCM2708 BSC

**Description**

Enabling this option will add BSC (Broadcom Serial Controller)
support for the BCM2708. BSC is a Broadcom proprietary bus compatible
with I2C/TWI/SMBus.

## CONFIG_MBOX_RP1

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** RP1 Mailbox

**Description**

An implementation of a mailbox interface to the Raspberry Pi RP1 I/O
interface. Although written as a mailbox driver, the hardware only
provides an array of 32 doorbells.
Say Y here if you want to use the RP1 Mailbox.

## CONFIG_MFD_ARIZONA_I2C

- **Value in `kernel-rpi5.config`:** `y`
- **Prompt:** Cirrus Logic/Wolfson Microelectronics Arizona platform with I2C

**Description**

Support for the Cirrus Logic/Wolfson Microelectronics Arizona platform
audio SoC core functionality controlled via I2C.

## CONFIG_MFD_RASPBERRYPI_POE_HAT

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Raspberry Pi PoE HAT MFD

**Description**

This module supports the PWM fan controller found on the Raspberry Pi
POE and POE+ HAT boards, and the power supply driver on the POE+ HAT.
(Functionally it relies on MFD_SIMPLE_MFD_I2C to provide the framework
that loads the child drivers).

## CONFIG_MFD_RP1

- **Value in `kernel-rpi5.config`:** `y`
- **Prompt:** RP1 MFD driver

**Description**

Support for the RP1 peripheral chip.

This driver provides support for the Raspberry Pi RP1 peripheral chip.
It is responsible for enabling the Device Tree node once the PCIe endpoint
has been configured, and handling interrupts.

## CONFIG_MFD_WM5102

- **Value in `kernel-rpi5.config`:** `y`
- **Prompt:** Wolfson Microelectronics WM5102

**Description**

Support for Wolfson Microelectronics WM5102 low power audio SoC

## CONFIG_MMC_BCM2835

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Broadcom BCM2835 SDHOST MMC Controller support

**Description**

This selects the BCM2835 SDHOST MMC controller. If you have
a BCM2835 platform with SD or MMC devices, say Y or M here.

Note that the BCM2835 has two SD controllers: The Arasan
sdhci controller (supported by MMC_SDHCI_IPROC) and a custom
sdhost controller (supported by this driver).

If unsure, say N.

## CONFIG_MMC_BCM2835_DMA

- **Value in `kernel-rpi5.config`:** `y`
- **Prompt:** DMA support on BCM2835 Arasan controller

**Description**

Enable DMA support on the Arasan SDHCI controller in Broadcom 2708
based chips.

If unsure, say N.

## CONFIG_MMC_BCM2835_MMC

- **Value in `kernel-rpi5.config`:** `y`
- **Prompt:** MMC support on BCM2835

**Description**

This selects the MMC Interface on BCM2835.

If you have a controller with this interface, say Y or M here.

If unsure, say N.

## CONFIG_PINCTRL_RP1

- **Value in `kernel-rpi5.config`:** `y`
- **Prompt:** Pinctrl driver for RP1

**Description**

Enable the gpio and pinctrl/mux driver for RaspberryPi RP1
multi function device.

## CONFIG_PWM_BRCMSTB

- **Value in `kernel-rpi5.config`:** `y`
- **Prompt:** Broadcom STB PWM support

**Description**

Generic PWM framework driver for the Broadcom Set-top-Box
SoCs (BCM7xxx).

To compile this driver as a module, choose M Here: the module
will be called pwm-brcmstb.c.

## CONFIG_PWM_PIO_RP1

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** RP1 PIO PWM support

**Description**

This is a PWM framework driver for Raspberry Pi 5, using the PIO
hardware of RP1 to provide PWM functionality. Supports up to 4
instances on GPIOs in bank 0.

To compile this driver as a module, choose M here: the module
will be called pwm-pio-rp1.

## CONFIG_PWM_RP1

- **Value in `kernel-rpi5.config`:** `y`
- **Prompt:** RP1 PWM support

**Description**

PWM framework driver for Raspberry Pi RP1 controller

To compile this driver as a module, choose M here: the module
will be called pwm-rp1.

## CONFIG_RASPBERRYPI_GPIOMEM

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Rootless GPIO access via mmap() on Raspberry Pi boards

**Description**

Provides users with root-free access to the GPIO registers
on the board. Calling mmap(/dev/gpiomem) will map the GPIO
register page to the user's pointer.

## CONFIG_RP1_PIO

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Raspberry Pi RP1 PIO driver

**Description**

Driver providing control of the Raspberry Pi PIO block, as found in
RP1.

## CONFIG_RPI_AXIPERF

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** RaspberryPi AXI Performance monitors

**Description**

Say y if you want to use Raspberry Pi AXI performance monitors, m if
you want to build it as a module.

## CONFIG_RPI_POE_POWER

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Raspberry Pi PoE+ HAT power supply driver

**Description**

Say Y here to enable support for Raspberry Pi PoE+ (Power over Ethernet
Plus) HAT current measurement.

## CONFIG_SENSORS_RP1_ADC

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** RP1 ADC and temperature sensor driver

**Description**

Say yes here to enable support for the voltage and temperature
sensors of the Raspberry Pi RP1 peripheral chip.

## CONFIG_SERIAL_RP1_PIO_UART

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Raspberry Pi RP1 PIO UART support

**Description**

This selects a software UART implemented using the RP1 PIO block,
with DMA moving data in and out of the PIO FIFOs and a PIO
interrupt used for break detection. Only 8N1 with no hardware
flow control is supported. Only useful on Raspberry Pi 5 and
newer platforms that have an RP1 southbridge.

If unsure, say N.

## CONFIG_SND_BCM2708_SOC_ADAU1977_ADC

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Support for ADAU1977 ADC

**Description**

Say Y or M if you want to add support for ADAU1977 ADC.

## CONFIG_SND_BCM2708_SOC_ALLO_BOSS2_DAC

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Support for Allo Boss2 DAC

**Description**

Say Y or M if you want to add support for Allo Boss2 DAC.

## CONFIG_SND_BCM2708_SOC_ALLO_BOSS_DAC

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Support for Allo Boss DAC

**Description**

Say Y or M if you want to add support for Allo Boss DAC.

## CONFIG_SND_BCM2708_SOC_ALLO_DIGIONE

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Support for Allo DigiOne

**Description**

Say Y or M if you want to add support for Allo DigiOne.

## CONFIG_SND_BCM2708_SOC_ALLO_KATANA_DAC

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Support for Allo Katana DAC

**Description**

Say Y or M if you want to add support for Allo Katana DAC.

## CONFIG_SND_BCM2708_SOC_ALLO_PIANO_DAC

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Support for Allo Piano DAC

**Description**

Say Y or M if you want to add support for Allo Piano DAC.

## CONFIG_SND_BCM2708_SOC_ALLO_PIANO_DAC_PLUS

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Support for Allo Piano DAC Plus

**Description**

Say Y or M if you want to add support for Allo Piano DAC Plus.

## CONFIG_SND_BCM2708_SOC_CHIPDIP_DAC

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Support for the ChipDip DAC

**Description**

Say Y or M if you want to add support for the ChipDip DAC soundcard

## CONFIG_SND_BCM2708_SOC_DIONAUDIO_LOCO

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Support for Dion Audio LOCO DAC-AMP

**Description**

Say Y or M if you want to add support for Dion Audio LOCO.

## CONFIG_SND_BCM2708_SOC_DIONAUDIO_LOCO_V2

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Support for Dion Audio LOCO-V2 DAC-AMP

**Description**

Say Y or M if you want to add support for Dion Audio LOCO-V2.

## CONFIG_SND_BCM2708_SOC_FE_PI_AUDIO

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Support for Fe-Pi-Audio

**Description**

Say Y or M if you want to add support for Fe-Pi-Audio.

## CONFIG_SND_BCM2708_SOC_GOOGLEVOICEHAT_SOUNDCARD

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Support for Google voiceHAT soundcard

**Description**

Say Y or M if you want to add support for voiceHAT soundcard.

## CONFIG_SND_BCM2708_SOC_HIFIBERRY_ADC

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Support for HifiBerry ADC

**Description**

Say Y or M if you want to add support for HifiBerry ADC.
Use this module for HiFiBerry's ADC-only sound cards

## CONFIG_SND_BCM2708_SOC_HIFIBERRY_AMP

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Support for the HifiBerry Amp

**Description**

Say Y or M if you want to add support for the HifiBerry Amp amplifier board.

## CONFIG_SND_BCM2708_SOC_HIFIBERRY_DAC

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Support for HifiBerry DAC and DAC8X

**Description**

Say Y or M if you want to add support for HifiBerry DAC and DAC8X.
Note: DAC8X only works on PI5

## CONFIG_SND_BCM2708_SOC_HIFIBERRY_DACPLUS

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Support for HifiBerry DAC+

**Description**

Say Y or M if you want to add support for HifiBerry DAC+.

## CONFIG_SND_BCM2708_SOC_HIFIBERRY_DACPLUSADC

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Support for HifiBerry DAC+ADC

**Description**

Say Y or M if you want to add support for HifiBerry DAC+ADC.

## CONFIG_SND_BCM2708_SOC_HIFIBERRY_DACPLUSADCPRO

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Support for HifiBerry DAC+ADC PRO

**Description**

Say Y or M if you want to add support for HifiBerry DAC+ADC PRO.

## CONFIG_SND_BCM2708_SOC_HIFIBERRY_DACPLUSDSP

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Support for HifiBerry DAC+DSP

**Description**

Say Y or M if you want to add support for HifiBerry DSP-DAC.

## CONFIG_SND_BCM2708_SOC_HIFIBERRY_DACPLUSHD

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Support for HifiBerry DAC+ HD

**Description**

Say Y or M if you want to add support for HifiBerry DAC+ HD.

## CONFIG_SND_BCM2708_SOC_HIFIBERRY_DIGI

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Support for HifiBerry Digi

**Description**

Say Y or M if you want to add support for HifiBerry Digi S/PDIF output board.

## CONFIG_SND_BCM2708_SOC_HIFIBERRY_STUDIO_DAC8X

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Support for HifiBerry Studio DAC8x soundcards

**Description**

Say Y or M if you want to add support for

## CONFIG_SND_BCM2708_SOC_IQAUDIO_CODEC

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Support for IQaudIO-CODEC

**Description**

Say Y or M if you want to add support for IQaudIO-CODEC.

## CONFIG_SND_BCM2708_SOC_IQAUDIO_DAC

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Support for IQaudIO-DAC

**Description**

Say Y or M if you want to add support for IQaudIO-DAC.

## CONFIG_SND_BCM2708_SOC_IQAUDIO_DIGI

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Support for IQAudIO Digi

**Description**

Say Y or M if you want to add support for IQAudIO Digital IO board.

## CONFIG_SND_BCM2708_SOC_I_SABRE_Q2M

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Support for Audiophonics I-Sabre Q2M DAC

**Description**

No help text is defined for this option in Kconfig.

## CONFIG_SND_BCM2708_SOC_JUSTBOOM_BOTH

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Support for simultaneous JustBoom Digi and JustBoom DAC

**Description**

Say Y or M if you want to add support for simultaneous
JustBoom Digi and JustBoom DAC.

This is not the right choice if you only have one but both of
these cards.

## CONFIG_SND_BCM2708_SOC_JUSTBOOM_DAC

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Support for JustBoom DAC

**Description**

Say Y or M if you want to add support for JustBoom DAC.

## CONFIG_SND_BCM2708_SOC_JUSTBOOM_DIGI

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Support for JustBoom Digi

**Description**

Say Y or M if you want to add support for JustBoom Digi.

## CONFIG_SND_BCM2708_SOC_PIFI_40

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Support for the PiFi-40 amp

**Description**

Say Y or M if you want to add support for the PiFi40 amp board

## CONFIG_SND_BCM2708_SOC_RPI_CIRRUS

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Support for Cirrus Logic Audio Card

**Description**

Say Y or M if you want to add support for the Wolfson and
Cirrus Logic audio cards.

## CONFIG_SND_BCM2708_SOC_RPI_DAC

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Support for RPi-DAC

**Description**

Say Y or M if you want to add support for RPi-DAC.

## CONFIG_SND_BCM2708_SOC_RPI_PROTO

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Support for Rpi-PROTO

**Description**

Say Y or M if you want to add support for Audio Codec Board PROTO (WM8731).

## CONFIG_SND_RP1_AUDIO_OUT

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** PWM Audio Out from RP1

**Description**

Say Y or M if you want to add support for PWM digital
audio output from a Raspberry Pi 5, 500 or CM5.

Output is from RP1 GPIOs pins 12 and 13 only, and additional
components will be needed. It may be useful when HDMI, I2S
or USB audio devices are unavailable, or for compatibility.

## CONFIG_USB_DWC2

- **Value in `kernel-rpi5.config`:** `y`
- **Prompt:** DesignWare USB2 DRD Core Support

**Description**

Say Y here if your system has a Dual Role Hi-Speed USB
controller based on the DesignWare HSOTG IP Core.

For host mode, if you choose to build the driver as dynamically
linked modules, the core module will be called dwc2.ko, the PCI
bus interface module (if you have a PCI bus system) will be
called dwc2_pci.ko, and the platform interface module (for
controllers directly connected to the CPU) will be called
dwc2_platform.ko. For all modes(host, gadget and dual-role), there
will be an additional module named dwc2.ko.

## CONFIG_USB_STORAGE

- **Value in `kernel-rpi5.config`:** `y`
- **Prompt:** USB Mass Storage support

**Description**

Say Y here if you want to connect USB mass storage devices to your
computer's USB port. This is the driver you need for USB
floppy drives, USB hard disks, USB tape drives, USB CD-ROMs,
USB flash devices, and memory sticks, along with
similar devices. This driver may also be used for some cameras
and card readers.

This option depends on 'SCSI' support being enabled, but you
probably also need 'SCSI device support: SCSI disk support'
(BLK_DEV_SD) for most USB storage devices.

To compile this driver as a module, choose M here: the
module will be called usb-storage.

## CONFIG_VIDEO_BCM2835_UNICAM_LEGACY

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Broadcom BCM283x/BCM271x Unicam video capture driver - no MC

**Description**

Say Y here to enable support for the BCM283x/BCM271x CSI-2 receiver.
This is a V4L2 driver that controls the CSI-2 receiver directly,
independently from the VC4 firmware.
This is the downstream version of this driver that still supports
being driven from the video node for simple devices. The mainline
driver only supports using Media Controller.
This driver is mutually exclusive with the use of bcm2835-camera. The
firmware will disable all access to the peripheral from within the
firmware if it finds a DT node using it, and bcm2835-camera will
therefore fail to probe.

To compile this driver as a module, choose M here. The module will be
called bcm2835-unicam.

## CONFIG_VIDEO_CODEC_BCM2835

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** BCM2835 Video codec support

**Description**

Say Y here to enable the V4L2 video codecs for
Broadcom BCM2835 SoC. This operates over the VCHIQ interface
to a service running on VideoCore.

## CONFIG_VIDEO_ISP_BCM2835

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** BCM2835 ISP support

**Description**

This is the V4L2 driver for the Broadcom BCM2835 ISP hardware.
This operates over the VCHIQ interface to a service running on
VideoCore.

To compile this driver as a module, choose M here: the module
will be called bcm2835-isp.

## CONFIG_VIDEO_RP1_CFE_DOWNSTREAM

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** RP1 DOWNSTREAM Camera Frond End (CFE) video capture driver

**Description**

Say Y here to enable support for the RP1 Camera Front End using
the downstream driver.

To compile this driver as a module, choose M here. The module will be
called rp1-cfe-downstream.

## CONFIG_VIDEO_RPI_HEVC_DEC

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Raspberry Pi HEVC decoder

**Description**

Support for the Raspberry Pi HEVC / H265 H/W decoder as a stateless
V4L2 decoder device.

To compile this driver as a module, choose M here: the module
will be called rpi-hevc-dec.

## CONFIG_WS2812_PIO_RP1

- **Value in `kernel-rpi5.config`:** `m`
- **Prompt:** Raspberry Pi PIO-base WS2812 driver

**Description**

Driver for the WS2812 (NeoPixel) LEDs using the RP1 PIO hardware.
The driver creates a character device to which rgbw pixels may be
written. Single-byte writes to offset 0 set the brightness at
runtime.
