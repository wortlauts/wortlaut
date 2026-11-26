# 0005: First deployment on a Raspberry Pi, one environment

Date: 2026-11-26
Status: accepted

## Context

The first live deployment should cost nothing. A Raspberry Pi 5 with 4 GB of memory is available. It already runs other services, so only about 2 GB of memory can be used. A second server available to the owner has 1 core and under 1 GB of free memory, which is too little for Elasticsearch.

A second environment with its own Elasticsearch, and Kibana or Airflow on top, does not fit into that memory. The index itself is small (about 90 MB for three legislative periods), so disk space is not the limit.

## Decision

- Everything runs **once** on the Raspberry Pi with Docker Compose: one Elasticsearch, one API, one frontend. Development happens on the developer machine.
- **Kibana runs permanently**, limited to 1.1 GB (it needs a JavaScript heap of at least 768 MB). It is the first service to give up if the memory turns out to be too small.
- **Airflow is postponed.** It needs more memory than is free. The daily indexing run starts as a timer on the Pi and moves to Airflow when there is room for it.
- Memory limits protect the services that already run on the Pi. They need the memory cgroup of the kernel to be enabled.
- Images are built for `linux/arm64` in CI.
- The API reads Elasticsearch with a read-only user. Secrets stay out of plain text in the repos (environment variables or SOPS).

## Consequences

- No hosting costs. An outage of the Pi or the home connection takes the site down, which is accepted for a side project.
- With Kibana the stack needs about 2.3 GB, which is close to what the Pi has to spare. A second environment (DEV) needs more memory or a second host. The Compose files should not depend on there being only one.
- Elasticsearch has to be tried early on the Pi 5, because its 16 KB memory pages have caused problems with some software.
- If the memory turns out to be too small, the next step is a small paid server. The Compose files stay the same.
- How releases reach the Pi and how the stack is isolated from the other services need their own ADR.
