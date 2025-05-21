# OSU Micro-Benchmark (OMB) Latency/Bandwidth Evaluation using ReFrame

This project uses [ReFrame](https://reframe-hpc.readthedocs.io/) to benchmark point-to-point communication performance of MPI using the OSU Micro-Benchmarks (OMB). The tests are configured to evaluate latency and bandwidth under different placement configurations and build sources.

---

## Assignment Overview

We evaluate the performance of the `osu_latency` and `osu_bw` benchmarks on the [Aion](https://hpc.uni.lu/systems/aion/) and Iris HPC clusters. Each run tests communication in different placement topologies:

- **intra_numa** – same NUMA node
- **cross_numa** – different NUMA nodes, same socket (if supported)
- **cross_socket** – different sockets, same node
- **inter_node** – across physical nodes

---

## Environment Setup

This project depends on:

- iris-cluster
- aion-cluster

So you need to have a account first to do benchmark :)
---

## Configuration

ReFrame is configured using `settings.py`, which defines systems (`aion`, `iris`), environments (`foss`), and custom bindings for CPU affinity.

Custom CPU mappings (set via `--cpu-bind`) are defined as:

```json
[
  ["intra_numa", "map_cpu:0,1"],
  ["cross_numa", "map_cpu:0,14"],
  ["cross_socket", "map_cpu:0,64"]
]
```

## Running the Benchmark

To launch the test suite and generate a performance report:

```sh
# latency benchmark
reframe -C settings.py -c tests/run/omb_latency.py -r --performance-report
# bandwidth benchmark
reframe -C settings.py -c tests/run/omb_bw.py -r --performance-report
```
This runs tests for:
* 3 binary sources: `generic`, `easybuild`, `eessi`
* 4 placements: intra_numa, cross_numa, cross_socket, inter_node

Each test is run with 2 MPI tasks and logs performance in microseconds (latency) or MB/s (bandwidth).

Note that on both **Iris** and **Aion**, you only need to run the **same script** to perform the benchmarking! Our script has already abstracted away the differences between the clusters using environment variables.

