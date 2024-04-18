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

## Meta

### What users are logged into the machine?

`w` shows you who is logged in, their login time, their CPU time, etc.

```
tyralyn@tyralyn-laptop ~ $ w
 17:03:58 up  3:44,  3 users,  load average: 0.50, 0.58, 0.64
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
tyralyn  tty8     :0               13:20    3:44m  9:15   0.11s /sbin/upstart --user
tyralyn  pts/2    :0.0             13:27    2:15m  0.19s  0.19s -bash
tyralyn  pts/5    :0.0             13:22    5.00s  0.58s  0.02s w
```

`ac` shows when users connected.

`lastcomm` shows recently-run commands.

Process accounting is enabled/disabled with `accton` and summarizedf with `sa`.

### How long does it take to run a command?

`time` times commands:

```
time -v host www.cyberciti.biz

time -v ls
```

### How can you control how commands are run?

Adding an `&` to the end of a command runs it in the background.



### What are the most