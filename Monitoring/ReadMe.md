# sFlow
## What is sFlow ?
sFlow® is an industry standard technology for monitoring high speed switched networks. It gives complete visibility into the use of networks enabling performance optimization, accounting/billing for usage, and defense against security threats.

## What is sFlow-RT ?
sFlow-RT® incorporates InMon's asynchronous analytics technology providing real-time visibility to Software Defined Networking (SDN), DevOps and Orchestration stacks and enabling new classes of performance aware automation such as load balancing, DDoS mitigation and workload placement.

![alt text](https://sflow-rt.com/img/rt-ecosystem.png)


## Why we use sFlow-RT ?
We use this Module because standard sFlow instrumentation is built into network equipment from over 40 vendors. We use this module to visualize attakes.

## How to install 
TO run sFlow-rt we must Download the tar file, extract it and run it.
```
wget https://inmon.com/products/sFlow-RT/sflow-rt.tar.gz
tar -xvzf sflow-rt.tar.gz
./sflow-rt/start.sh
```
After that the sFlow-RT is available in port 8008 and we can connect to [sFlow-RT GUI](http://localhost:8008) using a web browser.