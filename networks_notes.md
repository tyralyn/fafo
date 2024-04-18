# Networks

## Networks

### What is the OSI model?

* **Application**: high-level protocols for resource-sharing or remote file access
* **Presentation**: translation of data between networking service and application, including character encoding, data compression, and encryption/decryption. 
* **Session**: managing communication sessions (continuout exchange of info back and forth between two nodes)
* **Transport**: reliable transmission of data segments between points on a network, including segmentation, acknowledgement, and multiplexing
* **Network**: structuring and managing a multi-node network, including addressing, routing, and traffic control
* **Data-Link Layer**: transmission of data frames between two nodes connected by a physical layer
* **Physical**: transmission and reception of raw bit streams over a physical layer


### What is the TCP/IP model?

* **Application**: services, corresponds to OSI's Application, Presentation, and Session layers
* **Transport**: host-to-host, corresponds to OSI's Transport layer
* **Internet**: network, corresponds to OSI's network layer
* **Link**: corresponds to OSI's Data-Link layer and Physical layer

#### Some tricks to remember the TCP/IP stack

* **P**lease **D**o **N**ot **T**hrow **S**ausage **P**izza **A**way
* **A**ll **P**eople **S**eem **T**o **N**eed **D**ata **P**rocessing
* **P**lease **D**o **N**ot **T**ake **S**tupid **P**eople's **A**dvice

## What is the difference between TCP and UDP?

TCP is **T**ransmission **C**ontrol **P**rotocol. UDP is **U**ser **D**atagram **P**rotocol.
* While network traffic is sent by packets under the hood, TCP conceptually sends data as streams, while UDP sends datagrams.
* TCP sets up secure connections between sender and receiver, established and shut down via handshakes, before transferring data. UDP is connectionless.
* TCP is slow but complete, while UDP is fast but at risk of incomplete data.


TCP > UDP because:
* TCP is reliable -- if it doesn't receive acknowledgement of packets it sent, it resends them. UDP does not. 
* TCP guarantees delivery, while UDP does not.
* TCP sequences data, while UDP does not.
* TCP checks for data errors with thorough checksums, while UDP's error checking is more basic.
* TCP optimizes transfer rate based on the receiver's capabilities.
* Routers often drop UDP packets in favor of TCP packets.


UDP > TCP because:
* UDP supports broadcasting and multicasting, but TCP does not. 
* UDP packets are smaller.
* UDP is more efficient.
* UDP delivers data even if it is incomplete.
* TCP's handshake takes time, but UDP gets started faster.
* TCP has more overhead and uses more data than UDP.
* TCP is not suited for LAN and PAN networks.
* TCP slows down its transfer rate if it encounters congestion.


## What are some protocols in the TCP/IP stack layers?

**Application (Application + Presentation + Session)**
* **Over TCP**: HTTP, HTTP/TLS/SSL, NNTP, FTP, Telnet, SSH, POP3, IMAP4, SMTP
* **Over UDP**: DNS, TFTP, DHCP/BootP, SNP, NTP, Syslog

**Transport (Transport)**
* TCP
* UDP

**Internet (Network)**
* IP

**Link**
* Ethernet
* PPP Frame Relay
* MAC aaddresses
* ARP

* electrons, RF, light

## What is ARP?

ARP is **A**ddress **R**esolution **P**rotocol. It resolves IP addresses (which can change) to fixed hardware (MAC, link-layer) addreses and stores them in a dictionary. It is part of the IP protocol suite.

1. **Arrival**: when a packet arrives at a gateway (e.g. a router)
2. **Check**: the gateway machine asks the ARP program to find an IP address matching the IP specified in the packet.
3. **Specification**: the program looks it up and sends back the mapping.

Comouters joining a LAN get an IP address (either manually or via DHCP). All OSes in the network maintain an ARP cache. 

ARP is used by IP protocol when a  machine needs to send something. The machine checks whether the desination IP is on the same subnet at the source host. If so, ARP is used to get the destination's MAC address. If not, ARP is used to determine the hardware address of the default gatewau.


### What are some ARP vulnerabilities?

**ARP spoofing/poisoning**: the adversary sends fake ARP messages to a target LAN with the intent of linking their MAC with one of the network's legitimate IPs. The victim's data will get sent to the adversary.

This can cause man-in-the-middle (MTM) attack (where someone intercepts, relays, and alters messages between two parties), denial-of-service (DoS) attacks (where someone tries to overwhelm systems, servers, and networks to prevent users from accessing them), and session hijacking (where someone steals a user's session ID, takes over their web session, and masquerades as that user).

### What machines are ARP-locatable?

The `/etc/hosts` file:
```
more /etc/hosts
```

A system's ARP cache records ARP activity. The `arp` command can be used:
```
arp -a
```

### How to delete an ARP entry?

ARP caches have a timeout. To bypass this, manually delete the entry:

```
# ip neighbor show
192.168.122.170 dev eth0 lladdr 52:54:00:04:2c:5d REACHABLE
192.168.122.1 dev eth0 lladdr 52:54:00:11:23:84 REACHABLE

# ip neighbor delete 192.168.122.170 dev eth0

# ip neighbor show
192.168.122.1 dev eth0 lladdr 52:54:00:11:23:84 REACHABLE
```

## Can MAC addresses be spoofed?

While MAC addresses are usually assigned at the factory, some modern networks use VRRP (Virtual Router Redundancy Protocol), which uses generated MAC addresses.

## What is DHCP?

DHCP is **D**ynamic **H**ost **C**onfiguration **P**rotocol. It emables networks to assign IP addresses dynamically (without a network administrator) for some amount of time ("lease").

When DHCP fails, your machine instead gets an APIPA address (within 169.254.0.1 to 169.254.255.254), which allows your machine to talk to others on the LAN even though DHCP isn't working.

DHCP servers receive requests for IP addresses and allocate them out. The alternative is manually assigining an IP address (e.g. with `ifconfig`).

In a network that uses DHCP, each host is configured to send a DHCP request over the network upon boot, to discover whether there is a DHCP server they can use and ask for a network config from. The DHCP client has to amintain a communication with the server to renew its lease.

Bootup connection:
1. Host sends `DHCPDISCOVER` broadcast message.
2. DHCP server sends a `DHCPOFFER` message to the host.
3. Host sends a `DHCPREQUEST` message to the DHCP server.
4. DHCP server sends a `DHCPACK` message to the host.

### How to find the DHCP server address?

Logs have a DHCP message request logged:
```
cat /var/log/syslog | grep -i 'dhcp'
```

The `journalctl` command can be used to display these logs:
```
sudo journalctl -r | grep -m1 DHCPACK
```

The DHCP client on a host maintains a list of leases granted to it in the `dhclient.leases` file:
```
cat /var/lib/dhcp/dhclient.leases | grep -a -m1 &ldquo;dhcp-server-identifier&rdquo;
```

The `dhclient` command lets Linux machines obtain, release, and renew IP addresses:
```
dhclient -v 
```


## What is DNS?

DNS is **D**omain **N**ame **S**ystem, referred to as the phone book to the internet, mapping website names to IP addresses. It locates and translates domain names.

DNS servers receive queries about website names and responds with IP addresses.

Generally, which DNS server to use is established automatically by your ISP. 

### How to do a DNS lookup?

`ping` sends an ICMP Echo Request. If it works, you are successfully able to resolve a name or website to its IP address.
```
ping -c 3 server01
ping -c 3 192.168.1.101
```

`nslookup` queries DNS servers:
```
nslookup server01
```

`dig` gathers DNS info:
```
dig server01
dig -x 192.168.1.101
```

`host` is used for DNS lookups:
```
host 192.168.1.101
host -C example.com
host -t mx example.com
```


## What is ICMP?

ICMP is **I**nternet **C**ontrol **M**essage **P**rotocol. Devices in a network use it to communicate problems with data transmission, such as error messages, operational success/failure messages, etc. It is not typically used to exchange data in systems and is not usually used by end-user applications (except for `ping` and `traceroute`).

### Should ICMP be blocked?

Some network admins think it is a security risk and always block it at the firewall. However, it is useful for troubleshooting and essential for some network operations. (Instead of disabling ICMP, you can rate limit it...)

**Echo requests and replies**: enabling ICMP makes your host discoverable by `ping`, but if your web server is listening on port 80, it is still discoverable within your network. Disabling ICMP in your network makes troubleshooting harder because you can't contact your default gateway.

**Fragmentation needed / Packet Too Big**: these are essential in TCP's determination of allowing hosts to adjhust TCP maximum segment size (MSS) to one that will fit into the smallest MTU along the path between two hosts. If the hosts have smaller MTU than their own locals between them, your traffic will get silently blackholed. These ICMP packets get sent when a packet is too large for a router to transmit between an interface. The lack of ack of one of these packets is interpreted as congestion loss and the ICMP message will just be resent. This can cause silent TCP issues because the TCP handshakes still get sent, but as soon as any big packets get sent, the session appears to stall.

**Time Exceeded**: these are useful for the `traceroute` command. Disabling these makes some `traceroute` hops undiscoverable.

**NDP and SLACC (IPv6)**: IPv4 uses ARP for mapping between hardware and IP addresses, but IPv6 yues NDP (**N**eighbor **D**iscovery **P**rotocol). NDP provides router discovery, prefix discovery, address resolution, and more. SLACC **S**tate**L**ess **A**ddress **A**uto**C**onfiguration allows hosts to be dynamically configured similarly to DHCP.



## What is IP?

IP is **I**nternet **P**rotocol. It involves addressing packets so that they can travel across the network and arrive at the correct destination.

### What is IP subnetting?

Subnetting segments the network in meaningful ways, making routing more efficient.

A subnet is specied via a subnet mask, which identifies what IP addresses are in the same network. Devices compare destination IPs against their subnet mask to determine whether the destination is in their network (local) or not. They then route traffic differently depending on this answer, keeping local traffic within the subnet. This reduces congestion and network load outside the subnet (by avoiding unnecesarily sending local traffic out).

Example: A subnet of /24 results in a subnet mask of 225.225.225.0, or 0b11111111111111111111111100000000. Applying this mask to an IP address zeroes out the last 8 bits. Any IP address with the same first 24 bits is in the same subnet and can be contacted directly. Others must go through the router associated with that subnet and exit the subnet.

Subnets used to be created by class (e.g. A, B, C, D, E), with explicitly defined subnet mask lengths (e.g. /8, /16, /24), resulting in subnets with fixed numbers of addresses in them (16M, 64K, 256 respectively). This was inefficient because subnets had to be unnecessarily big. 

This led to the development of CIDR, **C**lassless **I**nter-**D**omain **R**outing, allocating space on any address-bit boundary. This gave organizations more granular and accurate control over subets and slowed IPv4 address exhaustion.

Example: a partner wanting 10 public IP addresses, plus an extra one for miscellaneous security purposes (e.g. firewall). A /24 subnet has 254 usable IP addresses, which is excessive. a /28, which has 16 addresses, is better. One can be used for network, one for broadcast, one for the datacenter, and another for the security (ASA), leaving 12 for them to use. They can assign them directly to hosts or use NAT.

### How does a machine get an IP address?

An IP address can be manually assigned:
```
ip addr add 10.0.0.1/24 dev eth0

# ifconfig interface_name IP_address
ifconfig e3a 192.0.2.10
```


## What is TCP?

TCP allows transmission of info in both directions.

### What happens in a TCP handshake?

1. The sender sends a SYN message to the receiver.
2. The receiver sends a SYN/ACK to the sender.
3. The sender sends an ACK to ack receiver.

In a closure:

1. The sender sends a FIN message to the receiver.
2. The receiver sends a FIN/ACK to the sender.
3. The sender sends an ACK to the receiver.

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

## How to troubleshoot a slow network?

Slow networks causes:

* **Hardware errors**: e.g. broken eth adapters or network configuration, physical cable problems
* **IP fragmentation**: when the receiving system can't contain a full datagram due to small MTU (maximum transit unit), breaking an IP packet down. 
	* Intermediate routers can fragment packets but can't reassemble them because the fragments can take different routes
	* TCP doesn't fragment IP packets by default -- instead, it listens for ICMP packets indicating MTU issues, and will decrease packet size accordingly
* **TCP retransmission**: if there's something wrong between endpoints

Triage strategies:

* Use `dmesg` to look at system messages
* Check the network via `ping` or `traceroute`
* Look at the interfaces (e.g. `ifconfig`)
* Look at open/closed/failed connections with `netstat`

Some problems solving strategies:

* Restart network interfaces (`ifdown eth0 && ifup eth0`)
* Check for IP address conflict (two or more devices on network trying to use the same IP address)
* Use `tcpdump` to troubleshoot TCP issues
* Change size of TCP window in kernel if it is too small
* Change MTU size if packets are getting lost

### Physical Layer

#### Is the physical interface up?

`ip link show` tells you about the interfaces:

```
# ip link show

1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: eth0: <BROADCAST,MULTICAST> mtu 1500 qdisc pfifo_fast state DOWN mode DEFAULT group default qlen 1000
link/ether 52:54:00:82:d6:6e brd ff:ff:ff:ff:ff:ff

# ip -br link show
lo UNKNOWN 00:00:00:00:00:00 <LOOPBACK,UP,LOWER_UP>
eth0 UP 52:54:00:82:d6:6e <BROADCAST,MULTICAST,UP,LOWER_UP>
```

To turn up /down an interface:
```
ip link set eth0 up

ifdown eth0
ifup eth0
```

#### Are packets getting dropped?

```
# ip -s link show eth0
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT group default qlen 1000
link/ether 52:54:00:82:d6:6e brd ff:ff:ff:ff:ff:ff
RX: bytes packets errors dropped overrun mcast
34107919 5808 0 6 0 0
TX: bytes packets errors dropped carrier collsns
434573 4487 0 0 0 0
```

#### Has the ethernet interface negotiated the right speed?

An interface negotiating the wrong speed (e.g. 10Gbps on an interface that only reports 1Gbps) can indicate hardware/cabling issues or negotiation misconfiguration on one side of the link (e.g. a misconfigured switch port).

```
# ethtool eth0
Settings for eth0:
Supported ports: [ TP ]
Supported link modes: 10baseT/Half 10baseT/Full
100baseT/Half 100baseT/Full
1000baseT/Full
Supported pause frame use: Symmetric
Supports auto-negotiation: Yes
Supported FEC modes: Not reported
Advertised link modes: 10baseT/Half 10baseT/Full
100baseT/Half 100baseT/Full
1000baseT/Full
Advertised pause frame use: Symmetric
Advertised auto-negotiation: Yes
Advertised FEC modes: Not reported
Speed: 1000Mb/s
Duplex: Full
Port: Twisted Pair
PHYAD: 1
Transceiver: internal
Auto-negotiation: on
MDI-X: on (auto)
Supports Wake-on: d
Wake-on: d
Current message level: 0x00000007 (7)
drv probe link
Link detected: yes
```

### Data Link Layer

The DLL is responsible for local network connectivity, e.g. the frames between hosts on the same LAN. Relevant protocols include ARP -- mapping between IPs and MAC addresses.

#### How to check entries in ARP table?

```
# ip neighbor show
192.168.122.1 dev eth0 lladdr 52:54:00:11:23:84 REACHABLE

# ip neighbor show
192.168.122.1 dev eth0 FAILED
```

### Internet/Network Layer

#### How to check local IP?

```
# ip -br address show
lo UNKNOWN 127.0.0.1/8 ::1/128
eth0 UP 192.168.122.135/24 fe80::184e:a34d:1d37:441a/64 fe80::c52f:d96e:a4a2:743/64
```

If there is no IP address present, that is a problem. Lack of IP address can be caused by local misconfiguration, (e.g. incorrect network config file), or by DHCP problems. 

#### How to troubleshoot general internet?

`ping` sends an ICMP Echo Request:

```
# ping www.google.com
```

`ping` can tell you a host is alive, but is not definitive. Some network operators block ICMP as a security precaution. 

Also, the times provided by `ping` can be helpful, but sometimes not -- some intermediate network gear rate-limits ICMP packets.

#### How to troubleshoot network?

`ping` can tell you a host is alive, but is not definitive. Some network operators block ICMP as a security precaution. 

Also, the times provided by `ping` can be helpful, but sometimes not -- some intermediate network gear rate-limits ICMP packets.

`traceroute` takes advantage of TTL in IP packets to determine path that traffic takes, by sending out packets one at a time, starting with a TTL of one. The packet expires in transit, so the upstream router sends back an ICMP TTL Exceeded packet. `traceroute` increments the TTL to determine the next hop, resulting in a list of intermediate routers that the packet traversed on its way to the destination.


Similarly to `ping`, `traceroute` uses ICMP packets, which can be filtered or rate limited. Also, paths to and from a destination may not be consistent or symmetric. `traceroute` can mislead you when trying to trace across large networks or the Internet (e.g. anything but small corp networks).

Also, a particular route may not have an upstream gateway, or it may not have a default route. Packets getting sent to different networks are sent to a gateway, which should know how to route a packet to its final destination. Gateways keep this info in their *routing tables*.

`ip route` can inspect and manipulate routing table entries in the kernel:
```
# ip route show
default via 192.168.122.1 dev eth0 proto dhcp metric 100
192.168.122.0/24 dev eth0 proto kernel scope link src 192.168.122.135 metric 100
```

Simple topologies include a default gateway -- a missing or incorrect gateway could be an issue.

#### How to troubleshoot network with a more complicated topology?

If the topology configures different routes for different networks, the routes will be listed with a specific prefix. 

```
# ip route show 10.0.0.0/8
10.0.0.0/8 via 192.168.122.200 dev eth0
```

#### How to troubleshoot DNS?

A telltale sign of DNS trouble is the ability to connect with a remote host by IP, but not hostname. 

```
# nslookup www.google.com
Server: 192.168.122.1
Address: 192.168.122.1#53

Non-authoritative answer:
Name: www.google.com
Address: 172.217.3.100
```

If `ping` or `traceroute` use a different IP address than `nslookup`, there may be a host file entry problem:

```
# nslookup www.google.com
Server: 192.168.122.1
Address: 192.168.122.1#53
  
Non-authoritative answer:
Name: www.google.com
Address: 172.217.12.132

# ping -c 1 www.google.com
PING www.google.com (1.2.3.4) 56(84) bytes of data.
^C
--- www.google.com ping statistics ---
1 packets transmitted, 0 received, 100% packet loss, time 0ms

# cat /etc/hosts
127.0.0.1 localhost localhost.localdomain localhost4 localhost4.localdomain4
::1 localhost localhost.localdomain localhost6 localhost6.localdomain6

1.2.3.4 www.google.com
```

In this example, google resolved to 172.217.12.132. But `ping` showed 1.2.3.4. The `/etc/hosts` file showed that someone put in an entry to override google as 1.2.3.4.

### Transport Layer

The transport layer has TCP and UDP. Applications listen on sockets, which consist of an IP address and a port. Traffic destined to an IP on a specific port will be directed to the listening application by the kernel.

#### What ports are listening on the localhost?

If you can't connect to a particular service on a machine, or if a daemon won't start because someone else is using that port, it could be a port issue. the `ss` command can be helpful:

```
ss -tunlp4
Netid State Recv-Q Send-Q Local Address:Port Peer Address:Port
udp UNCONN 0 0 *:68 *:* users:(("dhclient",pid=3167,fd=6))
udp UNCONN 0 0 127.0.0.1:323 *:* users:(("chronyd",pid=2821,fd=1))
tcp LISTEN 0 128 *:22 *:* users:(("sshd",pid=3366,fd=3))
tcp LISTEN 0 100 127.0.0.1:25 *:* users:(("master",pid=3600,fd=13))
```

#### Why can't I connect with a remote port?

If your machine can't connect to a remote port, the `telnet` command can be used to try to establish a TCP connection on that port. It is good to test remote TCP connectivity.

```
telnet 192.168.0.1 22
```

If telnet hangs, then it can't connect.

The `nmap` tool provides functionality like TCP+UDP port scanning remote machines, OS fingerprinting, and determining wherther report ports are simply closed or filtered.

```
nmap 192.168.0.1 -p 22
```

Also:

```
nc -zvw10 192.168.0.1 22

nmap 192.168.0.1 -p 22
```

For UDP, the `netcat` cool can check a remote UDP port:

```
# nc 192.168.122.1 -u 80
test
Ncat: Connection refused.
```

`netcat` can be used for TCP also. However, it can be a security risk also.

## Resources

* [Phillip Zito's TCP/IP stack article](https://www.linkedin.com/pulse/what-tcpip-stack-phillip-zito/)
* [Redhat's Beginner Guide to Troubleshooting Network Problems](https://www.redhat.com/sysadmin/beginners-guide-network-troubleshooting-linux)
* [Should I Block ICMP?](http://shouldiblockicmp.com/)
