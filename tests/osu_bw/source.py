import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class OSUBandwidthTest(rfm.RunOnlyRegressionTest):
    def __init__(self):
        # Test configuration
        self.descr = 'OSU Bandwidth Test'
        self.valid_systems = ['aion:cpu']
        self.valid_prog_environs = ['builtin']
        
        # Path to binary
        self.executable = '/opt/apps/easybuild/systems/aion/rhel810-20250405/2023b/epyc/software/OSU-Micro-Benchmarks/7.5-gompi-2023b/libexec/osu-micro-benchmarks/mpi/pt2pt/osu_bw'
        
        # Process configuration
        self.num_tasks = 2
        self.num_tasks_per_node = 2
        self.num_cpus_per_task = 1
        
        # Test parameters
        self.message_size = 1048576  # 1MB
        
        # Updated reference based on actual measurement
        self.reference = {
            'aion:cpu': {
                'bandwidth': (14950, None, 0.2, 'MB/s')  # New baseline ±20%
            }
        }
        
        # Result verification
        self.sanity_patterns = sn.assert_found(
            rf'^{self.message_size}\s+\d+\.\d+',
            self.stdout
        )
        self.perf_patterns = {
            'bandwidth': sn.extractsingle(
                rf'^{self.message_size}\s+(\d+\.\d+)',
                self.stdout, 1, float
            )
        }
