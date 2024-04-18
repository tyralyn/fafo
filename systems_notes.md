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

### What users are logged into the machine?

To get who is logged in: `w`


### What are the most recent system messages?

`dmesg` shows system messages. OOMs and dropped TCP requests could cause performance issues.

```
$ dmesg | tail
[1880957.563150] perl invoked oom-killer: gfp_mask=0x280da, order=0, oom_score_adj=0
[...]
[1880957.563400] Out of memory: Kill process 18694 (perl) score 246 or sacrifice child
[1880957.563408] Killed process 18694 (perl) total-vm:1972392kB, anon-rss:1953348kB, file-rss:0kB
[2320864.954447] TCP: Possible SYN flooding on port 7001. Dropping request.  Check SNMP counters.
```

### How long has the system been running?

To get how long system has been running: `uptime`
```
➜  ~ uptime
16:58  up 27 days,  8:49, 5 users, load averages: 2.94 3.13 2.92
```

These load averages show the average number of processes wanting to run on CPU and/or are blocked on uninterruptible IO, over the last one minute, five minutes, and fifteen minutes. If the numbers appear in descending order, it indicates a recent increase. If the numbers are very large (e.g. 30?), this could indicate high CPU demand.


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

Nice command for extended statistics: `iostat -xz 1`:

```
$ iostat -xz 1
Linux 3.13.0-49-generic (titanclusters-xxxxx)  07/14/2015  _x86_64_ (32 CPU)

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
          73.96    0.00    3.73    0.03    0.06   22.21

Device:   rrqm/s   wrqm/s     r/s     w/s    rkB/s    wkB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util
xvda        0.00     0.23    0.21    0.18     4.52     2.08    34.37     0.00    9.98   13.80    5.42   2.44   0.09
xvdb        0.01     0.00    1.02    8.94   127.97   598.53   145.79     0.00    0.43    1.78    0.28   0.25   0.25
xvdc        0.01     0.00    1.02    8.86   127.79   595.94   146.50     0.00    0.45    1.82    0.30   0.27   0.26
dm-0        0.00     0.00    0.69    2.32    10.47    31.69    28.01     0.01    3.23    0.71    3.98   0.13   0.04
dm-1        0.00     0.00    0.00    0.94     0.01     3.78     8.00     0.33  345.84    0.04  346.81   0.01   0.00
dm-2        0.00     0.00    0.09    0.07     1.35     0.36    22.50     0.00    2.55    0.23    5.62   1.78   0.03
[...]
^C
```

Notable columns:

* Read and write rates help characterize workload -- a performance problem could be caused by excessive load.
* **await**: this is the average I/O time in milliseconds, including both queueing time and service time. Large awai time could indicate device saturation or problems.
* **avgqu-sz**: this is the average number of requests issued to the device. While values > 1 could indicate saturation, devices generally operate on requests in parallel, especially if they are virtual devices with front multiple backend disks. Basically, this could maybe indicate device saturation but doesn't necessarily. Storage is sometimes a logical disk frontending many backend disks, which might not be saturated. 
* **%util**: busy percentage, showing the amount of time per second that a device is busy. >60% typically leads to poor performance, and values close to 100% usually indicate saturation.

Poor disk I/O performance is not necessarily an application issue -- a lot of stuff happens behind the scenes (e.g. read-aheads when reading and buffering writes) to do I/O asynchronously so that application doesn't block on I/O and suffer latency directly.

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

Notable columns:

* **r**: this is the number of processrs running and waiting. (Unlike load averages, this does not include processess waiting on I/O). An `r` value greater than CPU count shows CPU saturation.
* **free**: is there free memory?
* **si**, **so**: swap-in and swap-out. If these are > 0, then you are out of memory.
* **us**, **sy**, **id**, **wa**, **st**: these are average CPU time spent in userspace code, system (kernel) code, idle, waiting for I/O, and stolen. user + system time means that the CPUs are busy. Constant I/O wait could indicate disk bottleneck, causing CPUs to idle because tasks are waiting on I/O. Over 20% CPU time spent on system/kernel code might indicate the kernel is processing I/O inefficiently (I/O uses system time). High userspace time points to high application level usage.

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

### How can I make my system more secure?

To secure your system:

* two-factor authentication
* VPNs
* IDS (**I**ntrusion **D**etection **S**ystems)

To increase network security:

* firewalls
* antivirus software
* secure configurations

## Kernel

### What are kernel and user space?

Kernel space is reserved for running privileged kernel stuff. Userspace is where applications run. Drivers run in both depending.

## Filesystems

### What is an inode?

An inode is a data structure that contains info on a file: 

* size
* device ID
* user/group IDs
* file mode and access privileges
* creation and modification timestamps
* counter of hard links to the file
* pointers to blocks storing file contents

When a file is created, a filename and inode are assigned to the file. When a file is accessed, the filename's corresponding inode number is retrieved. Inode numbers and their respective indoes are kept in the inode table. Multiple filenames can correspond to a file (hardlinks), so filenames are not stored in inodes.

### How can I get inode numbers?

To show inodes generally:

```
ls -i

df -i
```

To find a specific file's inode number:
```
stat $FILENAME
```

To find a file by inode number:
```
find . -inum 1448239
```

### What is the difference between an inode and a file descriptor?

An inode represents a file, whereas a file descriptor represents a ticket to access the file, with limited permission and a time window

Inodes are data structures that hold info on the file itself, like a complex identifier for a file. They are artifacts of the filesystem and how the filesystem does stuff. They are a resource, just like memory and disk space. 

A file descripter is an opaque identifier to an open file, from the kernel's point of view. 'File' here is not the same as described above in the context of inodes. A file represents a stream. 

File descriptors and inodes are not related, unless something uses them internally to refer to the same things (e.g. a filesystem driver -- filesystem dictates what goes in an inode, and when operating on files, the kernel would refer to open files with a file descriptor).


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

### What is a memory leak? ??

A memory leak is failure to release unreachable memory, which can no longer be allocated again by any process during execution of the allocating process. This can be cured by garbage collection.

A memory leak is failure to release reachable memory that is no longer needed for the program to function correctly. This is super hard to detect by automate

### What is swap?

Swap is a memory management scheme in which any process can be swapped from main to secondary emory so that the main memory can be available for other processes. In an OS, swapping is done to access data present in the hard disk and bring it to RAM so that applications can use it. Swapping is done when the data is not in RAM to bring it to RAM.

* **Swap-out**: removing a process from RAM and adding it to the hard disk
* **Swap-in**: removing a program from hard disk and putting it back into main memory, or RAM

#### Why is swap important?

Long-running linux systems have a lot of idle processes, each with anonymous (not file-backed) data. Putting that data out to disk means that the kernel can use the RAM better, such as to page cache, by swapping. Without swap, precious RAM is wasted on processes that you don't care about.

Kernel should begin swapping out before RAM runs out. If a system is slow due to swap, it means you don't have enough RAM to hold all the data you do care about, and stuff you need in RAM is being swapped out.


### How to find out whether an OOM happened?

This can be caused by the sustem running out of memory. This would get logged in various places.

`dmesg` shows system messages:
```
$ dmesg | tail
[1880957.563150] perl invoked oom-killer: gfp_mask=0x280da, order=0, oom_score_adj=0
[...]
[1880957.563400] Out of memory: Kill process 18694 (perl) score 246 or sacrifice child
[1880957.563408] Killed process 18694 (perl) total-vm:1972392kB, anon-rss:1953348kB, file-rss:0kB
[2320864.954447] TCP: Possible SYN flooding on port 7001. Dropping request.  Check SNMP counters.
```

`/var/log` would log this too:
```sudo grep -i -r 'out of memory' /var/log/```

If you have the PID, you can get the chance that the process would get axed by the OOM killer:
```
cat /proc/5872/oom_score
```

### How do I fix overuse of memory?

**Disable memory overcommit**: Linux kernel often allows processes to request more memory than is free to improve utilisation, based on a heuristic that processes never use all the memory they request. This can be disabled with `sysctl`.

* **Add more memory to server**: add more memory devices.

* **Empty page cache**: disk caching makes the system faster, but consumes memory. If Linuxed was too aggressive in caching to memory, there's less free memory available for applications to use, which would cause swap in and swap out.

### What about cache misses?

Cache miss means that data's not in cache memory and has to go to disk.

To catch cache misses, use a perf tool like `perf` or `cachegrind`.

To reduce cache misses:

* set or change expiry on cache lifespan
* inrease size of cache or RAM
* reconfigure cache policy based on how it's used (e.g. FIFO, LIFO, LRU, MRU)

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

#### How can memory affect disk I/O?

```
$ free -m
             total       used       free     shared    buffers     cached
Mem:        245998      24545     221453         83         59        541
-/+ buffers/cache:      23944     222053
Swap:            0          0          0
```

* **buffers**: indicates the buffer cache, used for block device I/O
* **cached**: indicates the page cache, used for file systems

If these values are near-zero, then block devices (which are memory devices, because block devices are defined as random-access and are usually higher-speed) and filesystem caches are not being used, which can lead to higher disk I/O. Linux uses free memory for caches, but can reclaim it.


## Processes

### What are all the Linux processes running right now?

#### `/proc` directory

Every time the system runs a program, the kernel starts a process. All currently-running processes in the system have a directory in the `/proc` filesystem. This is technically a pseudo-file system -- it doesn't contain `real` files but runtime system info. A lot of system utilities are simply calls to files in this directory.

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

### What is each processor doing?

To get activities (time breakdown) of each processor (CPU): `mpstat -P ALL`

```
$ mpstat -P ALL 1
Linux 3.13.0-49-generic (titanclusters-xxxxx)  07/14/2015  _x86_64_ (32 CPU)

07:38:49 PM  CPU   %usr  %nice   %sys %iowait   %irq  %soft  %steal  %guest  %gnice  %idle
07:38:50 PM  all  98.47   0.00   0.75    0.00   0.00   0.00    0.00    0.00    0.00   0.78
07:38:50 PM    0  96.04   0.00   2.97    0.00   0.00   0.00    0.00    0.00    0.00   0.99
07:38:50 PM    1  97.00   0.00   1.00    0.00   0.00   0.00    0.00    0.00    0.00   2.00
07:38:50 PM    2  98.00   0.00   1.00    0.00   0.00   0.00    0.00    0.00    0.00   1.00
07:38:50 PM    3  96.97   0.00   0.00    0.00   0.00   0.00    0.00    0.00    0.00   3.03
[...]
```

An imbalance is notable; a single hot CPU could be evidence of a single-threaded application.

`pidstat` is similar to `top` but with rolling summaries instead of screen-clears. 

```
$ pidstat 1
Linux 3.13.0-49-generic (titanclusters-xxxxx)  07/14/2015    _x86_64_    (32 CPU)

07:41:02 PM   UID       PID    %usr %system  %guest    %CPU   CPU  Command
07:41:03 PM     0         9    0.00    0.94    0.00    0.94     1  rcuos/0
07:41:03 PM     0      4214    5.66    5.66    0.00   11.32    15  mesos-slave
07:41:03 PM     0      4354    0.94    0.94    0.00    1.89     8  java
07:41:03 PM     0      6521 1596.23    1.89    0.00 1598.11    27  java
07:41:03 PM     0      6564 1571.70    7.55    0.00 1579.25    28  java
07:41:03 PM 60004     60154    0.94    4.72    0.00    5.66     9  pidstat

07:41:03 PM   UID       PID    %usr %system  %guest    %CPU   CPU  Command
07:41:04 PM     0      4214    6.00    2.00    0.00    8.00    15  mesos-slave
07:41:04 PM     0      6521 1590.00    1.00    0.00 1591.00    27  java
07:41:04 PM     0      6564 1573.00   10.00    0.00 1583.00    28  java
07:41:04 PM   108      6718    1.00    0.00    0.00    1.00     0  snmp-pass
07:41:04 PM 60004     60154    1.00    4.00    0.00    5.00     9  pidstat
```

Here, java is using almost 1600% total CPU (of all CPUs), indicating that it is processing almost 16 CPUs. 

### WHat does CPU usage mean?

Roughly:

* 0-4%: kernel is idle and not doing anything
* 5-10%: kernel is doing some work but not a lot
* 11-20%: kernel is doing a lot of work and started to get bogged down, maybe encountering performance issues
* 21-100%: kernel is under heavy load and having a hard time keeping up

## Network (general)

`netstat` shows network connections, routing tables, interface stats, masq connections, and multicast memberships.

`ss` dumps socket stats.

`iptraf` gets realtime stats.

`tcpdump` dumps TCP traffic info.

`iftop` shows network interface info dynamically.

`strace` traces linux system calls and signals

### What is my IP address?

```
ip addr
ifconfig -a
```

To get your default gateway (your router's) IP:
```
route -r
```

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

### What kind of throughput are the network interfaces having?

The `sar` command collects and reports miscellaneous system activity. It has to be enabled for monitoring.

```
$ sar -n DEV 1
Linux 3.13.0-49-generic (titanclusters-xxxxx)  07/14/2015     _x86_64_    (32 CPU)

12:16:48 AM     IFACE   rxpck/s   txpck/s    rxkB/s    txkB/s   rxcmp/s   txcmp/s  rxmcst/s   %ifutil
12:16:49 AM      eth0  18763.00   5032.00  20686.42    478.30      0.00      0.00      0.00      0.00
12:16:49 AM        lo     14.00     14.00      1.36      1.36      0.00      0.00      0.00      0.00
12:16:49 AM   docker0      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00

12:16:49 AM     IFACE   rxpck/s   txpck/s    rxkB/s    txkB/s   rxcmp/s   txcmp/s  rxmcst/s   %ifutil
12:16:50 AM      eth0  19763.00   5101.00  21999.10    482.56      0.00      0.00      0.00      0.00
12:16:50 AM        lo     20.00     20.00      3.25      3.25      0.00      0.00      0.00      0.00
12:16:50 AM   docker0      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00
^C
```

It can be used to check network interface throughput.

* **rxkB/s, txkB/s**: measure workload
* **%ifutil**: shows device utilization, but is kind of hard to get right.

```
$ sar -n TCP,ETCP 1
Linux 3.13.0-49-generic (titanclusters-xxxxx)  07/14/2015    _x86_64_    (32 CPU)

12:17:19 AM  active/s passive/s    iseg/s    oseg/s
12:17:20 AM      1.00      0.00  10233.00  18846.00

12:17:19 AM  atmptf/s  estres/s retrans/s isegerr/s   orsts/s
12:17:20 AM      0.00      0.00      0.00      0.00      0.00

12:17:20 AM  active/s passive/s    iseg/s    oseg/s
12:17:21 AM      1.00      0.00   8359.00   6039.00

12:17:20 AM  atmptf/s  estres/s retrans/s isegerr/s   orsts/s
12:17:21 AM      0.00      0.00      0.00      0.00      0.00
^C
```

`sar` with TCP provides some TCP metrics:

* **active/s**: locally-initiated TCP connections per second
* **passive/s**: remotely-initiated TCP connections per second
* **retrans/s**: number of TCP retransmits per second

Active and passive TCP counts can serve roughly as a measure of server loaded -- number of new upstream and downstream connections. Retransmits can indicate network or server issues -- bad internet or the server being overloaded and dropping packets.

### How to check network status?

This can be done with `ifconfig` in general:

* **Physical layer**: `ip link show <interface>` checks whether network interface is up or down, `ethtool eth0` queries settings of eth device like network speed / packet drop etc.
* **Data link layer**: `ip neighbor show` shows the kernel's current neighbor table, `arp` lists current contents of ARP cache
* **Network/Internet layer**: `ip address show` or `ifconfig -a` show IP addresses of the network interfaces, `ping` or `traceroute` a website, `ip route show` shows the route table, `nslookup` or `dig` does DNS lookup for a website

### How to check a remote port on a listening machine is open?

```
nc -zvw10 192.168.0.1 22

nmap 192.168.0.1 -p 22

telnet 192.168.0.1 22
```

### How to transfer data to or from a server?

`curl` is supported for HTTP, FTP, IMAP, POP3, SCP, SMTP, TFTP, TELNET, LDAP, and FILE protocols.

```
curl http://site.{one, two, three}.comcurl -o hello.zip ftp://speedtest.tele2.net/1MB.zip
```

### Troubleshooting a slow network

Causes of a slow network:

* **Hardware errors**: broken ethernet adapter or network configuration, or physical cable problems
* **IP fragmentation**: when the receiving system can't contain a full datagram due to small maximum transit unit (MTU), breaking IP packet down. Intermediate routers can fragment packets, but not reassemble them because the fragments can take different routes. By default, TCP won't fragment IP packets -- istead, it will listen for ICMP packets indicating that there is MTU problems, and then will decrease packet size
* **TCP retransmission**: this means there's something wrong between endpoints

Triage strategies:

* Use `dmesg` to see what is going on in system messages.
* Check the network as a whole with `ping` or `traceroute`
* Look at interfaces
* Look at open/closed/failed connections with `netstat`
* Inspect packets with `tcpdump`

Miscellaneous solving strategies:

* Restart network interfaces (`ifdown eth0 && ifup eth0`)
* Check for IP address conflict (if two or more devices on the same network are trying to use the same IP address)
* Troubleshoot TCP issues with `tcpdump`
* Change the TCP window in the kernel if it is too small
* Change MTU size of packets r getting lost


### What network connections are open?

`netstat` (and its replacement, `ss`) prints info on the networking subsystem. Connections here mean listeners.

To get all connections:
```
netstat -anpl
```

To get TCP or UDP connections:
```
ss -t

ss -u
```

### Troubleshooting an SSH connection

SSH connection:
```
ssh [options] [user@]hostname [command]
```

Verify the address (e.g. ping it to see if it exists).

Check that the network allows SSH over that port -- some public networks block 22 or custom SSH ports. Try to establish a telnet session with `telnet server_address port_number`. 

Check whether client and server firewalls permit SSH.

Increase timeout value for SSH command.

### How can I check shared libraries/object dependencies of a binary?

To see object dependencies of binary `ls`: `ldd /bin/ls`

To find unused object dependencies: `ldd -u <file>`

To perform relocations and report any missing objects from binary: `ldd -d <file>`

To perform relocations and report any missing objects **and** functions from binary: `ldd -r <file>`

This can be useful if you need to know what dependencies are missing from binaries, as well as identifying and removing any unused dependencies

### What is DHCP?

DHCP is **D**ynamic **H**ost **C**onfiguration **P**rotocol. It emables networks to assign IP addresses dynamically (without a network administrator).

A device requests access to the network and needs an IP address. DHCP "leases" out IP addresses.

When DHCP fails, your machine instrad gets an APIPA address (within 169.254.0.1 to 169.254.255.254), which allows your machine to talk to others on the LAN even though DHCP isn't working.

DHCP servers receive requests for IP addresses and allocate them out.

### What is DNS?

DNS is **D**omain **N**ame **S**ystem, referred to as the phone book to the internet, mapping website names to IP addresses. It locates and translates domain names.

DNS servers receive queries about website names and responds with IP addresses.


### What is my DNS server's IP address?

`dig` (**D**omain **I**nformation **G**rouper):

```
dig howtouselinux.com
```

`nslookup`:

```
nslookup -query=a howtouselinux.com
```

The `/etc/resolv.conf` file also has this information:

```
cat /etc/resolv.conf
```

## IP

### What does the `ip` tool do?

To show info on network interfaces: `ip link`

To configure a link (set up or down): `ip link set eth 0 down`

To add an IP address to a network interface: `ip addr add 10.0.0.1/24 dev eth0`

To delete an IP address from a network interface: `ip addr del 10.0.0.1/24 dev eth0`


## TCP

TCP allows transmission of info in both directions.

### What are the TCP connection states?

For initiating connections:

* **SYN_SENT**: sender initiated connection process with receiver
* **SYN_RECEIVED**: receiver has receved a SYN from the sender
* **ESTABLISHED**: receiver has received SYN from the senter, sequence nums have been synchronized, and a connection established
* **LISTEN**: ready to listen 

For closing connections:

* **FIN_WAIT_1**: active close process has been initiated with a
* **TIMED_WAIT**: waiting for other side to acknowledge close process (controlled by timer) with an ACK
* **CLOSE_WAIT**: FIN has arrived from other side to begin closing
* **FIN_WAIT_2**: ACK for FIN has arrived
* **LAST_ACK**: last user input for terminating connection has been obtained, FIN statement can be sent
* **CLOSED**: 

### What is a failed connection attempt?

This is when the socket in SYN_RECV or SYN_SENT gets an unexpected traffic, e.g. a RCP reset, indicating that the other end is not listening.

### What is a bad segment?

This happens if an RFC 5691 Challenge Ack is sent, if the TCP header is too small, if the TCP is in the wrong place in the packet, or if there is a checksum error.

### How to capture TCP traffic?

To capture TCP traffic on all interfaces:
```
tcpdump -i any
```

To capture TCP traffic over 15 seconds:
```
tcpdump -G 15 -W 1 -w myfile -i eth0 'port 8080'
```

To capture specific protocols:
```
tcpdump -i interface ssh or dhcp

tcpdump -i interface UDP
```

and so on.

## IP

IP (Internet Protocol) is a set of rules for routing and addressing packets. 

### What is a subnet?

Subnetting segments the network in meaningful ways, making routing more efficient. It also limits IP address usage to within a few devices

Every computer has an IP address. A subnet mask identifies what IPs are in the same network and which must go through a router. Devices compare their IPs in their subnet mask to see if a destination address is local or not. This can keep internal traffic within a designated subnet, reducing congestion and network load.

A subnet mask of 255.255.255.0 ends up being 0b11111111111111111111111100000000, or /24. Anything on the first 24 bits is in the same subnet, and can be contacted directly. Others must go through the router.

Subnetting allows for more efficient use of finite IP address space, keeping backbone routers from having to know a fuckton of addresses if it can route by the first few numbers. Routers only care about networks, and not about individual hosts. This goes down and down into slightly smaller and smaller subnets to regions within networks.


Subnetting used to be done by class (e.g. A, B, C, D, E) with explicitly defined subnet mask lengths (e.g. /8, /16, etc). This is inefficient because no one is really using up all 16 million hosts in a /8 network. TCP/IP was amended to use CIDR (**C**lassless **I**nter-**D**omain **R**outing), allocating space on any address-bit boundary. This gave organizations more granular control of subnets, slowing IPV4 address exhaustion.

Example: a partner wants 10 public IP addresses that need to be routed through enough IP addresses for misc. security reasons. A /24 subnet has 254 usable IP addresses and would be too many. A /28 (14 usable IP addresses, 16 total) is better for this use case. One IP address is used for network, and one is for broadcast. One is assigned to the datacenter, and one to their security thing (ASA), leaving them 12 for use with NAT or to assign directly to hosts.

If they require 1 NATted address, assign a /30 (4 address + 2 reserver + 1 for datacenter + 1 for ASA). Breaking down network areas into virtual LANs with small subnets minimizes layer 2 broadcast traffic (broadcast domain will only broadcast to MAC addresses in a specified range).

Subnetting saves IP address *in comparison to subnet classes* by not having people allocate stupid big subnets. It might also force people to share IP addresses via NAT.

## Problems

## What is the difference between a crash and a panic?

Crashes occur when a trap occurs when an application tries accessing memory incorrectly. Panic occurs when an application kills/shuts itself down abruptly. Crashes are hardware or OS-initiated, while panics are initiated by an application calling `abort`. 

## What happens when you turn on a computer?

1. Booting
2. Startup

### Bootup

#### Boot stage 1

**BIOS POST**: basic IO and hardware checks. Then, (via BIOS interrupt) it tries to find boot sectors on any attached bootable devices (disks, USBs, CD-ROMs). In disks, a boot record would be stored in the **M**aster **B**oot **R**ecord (MBR), the sector comprising the very first 512-byte sector. This sector also contains the partition table, a 64-byte structure containing info on the division (partitions) of the HDD. 

Once a valid boot record is found, it is loaded into RAM and executed (transferring control there). This is technically considered to be the first stage of the boot loader.

**GRUB**: **Gr**and **U**nified **B**ootloader is the primary bootloader (bootstrap code)for most Linux distros, saved as an image file. It essentially makes the computer smart enough to find the OS kernel and load it into memory and get it running. It is very small, fitting into the aformentioned MBR, and therefore isn't smart enough to know stuff like filesystems. All it does is get to the next stage of booting.

#### Boot stage 1.5

The code/info needed for this stage is located between the boot record (MBR) and the first partition on the disk drive. For example, the MBR will start at sector 0, and the first partition would start in sector 63. The space between (62 512-byte sectors, totaling 31,744 bytes) would contain the `core.img` file. This file would contain a few common filesystem drivers (e.g. EXT) that the bootloader (GRUB) supports.

In this stage, the filesystem drivers in `core.img` get loaded so that the bootloader can  locate the `/boot` filesystem in order to proceed to the next stage.

#### Boot stage 2

While the previous stages were image files stored in predictable locations on the disk, at this point, GRUB has loaded the necessary filesystem drivers and knows where the `/boot/grub2` directory is. This directory contains runtime kernel modules that GRUB will use.

In this stage, GRUB finds a LINUX kernel (it is capable of picking between multiple kernels), loads it into RAM, and turns control over to the kernel.

Space is at a premium here in the `/boot` directory so kernels are stored in a self-extracting, compressed format. Once the kernel has extracted itself, it loads `systemd`, ending the boot process.

### Startup

At this point, the kernel and `systemd` are running.

`systemd` is a system daemon that does a lot of things, including setting up all other operating system stuff (e.g. mounting filesystems, starting and managing miscellaneous Linux services). This is an implementation of POSIX's `init` (POSIX is an interface definition for operating systems) and replaces the old-school SystemV `init`.

`/etc/fstab` file stores static config info on filesystems, such as mount points and options. `systemd` uses this to mount filesystems (besides the `/boot` directory, which it already knows about). 

`systemd` has a configuration file for itself, symlinked from `/etc/systemd/system/default.target`, that determines what state or target to boot the host into. This is set to a default value.

* **halt.target**: halts the system without shutting it down
* **poweroff.target / runlevel0.target**: halts the system and turns off the power
* **emergency.target**: single-user mode with no services or filesystems besides an emergency shell on the main console for interacting with the system
* **rescue.target / runlevel1.target**: a base system with mounted filesystems, some super basic services, and a rescue shell on the main console
* **runlevel2.target**: multiuser mode with all non-GUI services except for NFS (network filesharing)
* **multi-user.target / runlevel3.target**: all services running but only via CLI (no GUI)
* **runlevel4.target**: unused
* **graphical.target / runlevel5.target**: multiuser with a GUI
* **reboot.target / runlevel6.target**: reboot
* **default.target**: this is symlinked to either multi-user.target or graphical.target, `systemd` will always use this one

Each of these these targets has a config file listing its the dependencies needed to run the Linux host. `systemd` will start these dependencies.

## What happens when you type `ls` into the command prompt?

1. The shell reads your input using `getline()`, and tokenizes it (breaks it into individual works) with `strtok()`. 

2. The shell checks whether the first token is a shell alias (built-in function). If not, it checks the `PATH` for executable binaries corresponding to the first token.

3. The program is loaded into memory.

4. A system call `fork()` creates a child process as `ls`, getting the PID of the process in return.

5. The `ls` process executes the system call with `execve()`, that gives it a new address space (virtual memory space) to run with. The `ls` process starts running. Under the hood, the `ls` utility consults the underlying filesystem's inodes to read the directories and files on the disk.

6. When `ls` is done, it calls `_exit()` (with 0, denoting normal execution).

7. Kernel frees resources of the `ls` process.




## zombie 


















