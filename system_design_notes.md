# System Design 

## How to approach system design?

1. **Gather requirements**: who is this for? how/when/where will they use it? what is the success metrics? what other kinds of support (e.g. oncalls) are needed?
2. **High-level estimates**
3. 

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

Other things to consider:
* DNS
* CDN
* Load balancers
* Reverse Proxy
* TODO more stuff

### Tips

* Don't rush to architecture
* Do breadth-first of solution space, and then go deeper. Do high-level components in general terms first -- if you go too deep on something, the interviewer will drill you on it
* Ask yes/no and A-or-B questions -- give the interviewer choices and can provide alternatives if they want

## References

* [Engineering Leader's System Design Interview](https://docs.google.com/document/d/1ckl5roGhYkZAEBfaJHZT_-80upmhfzBZWAGmXvPJd3U/edit#)

