# Linux Cheat Sheet

## General

### How to get the computer's name, OS, kernel?

```
`uname -a`
```

### How to get hardware info?

* **General hardware info: `lshw` or `hwinfo`
* **Block devices**: `lsblk`
* **CPU**: `lscpu`
* **PCI devices**: `lspci`
* **SCSI/SATA devices**: `lscsi`
* **USB devices**: `lsusb`
* **Individual disk devices**: `hdparm /dev/sda1`
* **Misc info from DMI tables**: 
```
dmidecode -t system

dmidecode -t memory

dmidecode -t bios

dmidecode -t processor
```

### What users are logged into the machine?

`w`

### What are the most