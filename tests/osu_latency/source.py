import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class OSULatencyTest(rfm.RegressionTest):
    def __init__(self):
        # Remove all spaces in system names
        self.valid_systems = ['aion_standalone:default', 'aion:cpu']
        self.valid_prog_environs = ['builtin']
        
        # Rest of your test configuration...
        self.descr = 'OSU Latency Test'
        self.executable = 'osu_latency'

        self.num_tasks = 2
        self.num_tasks_per_node = 2
        self.reference = {
            'aion_standalone:default': {'latency': (2.3, None, 0.1, 'µs')},
            'aion:cpu': {'latency': (2.3, None, 0.1, 'µs')}
        }
        self.sanity_patterns = sn.assert_found(r'^8192\s+(\d+\.\d+)', self.stdout)
