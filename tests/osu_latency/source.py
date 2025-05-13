import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class OSULatencySource(rfm.RegressionTest):
    def __init__(self):
        # Test metadata
        self.descr = 'OSU Latency Test (compiled from source)'
        self.valid_systems = ['aion:cpu', 'iris:cpu']
        self.valid_prog_environs = ['default']
        self.build_system = 'Make'
        self.executable = 'osu_latency'
        
        # Source and build configuration
        self.sourcesdir = 'https://mvapich.cse.ohio-state.edu/download/mvapich/osu-micro-benchmarks-7.2.tar.gz'
        self.build_system.cppflags = ['-O3']
        self.build_system.make_opts = ['clean', 'all']
        
        # Runtime configuration
        self.num_tasks = 2
        self.num_tasks_per_node = 2  # Intra-node test
        self.message_size = 8192  # Fixed message size
        
        # Modules
        self.modules = ['foss/2023b', 'hwloc']
        
        # Performance reference (Aion)
        self.reference = {
            'aion:cpu': {
                'latency': (2.3, None, 0.1, 'µs')  # 2.3 µs ±10%
            }
        }
        
    def setup(self, partition, environ, **job_opts):
        super().setup(partition, environ, **job_opts)
        # Additional setup if needed
        
    def post_build(self):
        # Verify compilation
        super().post_build()
        
    def run(self):
        # NUMA binding for intra-node
        self.job.launcher.options = ['--bind-to numa']
        super().run()
        
    @rfm.run_before('sanity')
    def set_sanity_patterns(self):
        self.sanity_patterns = sn.assert_found(
            rf'^{self.message_size}\s+(\d+\.\d+)', 
            self.stdout
        )
