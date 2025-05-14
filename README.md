# HPC Software Environment


## Interactive mode 
```
salloc -p interactive --qos debug --time=2:00:00 -N 2 -n 2 -c 32
```

```
module load system/hwloc 
```

```
module load perf/OSU-Micro-Benchmarks
```

```
module load tools/EasyBuild/5.0.0
```

```
module use /opt/apps/easybuild/systems/aion/rhel810-20250216/2023b/epyc/modules/all
```

```
module load devel/ReFrame
```

```
reframe --checkpath source.py --run
```

```
reframe -C ../common/config.py -c source.py -r --system=aion:cpu -v
```
