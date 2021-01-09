# winusb
Script to create Windows 10 bootable USB from linux

Visit the [blog page](https://programagik.blogspot.com/) for additional information.

This script works for Ubuntu and can be modified for any other distro by changing the `apt` package to others.

### Step to prepare:
1. Download Windows10.iso file from Microsoft website.
1. Format USB to FAT32 and mount it.

To run the program, run the script as follows:

`$ bash winusb.sh <windows10.iso> <usb_drive_location>`

*Warning: Do not use `/` at the end of USB mount drive since it is added in the script.*
