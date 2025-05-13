import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class OSULatencyTest(rfm.RunOnlyRegressionTest):
    def __init__(self):
        # Test configuration
        self.descr = 'OSU Latency Test'
        self.valid_systems = ['aion:cpu']
        self.valid_prog_environs = ['builtin']
        
        # Using the exact path we found
        self.executable = '/opt/apps/easybuild/systems/aion/rhel810-20250405/2023b/epyc/software/OSU-Micro-Benchmarks/7.5-gompi-2023b/libexec/osu-micro-benchmarks/mpi/pt2pt/osu_latency'
        
        # Benchmark parameters
        self.num_tasks = 2
        self.num_tasks_per_node = 2
        self.num_cpus_per_task = 1  # Prevents SLURM conflict
        
        # Performance reference (Aion typical values)
        self.reference = {
            'aion:cpu': {
                'latency': (2.3, None, 0.1, 'µs')  # 2.3 µs ±10%
            }
        }
        
        # Result verification
        self.sanity_patterns = sn.assert_found(
            r'^8192\s+\d+\.\d+',  # Matches "8192    2.35"
            self.stdout
        )
        self.perf_patterns = {
            'latency': sn.extractsingle(
                r'^8192\s+(\d+\.\d+)',
                self.stdout, 1, float
            )
        }
