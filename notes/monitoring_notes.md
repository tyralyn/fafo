# Monitoring

## General

### What are the pull and push model of monitoring?

Push model has applications send metrics to the server at regular intervals, which the server scrapes from the application endpoints. The pull model has the server query the metrics endpoints for data. 

Push is good for when metric sources are fewer in number, well-known in advance, and expose a fixed set of metrics. For example, microservices exposing their metrics and a known endpoint like `/metrics`.

Pull model is suited for scenarios where metric sources are numerous, dynamic, and not known in advance. For example, K8s clusters where new nodes and pods are frequently added and removed.
 
Push model is easier to set up and provides more control over when metrics are collected, but pull model is more flexible and handles dynamic environments better.

Push > Pull: 

* Push model works well when there are fewer, known metric sources
* Push model is easier to set up
* Push model provides more control over when metrics are collected


Pull > Push

* Pull model is more flexible handles ambiguity better, such as when metric sources are numerous, dynamic, and not known in advance.
* Pull model centralizes configuration -- monitoring system can be configured to scrape targets in some kind of order or use different scrape intervals.
* Pull model doesn't require application to handle sending metrics, eliminating need for application-level instrumentation
* Pull model doesn't put additional load on application servers -- application writes to application endpoint and monitoring system pulls from it
* Pull model reduces network traffic -- the target exposes a lightweight endpoint that only returns requested metrics
* Pull model lets monitoring collect metrics from any application, regardless of programming language or tech stack
* Pull model is less intrusive -- the target exposes only a read-only endpoint that returns metrics. In push model, target has to be granted write access to server.
* Pull model can scrape at regular intervals, ensuring no metrics are missed. In push model, target failing to push metrics results in lost metrics.

### What is tracing and spanning?

Tracing is monitoring and tracking the flow of requests through a distribuetd system or application to gain visibility into behavior and performance of a system. It breaks down each request into smaller units of works (spans) representing steps in the request processing pipeline. A span is a single unit of work.

## What is Monarch?

Monarch is Google's modern time-series database. Before Monarch was Borgmon, which is more similar to Prometheus.

Monarch data is divided into autonomous regions. However, it has global management and querying, and queries go straight to the source for data.

Monarch's two main components are *targets* and *metrics*. Targets are source entities that a time series (metric) is associated with. 

### Why did Google switch from Borgmon to Monarch?

Borgmon is decentralized, whereas Monarch is centralized. Teams had to operate their own Borgmons themselves, adding operation cost and requiring a lot of expertise. This also made correlating data between components on different Borgmon instances harder.

Borgmon did not have schemas for measurement dimensions and metrics, causing a lot of semantic ambiguities of queries and limiting expressiveness of query language.

Borgmon does not support histograms.

Monarch was designed for high availability and partition tolerance (and not consistency).

Monarch drops delayed writes, and prefers returning partial data to fully accurate data (inconsistency).

Monarch stores data close to where it was generated, making storage and retrieval cheaper and faster.

### What are the benefits of Monarch?

Monarch shards timeseries keys lexographically (alphabetically), improving ingestion and query scalability. Range assigners distribute lexical ranges to different leaf routers, distributing traffic.

Push-based data collection is more robust. It also simplifies architecture because central system does not need to access targets.

Schematized data model improves robustness and performace, so that data can be sharded based on location, user, and other target fields.

### How and where does Monarch store data?

Monarch is stored on regular memory instead of dedicated storage. Storing it in dedicated storage, which itself requires Monarch, causes circular dependency.

1. Clients send data to nearby ingestion routers in the same cluster.
2. The ingestion router finds the right place to store the data based on the target's `location` field, and forwards the data to the appropriate leaf router
3. The leaf router forwards the data to the appropriate leaves in the zone .
4. The leaves write data into their in-memory store. They also write data unreliably into recovery store.

Because the recovery store write is unreliable, the system won't hang on that and will continue operating if recovery store is unavailable. 

## What is Prometheus?

Prometheus is a time-series based monitoring system based on Borgmon. 

* **Multi-dimensional data model**: time series are identified by a metric name and set of key-value pairs.
* **Queries and visualization**: allows you to visualize via built-in expression browser, Grafana integration and console template language.
* **Operation**: each server is independent, relying on local storage. Binaries are statically linked. Automatic service discovery, which simplifies the process of adding new targets to be monitored without requiring extra configuration.
* **Storage**: time series are stored in memory and on local disk an a custom format. Can be sharded and federated. Time-series data retention and compaction.
* Alerting, client libraries, integration with a lot of third parties

Prometheus uses a pull model, where Prometheus pulls data from monitored targets at regular intervals. Supported protocols to expose metrics over include HTTP, SNMP, and JMX. Metric types include counters, gauges, histograms, summaries, etc.

### What is Prometheus architecture like?

* **Prometheus server**: collect, store, and query time-series data
* **Exporter**: agents that run on monitored targets and collect metrics data
* **Alertmanager**: handles alerts generated by Prometheus and sends notifications
* **Pushgateway**: component that allows for pushing metrics data to Prometheus from batch jobs, scripts, and other non-service targets

### How does Prometheus store data?

Prometheus uses TSDB (**T**ime **S**eries **D**atabase) for storage. TSDBs are designed to handle high write and query loads, and offer efficient storage and retrieval of time-series data. 

TSDBs are relatively large and uniform compared to other data, often with fewer relationships between data entries on different tables. This allows for use of specialized compression algorthms that don't work on less uniform data. They do not require infinite storage of entries and can be configured to delete old data.

Default retention in Prometheus is 15 days before being deleted from TSDB.

### WHat is cardinality in Prometheus?

Prometheus keeps all labels of a given timeseries together on disk, which can result in performance problems or crashes when labels have high cardinality (too many different values of labels). In something like Graphite, which doesn't care how finely a timeseries is subdivided because each leaf of its hierarchical structure is stored in its own file on disk.

How to limit metric cardinality in Prometheus:

* **Avoid server-specific labels**: stuff like IP addresses or node names come and go, resulting in high cardinality
* **Avoid application-specific labels**: abundant stuff like names, employer IDs, or jobs result in high cardinality and are not usually needed in monitoring at that detailed granularity
* **Group web data labels**: HTTP status codes don't usually need to be fully represented in metric label. 3xx redirects vs 4xx errors vs 5xx errors is useful to know but not much more than that.

Rule of thumb is to keep product of cardinalities for all labels of that metric under 1k.


## How do you monitor a Linux machine?

* **`top`, `htop`, etc.**: provides real-time info on system processes and resource usage, such as CPU, memory, and disk I/O
* **`ps`**: provides detailed info on processes, useful for identifying high resource consumers.
* **`lsof`**: lists open files and network connections.
* **`vmstat`**: good for identifying bottlenecks and monitoring system performance, based on detailed info on (virtual) system memory, CPU, and disk I/O.
* **`iostat`**: providing detailed info on I/O performance to identify disk bottlenecks and usage.
* **`sar`**: **S**ystem **A**ctivity **R**eporter, collecting and reportng historical system performance metrics like CPU, memory, disk I/O, and network activity.
* **`netstat`**: useful for monitoring network activity and diagnosing network issues, based on network stats about network connections, socket states, and interface statistics.
* **`tcpdump`**: captures network TCP traffic for network troubleshooting, monitoring, and security analysis.
* **`iftop`**: displays real-time bandwidth users for interfaces w/ network connections, useful for identifying bandwidth hogs and monitoring network activity.

## How do you monitor a frontend?

* **Synthetic monitoring**: tools that automatically perform checks on the website or API at regular intervals, such as uptime monitoring services, load testing software, transaction monitoring, and security scans. Good for SLAs because they are end-to-end.
* **Error tracking and crash reporting**: tools that let you identify and troubleshoot runtime issues by installing an agent in the application that listens for errors and sends them to a backend for aggregation and alerting. They often include anonymization features.
* **Real user monitoring (RUM)**: tools that monitor your application;s usage and performance from the point of view of the end user (sometimes called browser monitoring). Can detect performance issues, Javascript issues, and other on-device info. Measures end-user metrics like page load time and helps understand the end-to-end experience and what real users (as opposed to a dev on a powerful workstation) perceives.
* **Marketing analytics**: reports and statistics to help understand where visitors are coming from, what pages they visit, and which marketing efforts convert better.
* **Product analytics**: reports and statistics to help understand how a website or app is being used in terms of its features (vs marketing analytic's stats on visitor arrival and content). Helps product teams identify user experience problems, product feature use, and which customers are likely to churn.
* **Application performance monitoring (APM)**: tools to help debug issues and identify performance bottlenecks.

## How to reduce monitoring usage?

* Drop unused metrics
* Avoid cardinality (exclude granular IDs/info, exclude ephemeral IDs/info, aggregate out too-granular info)
* Configure applications and exporters
* Relabel metrics to make them easier to drop
* Focus on high-cardinality metrics (use something like Prometheus' cardinality exporter to find the dimensionality of metrics)
* Analyze resource usage with tools like `pprof`
* Configure scrape or push intervals


## References

* [dmathieu's monarch article](https://dmathieu.com/articles/reading/papers/monarch/)
* [A Quick Guide on Website and App Monitoring Tools](https://medium.com/@thejufo/a-quick-guide-on-website-and-app-monitoring-tools-525472fe9568)
* [basic prometheus overview](https://medium.com/@sayalishewale12/prometheus-1753d12a240a)
* [why and how to use prometheus for kubernetes](https://medium.com/@ziprecruiter.engineering/why-and-how-we-use-prometheus-to-monitor-kubernetes-9da1f11fd39d)