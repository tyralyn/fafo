# Linux Debugging Tips

## Overall

### How to get basic machine and hardware info:

To get info on this machine's name, OS, kernel: `uname -a`

To get **L**inux **S**ystem **H**ardware info: `lshw`

To get CPU information: `lscpu`

To get block device information: `lsblk`

To get USB device and controller info: `lsusb`

To get PCI device info: `lspci`

To get SCSI/SATA device info: `lsscsi`

To get SATA device info: `hdparm /dev/sda1`

To get filesystem information: `fdisk -l`

To get info from DMI tables:
```
dmidecode -t system

dmidecode -t memory

dmidecode -t bios

dmidecode -t processor

```

To get general device info, see the `/dev` directory.

### Other basic info:

To get who is logged in: `w`

To get how long system has been running: `uptime`

To get activities of each processor: `mpstat -P ALL`


### What temperature is my XXX?

For hard drives, use `hddtemp`:
```
hddtemp /dev/DISK
hddtemp /dev/sg0
```

For CPU:
```
tyralyn@tyralyn-laptop ~ $ sensors
coretemp-isa-0000
Adapter: ISA adapter
Physical id 0:  +32.0°C  (high = +100.0°C, crit = +100.0°C)
Core 0:         +30.0°C  (high = +100.0°C, crit = +100.0°C)
Core 1:         +29.0°C  (high = +100.0°C, crit = +100.0°C)
```


### How can I see overall info (CPU, IO) for the system?

The `iostat` command reports in/out for a system:

```
tyralyn@tyralyn-laptop ~ $ iostat
Linux 4.4.0-21-generic (tyralyn-laptop) 	05/07/2023 	_x86_64_	(4 CPU)

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           6.58    0.17    1.91    6.39    0.00   84.95

Device:            tps    kB_read/s    kB_wrtn/s    kB_read    kB_wrtn
sda              47.42       539.25       370.58    3496217    2402638
dm-0              0.03         0.50         0.05       3240        336

```

By default, `iostat`'s first report shows stats for the entire duration since system startup / boot, and subsequent reports show stats since the last report.

* `-x`: extended statistics report
* `-t`: enable time for each report
* `-z`: exclude devices that haven't done anything
* `-k`: use kilobytes instead of blocks
* `-m`: use megabytes/second
* `-d`: generate reports at intervals


### How can I see overall info (processes, mem, swap, IO, system, CPU) for a VM?

The `vmstat` command reports virtual memory statistics.

```
tyralyn@tyralyn-laptop ~ $ vmstat
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 0  0      0 127480 204852 4151320    0    0   158   105  202  516  7  2 83  7  0
```

* **r**: number of runnable (running or waiting for runtime) processes
* **b**: number of processes in uninterruptible sleep
* **swpd**: amount of virtual memory used
* **free**: amount of idle memory
* **buff**: amount of memory used as buffers
* **cache**: amount of memory used as cache
* **si**: amount of memory swapped in from disk
* **so**: amount of memory swapped to disk
* **bi**: blocks received from a block device
* **bo**: blocks sent to a block device
* **in**: number of interrupts per second
* **cs**: number of context switches per second
* **us**: % time spent in userspace code
* **sy**: % time spent in kernel code
* **id**: % time spent idle
* **wa**: % time spent waiting for I/O
* **st**: % time stolen from a virtual machine

### Who is logged in on this machine?

The `w` command shows who is logged in and what they are doing:
```
tyralyn@tyralyn-laptop ~ $ w
 17:03:58 up  3:44,  3 users,  load average: 0.50, 0.58, 0.64
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
tyralyn  tty8     :0               13:20    3:44m  9:15   0.11s /sbin/upstart --user
tyralyn  pts/2    :0.0             13:27    2:15m  0.19s  0.19s -bash
tyralyn  pts/5    :0.0             13:22    5.00s  0.58s  0.02s w
```

To get users connect time: `ac`

To get info about previously executed commands: `lastcomm`

To enable/disable process accounting: `accton`

To summarize accounting info: `sa`

### How long does it take to run a command?

The `time` command:

```
time -v host www.cyberciti.biz

time -v ls
```

## Filesystems

### How to repair a filesystem?

To check and repair filesystems, the `fsck` (filesystem check) command can help:
```
fsck Fs-Name-Here
fsck /dev/xyz
fsck /home
fsck.ext3 /dev/hdc1
fsck.ext2 /dev/flash/device/name
```

`fsck` can take device names, mount points, ext2 labels, UUID specifiers 

This only works on unmounted filesystems, so take the system down to runlevel 1:
```
init 1
```

Unmount the filesystem:
```
umount /home
```

Run `fsck` on the partition:
```
fsck -t ext3 /dev/sda23
```

### How to debug a filesystem?

`debugfs` can be used to debug a filesystem.

### How to get info on a partition?
```
fdisk -l
```

## Memory

### Where to find info on memory?

The `/proc/meminfo` file reports stats on memory usage on Linux:

```
tyralyn@tyralyn-laptop ~ $ cat /proc/meminfo
MemTotal:        8031804 kB
MemFree:          170560 kB
MemAvailable:    3556672 kB
Buffers:          234012 kB
Cached:          3298300 kB
SwapCached:          232 kB
Active:          4612672 kB
Inactive:        2386132 kB
Active(anon):    3091176 kB
Inactive(anon):   908872 kB
Active(file):    1521496 kB
Inactive(file):  1477260 kB
Unevictable:         608 kB
Mlocked:             608 kB
SwapTotal:      16776700 kB
SwapFree:       16773180 kB
Dirty:               152 kB
Writeback:             0 kB
AnonPages:       3466932 kB
Mapped:           516312 kB
Shmem:            533556 kB
Slab:             678244 kB
SReclaimable:     429536 kB
SUnreclaim:       248708 kB
KernelStack:       18224 kB
PageTables:        88464 kB
NFS_Unstable:          0 kB
Bounce:                0 kB
WritebackTmp:          0 kB
CommitLimit:    20792600 kB
Committed_AS:   15678284 kB
VmallocTotal:   34359738367 kB
VmallocUsed:           0 kB
VmallocChunk:          0 kB
HardwareCorrupted:     0 kB
AnonHugePages:    684032 kB
CmaTotal:              0 kB
CmaFree:               0 kB
HugePages_Total:       0
HugePages_Free:        0
HugePages_Rsvd:        0
HugePages_Surp:        0
Hugepagesize:       2048 kB
DirectMap4k:      366992 kB
DirectMap2M:     7878656 kB
DirectMap1G:           0 kB
```


### How much memory is free? 

The `free` command:

```
tyralyn@tyralyn-laptop ~ $ free -h
              total        used        free      shared  buff/cache   available
Mem:           7.7G        3.5G        150M        532M        4.0G        3.4G
Swap:           15G        3.4M         15G

```

* **shared**: memory mostly used by tmpfs
* **buffers**: memory used by kernel buffers
* **cache**: memory used by the page cache and slabs
* **buff/cache**: sum of buffers and cache

`vmstat` includes some memory info (free, buffered, cache, swap).

`top` includes percent memory usage per process.

`/proc/meminfo` contains info on memory:
```
grep -E --color 'Mem|Cache|Swap' /proc/meminfo
```

### How much memory is a process using?

`pmap` reports the memory map of a process:
```
pmap -d PID
```

### What is swap?

Swap is a memory management scheme in which any process can be swapped from main to secondary emory so that the main memory can be available for other processes. In an OS, swapping is done to access data present in the hard disk and bring it to RAM so that applications can use it. Swapping is done when the data is not in RAM to bring it to RAM.

* **Swap-out**: removing a process from RAM and adding it to the hard disk
* **Swap-in**: removing a program from hard disk and putting it back into main memory, or RAM

#### Why is swap important?

Long-running linux systems have a lot of idle processes, each with anonymous (not file-backed) data. Putting that data out to disk means that the kernel can use the RAM better, such as to page cache, by swapping. Without swap, precious RAM is wasted on processes that you don't care about.

Kernel should begin swapping out before RAM runs out. If a system is slow due to swap, it means you don't have enough RAM to hold all the data you do care about, and stuff you need in RAM is being swapped out.


## Disk 

### How much disk space is free?

`df` provides info on free disk space.

To get basic human-readable info about disk usage, use `df -h`:

```
tyralyn@tyralyn-laptop ~/src/fafo $ df -h
Filesystem              Size  Used Avail Use% Mounted on
udev                    3.9G     0  3.9G   0% /dev
tmpfs                   785M  9.4M  775M   2% /run
/dev/sda8               246G  8.5G  225G   4% /
tmpfs                   3.9G  151M  3.7G   4% /dev/shm
tmpfs                   5.0M  4.0K  5.0M   1% /run/lock
tmpfs                   3.9G     0  3.9G   0% /sys/fs/cgroup
/dev/sda10              414G  6.8G  386G   2% /home
cgmfs                   100K     0  100K   0% /run/cgmanager/fs
tmpfs                   785M   36K  785M   1% /run/user/1000
/home/tyralyn/.Private  414G  6.8G  386G   2% /home/tyralyn
```

To get info on inode usage, use `df -i`:

```
tyralyn@tyralyn-laptop ~/src/fafo $ df -i
Filesystem               Inodes  IUsed    IFree IUse% Mounted on
udev                     998639    589   998050    1% /dev
tmpfs                   1003975    886  1003089    1% /run
/dev/sda8              16384000 248153 16135847    2% /
tmpfs                   1003975    156  1003819    1% /dev/shm
tmpfs                   1003975      5  1003970    1% /run/lock
tmpfs                   1003975     18  1003957    1% /sys/fs/cgroup
/dev/sda10             27525120 139735 27385385    1% /home
cgmfs                   1003975     14  1003961    1% /run/cgmanager/fs
tmpfs                   1003975     23  1003952    1% /run/user/1000
/home/tyralyn/.Private 27525120 139735 27385385    1% /home/tyralyn
```

### What files are using the most disk?

To get the top consumptive files, use the `du` command with `sort` and `tail`.

```
tyralyn@tyralyn-laptop ~ $ du -ch /home/tyralyn | sort -h | tail -n 30
man420M	/home/tyralyn/src/RustOS
429M	/home/tyralyn/src
433M	/home/tyralyn/.config/google-chrome/Profile 1/File System/002
433M	/home/tyralyn/.config/google-chrome/Profile 1/File System/002/p
434M	/home/tyralyn/.config/google-chrome/Profile 1/File System
443M	/home/tyralyn/.cache/mozilla/firefox/mwad0hks.default/cache2/entries
444M	/home/tyralyn/.cache/mozilla/firefox/mwad0hks.default/cache2
485M	/home/tyralyn/.cache/mozilla
485M	/home/tyralyn/.cache/mozilla/firefox
485M	/home/tyralyn/.cache/mozilla/firefox/mwad0hks.default
493M	/home/tyralyn/opt/rust/rust-docs/share/doc/rust/html/libc
607M	/home/tyralyn/opt/rust/rust-docs
607M	/home/tyralyn/opt/rust/rust-docs/share
607M	/home/tyralyn/opt/rust/rust-docs/share/doc
607M	/home/tyralyn/opt/rust/rust-docs/share/doc/rust
607M	/home/tyralyn/opt/rust/rust-docs/share/doc/rust/html
635M	/home/tyralyn/.cache/google-chrome/Profile 1/Cache
834M	/home/tyralyn/opt
834M	/home/tyralyn/opt/rust
851M	/home/tyralyn/Downloads
877M	/home/tyralyn/.cache/google-chrome/Profile 1
878M	/home/tyralyn/.cache/google-chrome
921M	/home/tyralyn/.config/google-chrome/Profile 1
1021M	/home/tyralyn/.config/google-chrome
1.1G	/home/tyralyn/applications
1.1G	/home/tyralyn/applications/clion-2018.2.5
1.1G	/home/tyralyn/.config
1.4G	/home/tyralyn/.cache
6.4G	/home/tyralyn
6.4G	total

```

```
du -a /ftpusers/tmp | sort -n -r | head -n 10
du -cks * | sort -rn | head
# check for the whole disk #
du -cks / | sort -rn | head
```

### What to do if disk is full?

Compress uncompressed files like logs:
```
gzip /ftpusers/tmp/*.log
bzip2 /ftpusers/tmp/large.file.name
``` 

Delete unwanted files:
```
rm -rf /ftpusers/tmp/*.bmp
```

Move files to other system or external hard disks:
```
rsync --remove-source-files -azv /ftpusers/tmp/*.mov /mnt/usbdisk/
rsync --remove-source-files -azv /ftpusers/tmp/*.mov server2:/path/to/dest/dir/
```

Truncate a file (see next section).

Check for deleted-but-open files:
```
## Works on Linux/Unix/OSX/BSD etc ##
lsof -nP | grep '(deleted)'
 
## Only works on Linux ##
find /proc/*/fd -ls | grep  '(deleted)'
```


### What if the culprit is one big file being written to?

The `truncate` command can help -- this will truncate the file to 0 bytes and still allow other processes to use it (because deleting it might not be a good idea if processes still expect it to be open).

```
truncate -s0 BIG_LOG.log
```

#### What if processes are still holding onto the file?

Sometimes, if you delete a file, the space will still show up as being used because processes are still holding onto the file descriptor of the deleted file. it doesn't get freed until the file is stopped. 

`lsof` **l**i**s**ts **o**pen **f**iles:

```
lsof | grep deleted | grep OLD_FILENAME
```

Then, you can `kill` the process. 

### What if a system is in read-only mode?

Check if in read-only mode with the `mount` command:
```
mount | grep '/ftpusers'
```

To fix, remount the fs in read-write mode:
```
mount -o remount,rw /ftpusers/tmp
```

Sometimes the Linux fs will enter read-only mode if there are disk or filesystem problems. Check disk health with `smartctl`:


### Disk I/O

#### What causes disk I/O issues?

* **Storage complexity**: software-defined or virtual storage layers over underlying physical storage might not be able to read and write as fast as physical storage can.
* **Application bottlenecks**: if multiple busy applications use the same datastore.
* **RAID configuration**: this is when you have multiple disks being treated at one. The device of software that handles this configuration/management might have problems.
* **Poor storage design, IO response time...** idk

#### What metrics are used to analyze disk I/O performance?

* read request rate
* write request rate
* total bytes read, byte read rate
* total bytes writte, byte write rate
* requests waiting in queue

#### How can I fix disk I/O issues?

**Software fixes**:

* use separate virtual and physical hard disks
* install the host OS onto a different disk than the VMs
* optimize hard drives by implementing disk partitioning in the guest and host OSes
* investigate whether the current RAID type/configuration is optimal
* turn on Direct Memory Access

**Hardware fixes**:

* upgrade hard drives to SSDs or faster spinning disk
* divide application load between hard disks to better cope with IO
* upgrade to larget in-memory cache so that direct r/w from filesustem will be less frequent

#### How can I get disk I/O stats?

`iostat` or `vmstat` can give overall/basic disk I/O info.

The `iotop` command displays dynamic I/O info for the system overall and for processes (where applicable):

* Disk read/write, swap
* Thread ID and priority of the process and the command

To display accumulated figures instead of bandwidth, use the `-a` flag.


## Processes

### What are all the Linux processes running right now?

#### `/proc` directory

Every time the system runs a program, the kernel starts a process. All currently-running processes in the system have a directory in the `/proc` filesystem.

```
ls /proc
```

Thins in `/proc` that might be useful include:

* **buddyinfo**: info on memory fragmentation
* **cgroups**: linux lets procs be grouped together, info on this and resource config for these groups
* **cmdline**: parameters passed to kernel at boot time
* **cpuinfo**
* **crypto**: ciphers uses for crypto by kernel
* **devices**: character and block devices that r configured
* **dma**: Direct Memory Access channels
* **execdomains**: execution domains 
* **fb**: frame buffer devices
* **filesystems**: list of fs types supported by kernel
* **interrupts**: different kinds of interrupts and their handlers
* **iomem**: current map of system memory for each physical device
* **ioports**: list of currently registered port regions used for input or output communication with a devcice
* **info**: 
* **info**: 
* **info**: 
* **info**: 
* **info**: 
* **info**: 
* **info**: 
* **info**: 


#### dynamic view:`top`

The `top` command provides dynamic info (memory, cpu, swap) for currently running processes.

In the window, you can do different stuff via keypress:

* Get the help menu: 'h'
* Sort by PID: `M` and `T` 
* Sort by memory usage: `M` and `P`
* Sort by running time: `M` and `T`
* Sort by CPU utilization: `Shift` and `P`
* Highlight the running process: `Z`
* Get the absolute paths of processes: `C`
* Set refresh interval: `d`
* Kill a process: `k` (kills top process unless you specify a PID)
* Renice (change priority) of a proces: `r`
* See CPU cores: `1`
* Show only idle processes: `i`

To save top command results to a file:
```
top -n 1 -b > top-output.txt
```

#### `ps`

The `ps` command gives info on processes:

```
tyralyn@tyralyn-laptop ~ $ ps -A
  PID TTY          TIME CMD
    1 ?        00:00:01 systemd
    2 ?        00:00:00 kthreadd
    3 ?        00:00:00 ksoftirqd/0

...
```


```
tyralyn@tyralyn-laptop ~ $ ps axu
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.0 119844  5988 ?        Ss   13:19   0:01 /sbin/init splash
root         2  0.0  0.0      0     0 ?        S    13:19   0:00 [kthreadd]
root         3  0.0  0.0      0     0 ?        S    13:19   0:00 [ksoftirqd/0]

...
```

### How to find a process's ID?

```
pidof chrome

ps aux | grep chrome

pgrep chrome
```

### How to find a process' name from PID?

```
ps -p 2523 -o comm=
```

### What else can `ps` do?

To display a process by user ID:
``` 
ps -fU tyralyn
```

To display by PID:
```
ps -fp 1178

ps -fp 2226,1154,1146
```

To display processes belonging to PPID (parent process ID):
```
ps -f --ppid 1154
```

To display process trees:
```
ps -e --forest

ps -f --forest -C sshd
```

To print all threads (**L**ight**W**eight **P**rocesses) of a process:
```
ps -fL -C httpd
```

To see execution time of a process:
```
ps -eo comm,etime,user | grep httpd
```

To find top running processes by highest memory and CPU usage:
```
ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%mem | head

$ ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%cpu | head
```

To find the processes for the current shell:
```
tyralyn@tyralyn-laptop ~ $ ps
  PID TTY          TIME CMD
 2844 pts/5    00:00:00 bash
13533 pts/5    00:00:00 ps
```

To perform real-time process monitoring:
```
watch -n 1 'ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%mem | head'
```

### How to get status (running or not) of a process?

```
service chrome status 
systemctl status chrome
```

```
pgrep chrome
ps -aux | grep chrome
```

### How to kill a process?

The `kill` command allows sending a specific signal or kill command to a process. Signals include `SIGHUP` (1), `SIGKILL` (9), and SIGTERM (15):
```
kill -9 3139

kill -SIGTERM 3139
```

To kill a process (and its children) by process name:
```
killall chrome

pkill chrome
```


## CPU

To display CPU info:
```
cat /proc/cpuinfo
```

## Network 

`netstat` shows network connections, routing tables, interface stats, masq connections, and multicast memberships.

`ss` dumps socket stats.

`iptraf` gets realtime stats.

`tcpdump` dumps TCP traffic info.

`iftop` shows network interface info dynamically.

`strace` traces linux system calls and signals

### What are the network interface settings?

```
tyralyn@tyralyn-laptop ~ $ ifconfig
enp1s0    Link encap:Ethernet  HWaddr c8:5b:76:6a:99:47  
          UP BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:11951 errors:0 dropped:0 overruns:0 frame:0
          TX packets:11951 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1 
          RX bytes:1315107 (1.3 MB)  TX bytes:1315107 (1.3 MB)

wlp2s0    Link encap:Ethernet  HWaddr 84:ef:18:2b:cd:61  
          inet addr:192.168.1.65  Bcast:192.168.1.255  Mask:255.255.255.0
          inet6 addr: 2600:1700:4384:b020::49/128 Scope:Global
          inet6 addr: 2600:1700:4384:b020:9542:3d05:106b:de99/64 Scope:Global
          inet6 addr: fe80::e415:cce0:bdfc:52fe/64 Scope:Link
          inet6 addr: 2600:1700:4384:b020:2c49:749f:1f26:e1ef/64 Scope:Global
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:449635 errors:0 dropped:0 overruns:0 frame:0
          TX packets:163334 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 

```

## Boot

### What happens during bootup?

**BIOS POST**: basic IO and hardware checks. Then try to find boot sectors on any attached bootable devices (disk, USBs, CD-ROMs). For disks, the **M**aster **B**oot **R**ecord (MBR) is the sector at the very beginning.

The boot sector with a valid boot record is loaded into RAM, and control is transferred there. This is the first part of the boot loader.

**GRUB**: **Gr**and **U**nified **B**ootloader is the primary bootloader for most linux distros. This makes the computer smart enough to find the OS kernel and load it into memory and get it running.