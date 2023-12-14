# oresat-prucam-pirt1280

Kernel module, device tree overlay, and PRU firmware to interface to the
PIRT1280 camera using the PRUs on the [AM335x].

_**NOTE:**_ This was tested on Debian with 5.10 kernel.

## What is a PRU?

Programible Real-time Units. It a microcontroller that shares pins and other
resource with the core processor allowing for custom interface to other hardware
like cameras. See [TI PRU-ICSS webpage] for more details.

## Build and install prucam

**NOTE:** The kernel module requires both the device tree overlay and pru
firmware binaries to be installed to work, so build and insert it last.

### Device tree overlay

- Install dependencies: `$ sudo apt install device-tree-compiler`
- Compile dtbo: `$ make -C src/device_tree_overlay`
- Install dtbo: `$ sudo make -C src/device_tree_overlay install`
- Edit `/boot/uEnv.txt`
  - Change the `#dtb_overlay=<file8>.dtbo` line to `dtb_overlay=/lib/firmware/cfc-00A0.dtbo`
  - Make sure the correct pru rproc `uboot_overlay_pru=` line is not commented
  out (depends kernel version).
  - Make sure the `#enable_uboot_cap_universal=` line is commented out.
- Reboot system to apply device tree overlay: `$ sudo reboot`

### PRU firmware

- Install dependencies: `$ sudo apt install ti-pru-cgt-v2.3 ti-pru-software-v6.0`
- Compile binaries for both PRUs: `$ make`
- Install binaries for both PRUs: `$ sudo make install`
- Start PRUs: `$ sudo ./deploy.sh`

### Kernel module

- Install the kernel headers: ``$ sudo apt-get install linux-headers-`uname -r` ``
- Build kernel module: `$ make -C src/kernel_module clean all`
- Insert kernel module: `$ sudo insmod src/kernel_module/prucam.ko`
- **Note:** To remove kernel module: `$ sudo rmmod prucam`

## Test prucam

- `$ cd scripts`
- Install dependencies: `$ pip install -r requirements.txt`
- Capture image:`$ sudo ./capture.py`
  - This will produce `capture.png`

## Debian package

`prucam-dkms` is the kernel module that provides the sysfs interfaces to the
pru and ar013x camera settings. This package will also install the compiled
both PRUs firmware and the prucam dtbo. **NOTE** when install, it will auto
load the module.

To build `prucam-dkms`:

- Install build dependencies: ``$ sudo apt install --no-install-recommends
  --no-install-suggestions debhelper fakeroot dkms linux-headers-`uname -r`
  device-tree-compiler ti-pru-cgt-v2.3 ti-pru-software-v6.0``
  - The `--no-install-*` flags are due to `dkms` installing `linux-headers`
    package for the wrong kernel version
- Build `prucam` Debian packages: `$ dpkg-buildpackage -us -uc`

[TI PRU-ICSS webpage]:https://processors.wiki.ti.com/index.php/PRU-ICSS
[AM335x]:https://www.ti.com/processors/sitara-arm/am335x-cortex-a8/overview.html
