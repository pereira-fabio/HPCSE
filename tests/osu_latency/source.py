import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class OSULatencyTest(rfm.RegressionTest):
    def __init__(self):
        # Test metadata
        self.descr = 'OSU Latency Test (pre-installed)'
        self.valid_systems = ['aion_standalone:default ', 'aion:cpu']
        self.valid_prog_environs = ['builtin']
        
        # Using pre-installed binary
        self.executable = 'osu_latency'
        self.executable_opts = ['-x', '100', '-i', '1000']  # Warmup and iterations
        
        # Runtime configuration
        self.num_tasks = 2
        self.num_tasks_per_node = 2  # Intra-node test
        self.message_size = 8192
        
        # Performance reference
        self.reference = {
            'aion:cpu': {
                'latency': (2.3, None, 0.1, 'µs')  # 2.3 µs ±10%
            }
        }
        
        # Sanity and performance patterns
        self.sanity_patterns = sn.assert_found(
            rf'^{self.message_size}\s+(\d+\.\d+)', 
            self.stdout
        )
        self.perf_patterns = {
            'latency': sn.extractsingle(
                rf'^{self.message_size}\s+(\d+\.\d+)',
                self.stdout, 1, float
            )
        }
        
        # NUMA binding
        self.job_options = ['--bind-to numa']

