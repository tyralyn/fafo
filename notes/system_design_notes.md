# System Design 

## How to approach system design?

1. **Gather requirements**: who is this for? how/when/where will they use it? what is the success metrics? what other kinds of support (e.g. oncalls) are needed?
2. **High-level estimates**
3. 

### Schedule

* 5 mins clarifying functional requirements
* 5 mins clarifying nonfunctional requirements
* 5 mins talking about the logical entities in the system
* 5 mins talking about the APIs
* 5 mins doing the physical architecture

### Requirements

**Business**: what is the key metric of success (e.g. revenue, conversions)?

**Functional**: what should the system do? 

* Each major thing may end up being an API
* Come up with a list of things and scope down (e.g. set security and authentication aside in favor of more interesting stuff.

**Non-functional requirements**:

* number of users, kinds of users
* user location, language, devices (mobile, web, desktop)
* usage patterns (who, what, where, when)
* maintainability, extensibility, cost, reuse
* low latency, high availability, are usually givens
* partition tolerance (ability to handle gaps in communication between distributed systems) or strong consistency>
* on-call rotations and support needs
* efficiency operations --> lower energy usage --> better for climate and DevOps budget
* less data --> less user bandwidth --> more $$
* less work --> fewer pieces in system --> resiliency + lower costs

**Ask interviewer if the assumptions are complete!**

* What is out of scope?
* Have I missed any key considerations?

### High-level estimates

Understanding the size and shape of the problem.

* **Number of users per day/month**: US (~330M population), India (~1.4B population), world (~8B population), major business-to-commercial (2~B monthly active users)
* **Read/write ratio**
* **Traffic estimates**: r/w QPS and volume of data

Tips:

* At the very least, do QPS per API call.
* If you're starting small and scaling up, set the total goal first and then the starting point / incremental goal (e.g. 100x or 1000x smaller).
* For global/Internet scale problems, suggest 100 points-of-presence (POPs) or datacenters, and design a system for a single POP/DC and then scale up.

### API + data design

Tip:

* Break down into subtaks
* APIs for read/write scenarios for crucial components -- API endpoints and initial data -- and tie them back to functional requirements
* Data schema -- JSON is pretty easy
* Table/database may be relevant

CAP Theorem: between consistency, availability, and partition tolerance, pick two.

* Latency and throughput requirements
* Consistency vs. availability: 


### High-level architecture diagram

Tip:

* Start with a high-level diagram and circle back
* Keep high-level (e.g. application server, data store) and avoid naming specific technologies early. Discuss technologies later in scaling up section
* Talk through API endpoints
* Generally don't pseudocode the algorithm unless it is a stupid complex system -- it'll make you look like you're hung up on details. "I'm avoiding rushing to the diagram"


### Deep dive and scaling

* What happens when we add more data? e.g. 10x, 100x data or QPS
* Refer back to functional requirements and estimates to guide this discussion
* Steer discussion to areas you're most familiar with
* For each component, consider availability, consistency, and scale

Casual generic robust server that isn't too expensive:
* **Generic server**: 100GB RAM, 1TB SSD, 10CPU @ 2.3GHz+, 10GB/s network
* **Storage server**: 50GB RAM, 10TB SSD

Horizontal scaling means adding more servers to distribute requests, whereas vertical scaling increases capacity of a single machine by adding resources and allowing it to handle more traffic.

Other things to consider:
* DNS
* CDN
* **Load balancers**: balancing load amongst servers, distributing traffic, preventing service breakdown, etc. Help maintain throughput and availability
* **Forward proxy**: middleman between client and server; masks clients and hides client identity from the server (e.g. VPN)
* **Reverse proxy**: mask for servers, hides server identity from response (e.g. load balancer)
* **Caching**: storing frequently used data to let it be accessed quickly. Cache memory is generally expensive, so eviction algorithms like LIFO, FIFO, LRU, and LFU are used to manage removal of cache.
* **Consistent hashing**: a horizontal scaling mechanism where you look at all the servers as a virtual circular ring and assign servers random locations based on a hash dunction, to allow for efficient request distribution
* TODO more stuff


### Tips

* Don't rush to architecture
* Do breadth-first of solution space, and then go deeper. Do high-level components in general terms first -- if you go too deep on something, the interviewer will drill you on it
* Ask yes/no and A-or-B questions -- give the interviewer choices and can provide alternatives if they want

## Concepts

### Metrics

* **Availability**: percentage time system is operational
* **Latency**: measure of time duration to produce the result
* **Throughput**: maximum rate of transfer or capacity of the system

### Availability

**Availability**: percentage of time in a given period that a system is available to perform its task and function under normal conditions; how resistant a system is to failure.

`Availability` = `Uptime` / (`Uptime` + `Downtime`)

**Redundancy**: duiplicating or adding additional hardware (servers or storage) components
* **Passive redundancy**: turning on a backup when server goes down
* **Active redundancy**: multiple active components (servers or storage devices) working simultaneously to perform the same tasks. If one fails others take over

**Failure detection mechanisms**: identifying failures, requiring regular high-availability testing and the ability to take corrective action whenever one of the components become unavailable

High availability vs. fault tolerance
* High availability = system or component's ability to remain operational and accessible with minimal downtimw
* Fault tolerance = a system or components ability to continue functioning normally even int he event of failure


### Latency

**Latency** ius how quickly data can be transferred between client and server.

Causes:
* **Transmission medium**: physical path between endpoints, e.g. WAN, Wifi, fiber optic cables
* **Propagation**: the amount of time required for a packet to travel fro one source to another. Distance between communicating nodes
* **Routers**: how efficiently routers/hops process requests
* **Storage delays**: the type of storage system, the time taken to process and return data

How to measure latency:
* **Ping**: send packet to address and see how fast a response takes
* **Traceroute**
* **MTR (my traceroute)**: combo of ping and traceroute, gives a list of reports on how each hop in a network is required for a packet to travel from one end to the other, with details like percentage loss, avg latecency, etc. 

How to optimize latency:
* **HTTP/2**: allows parallelized transfers, minimizes round trips form sender to receiver
* **Reducing external HTTP requests**: third-party HTTP increases latency, so reduce these
* **CDN**: stores resources in multiple locations worldwide and reduces request and response travel time, basically caching
* **Browser caching**: local caching
* **Disk I/O**: using write-through caches or in-memory databases or combining writes or using fast storage like SSDs
* **Efficient algorithms**: avoiding unnecessary loops or nested expensive operations
* **Reducing locks**: using design patterns that avoid locking, since multithreaded locks introduce latency
* **Asychronity**: utilize hardware better by eliminating blocking
* **Limiting queues**: bounding queues and providing back pressure to reduce queue times

### Throughput

**Throughput**: The rate at which something is produced or processed.

Factors affecting throughput:
* **Analog limitations**: physical medium of networked communication sustem can have dignificant impoact on max achieveable throughput
* **Hardware limitations**: systems have limited processing power and can only handle a certain amount of workload at a time
* **High accessibility or concurrent requests**: sharing resources camongst users can affect systems ability to process and transmit data efficiently

How to increase throughput:
* Upgrading hardware components (processors, memory, storage devives)
* Using proper load-balancing to distribute workload amonst components
* Increasing network bandwidth or upgrading network components to improve data transmission speed
* Writing efficient code and using optimized algorithms to improve processing speed
* Caching frequently used data in memory to reduce time required for data retrieval
* Breaking a task down into smaller subtasks and processing them simultaneously using multiple processors (parallel processing)
* Minimixing protocl overhead 

### Load Balancers

**Load balancer**: software or device sitting between clients and a group of servers and distributes workloads evenly to prevent any one server from becoming overloaded. Prevents single points of failure too -- if a single server goes down, then the entire application beceomes unavailable. By scaling horizontally and adding a load balancer, we can address this.

Where to add load balancers:
* Between clients and frontend web servers
* Between frontend web servers and backend application servers
* Between backend application servers and cache servers
* Between cache servers and database servers

#### Software and Hardware Load Balancers

Types of load balancers:
* **Software load balancers**: more flexible and customizable. Can be installed on a server and configured to meet specific needs of a system. Easier to scale, cheaper
* **Hardware load balancers**: physical devices installed on a network, less flexible and customizable, but often faster and more reliable because they are dedicated hardware devices designed specifically for load balancing. Extra secure because only authorized personnel can physically access the servers, but require extra expertise

Examples of software load balancers:
* **HAProxy**: TCP load balancer
* **NGINX**: HTTP load balancer with SSL termination support
* **mod_athena**: Apache-based HTTP load balancer
* **Varnish**: reverse proxy-based load balancer
* **Balance**: open-source TCP load balancer
* **LVS**: linux virtual server offering layer 4 load balancing

Examples of hardware load balancers:
* F5 BIG-IP load balancer
* CISCO system catalyst
* Barracuda load balancer
* Coyotepoint load balancer
* Citrix NetScaler

#### Layer 4 and Layer 7 Load Balancing

Layer 4 load balancing uses TCP client-to-server connection info, while Layer 7 has uses two TCP connections from client to server. Layer 7 has application awareness while Layer 4 only knows about network and application ports. Layer 7 balances load based on data content, whereas layer 4 carries out load balancing based on inbuilt software algorithm. 

#### Load Balancing Algorithms

**Static load balancing algorithms** are independent of backend state. They are simpler and more efficient but less effective. This includes round robin and weighted round robin, source IP hash, URL hash, randomized algorithm, etc.

**Dynamic load balancing algorhtms** take into account the backent server state and load when distributing requests.


### Long Polling

Long polling is a reliable way to keep clients updated with new info real-time.

Polling is a technique for letting servers send to clients. Long polling allows servers to send data whenever it becomes available. Clients send requests but don't require immediate response. Servers wait until data is available and then sends complete response to client.

Client sends long-polling HTTP request. When update is available, server provides client with a complete response. Client sends a new long-poll request with timeout. If time out, client restablishes connection.

* Reduces number of HTTP requests required
* Long polling is included in HTTP protocol, thus making it generally available and uses less bandwidth than short polling
* Not inherently scalable, u have to do something about it
* Long polling is basically modified version of underlying request/response mechanism
* Some challenges around message ordering and delivery, performance and scaling

### Publisher-subscriber (pubsub) architectural design pattern

**Pub/sub**: an architectural design pattern that enables publishers and subscribers to communicate with each other. Publishers and subscribers rely on a message broker to send messages from the publisher to the subscriber. Messages (events) are sent out buy the host (publisher) to a channel, which subscribers can join. Allows messages to flow between system components without components knowing about each others identities.

Pros:
* **Low coupling for publisher**: publishers don't need to know the number, identity, or types of messages that subscribers are interested in, resulting in flexibility and scalability b/c subscribers can be added without affecting publisher
* **Lower cognitive load for subscribers**: subscribers don't have to worry about inner workings of publisher, and only communicate with publisher using publisher's public API
* **Separation of concerns**: developers can practice finegrained separation of concerns. Different kinds of messages can be split into distinct categories each fulfilling a single, straightforward purpose
* **Improved testability**: fine-grained topic control makes it easy to confirm eent buses are transmitting necessary messages]
* **Improved security**: well-suited for minimil privileges

Cons:
* **Inflexibility of publisher data**: it can be hard to modify the data structure of messages once established because all subscribers have to accept the new format. This can be addressed with versioned messages format, but that assumes subscribers to be correctly consuming version info. Alternatively, use versioned endpoints (e.g. `/APIv0/` and `/APIv1`), which requires developers to support multiple versions
* **Instability of delivery**: determining health of subscribers can be difficult, publisher has no idea of systems listening to its messages

### Rate limiting and throttling

**Rate limiting**: a technique used to control the amount of traffic allowed to acess a system or network within a specific time period

Benefits: avoiding resource depletion due to DDoS attacks, reducing expenses, ensuring servers aren't overburdened

Methods of implementing API rate-limiting:
* **Request queues**
* **Throttling**: establishing temporaryu state in which each request is evaluated bu API, allowing API dev to control how the API is used
* **Rate limiting algorithms**: e.g. fixed window technique (tracking number of incoming requests over a fixed time period), leaky bucjet technique (converting incoming requets into a FIFO queue and dropping requests when the queue is full, allowing processing items at a consistent rate), sliding window technique (similar to fixed-window, but the time period starting when the user makes a new request rather than at a predetermined time), etc.



## Different options

### Why would someone pick microservices vs. monolithic architecture?

Microservice architecture is breaking up a single large system into smaller, loosely-coupled components. It is an alternative to monolithic architecture. 

Microservices > monolithic
* Each element can be scaled independently in microservices
* Easier to integrate with new tech in microservices
* Microservices are more resilient because a single bug or issue is less likely to ruin everything 
* Microservices can be worked on independently

Monolithic > microservices

* Easier to develop an entire app and get it to market with monolithic
* Monolithic systems have moving parts so deployments are simpler
* It is easier to test and debug monolithic systems
* Communication within a single unit is more secure (microservices require IPCs, and the API gateways raise additional security issues)

### Why would someone pick noSQL over a relational database?

SQL databases are table-based, whereas noSQL databases are document, key-value, graph, or wide-column stores. SQL databases have schemas, whereas noSQL databases have dynamic schemas for unstructured data.

SQL > noSQL
* SQL is good for multi-row transactions
* SQL is vertically scalable -- you can increase load on a single server by adding more resources (CPU, RAM, SSD)
* SQL follows **ACID** properties (**A**tomicity ensures a group of operations is treated as a single unit of work, **C**onsistency ensures that each transaction complies with a set of rules to prevent from corrupting data and that transactions move from one valid state to another, **I**solation meaning that transactions are executed independendly of one another, ensuring concurrency, **D**urability ensuring data written to the database is persisted and remains there) for transaction management (this is required of RDBMS but not necessarily for noSQL DBs)
* SQL supports joins and complex queries

noSQL vs SQL
* noSQL is good for unstructured data, like documents or JSON
* noSQL is horizontally scalable -- you can handle higher traffic by sharding
* noSQL follors **BASE** compliance (**B**asically **A**vailable system, **S**oft state tat provides flexibility to the system and allows it to change over time for faster access, and **E**ventual consitentcy ensuring that the system takes some time to reach consistent state and eventually becomes consistent)
* noSQL is easier to set up quickly, since it doesn't have the overhead of a SQL database

### Why would someone pick a push model over a pull model?

Push models send a request every time something changes, whereas pull models set a schedule by which to collect data.

Push > pull
* If you push every time you have an update, you can update more quickly
* No schedule required, so less overhead
* Good for real-time, one-way data flow
* Pull model requires knowledge of the info by the puller, so push is better if the actual data being exchanged is changing
* Pull model requires knowing of an entity to get info from it, so push can be better because it doesn't require a handshake/setup

Pull > push
* For push, the sending entities have to know where to push to (clients are heavier)
* If you have limited, known set of data, pull is good
* Pull lets you take in load balancing, etc, from the server side (pushers don't really know a lot about load balancing)
* Pull lets you distribute work easier
* With pull, you can stop pulling if you need to -- easier to handle resource exhaustion

Now there are **service mesh** architectures: keeping clients simple, putting client complexity in sidecar processes. Thus, clients only need to know how to make basic requests, and service mesh handles routing, service discovery, retries, circuit breakers, instrumentation, etc.

### Why would someone use a proxy?

A proxy is a middleman server between the client and server. 

**Forward proxies** sit in front of client machines, and client requests go to the forward proxy, which forwards to the server. Forward proxies can filter network traffic (e.g. block access to specific websites or reestrict access, enforce security policies and protect against malware, etc.) Forward proxies like VPNs can provide anonymity for clients by hiding IP addresses, and can optimize network traffic by compressing data, removing unnecessary headers, and reducing size of transferred data.

**Reverse proxies** sit between one or more servers and act on behalf of the server. Reverse proxies can intercept client requests and handle the sending request and responses, so that the client thinks it is interacting directly with the server. Reverse proxies can hide backend server IPs to prevent DDoS attackts and reject or rate-limit traffic per client. Reverse proxies can also load balance to distribute traffic amongst servers and prevent overload, also incorporating caching if desired.

Reverse proxies increase complexity (increasing latency and overhead) and add a single failure surface. They also must manage SSL certs, which can be challenging if there are multipkle backend servers with SSL configurations.


## Example: URL shortener

[link](https://www.enjoyalgorithms.com/blog/design-a-url-shortening-service-like-tiny-url)
# 
 
## References

* [Engineering Leader's System Design Interview](https://docs.google.com/document/d/1ckl5roGhYkZAEBfaJHZT_-80upmhfzBZWAGmXvPJd3U/edit#)

