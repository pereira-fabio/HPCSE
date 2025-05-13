site_configuration = {
    'systems': [
        {
            'name': 'aion_standalone',
            'descr': 'Stand alone Aion node',
            'hostnames': [r'aion-[0-9]{4}'],
            'modules_system': 'lmod',
            'partitions': [
                {
                    'name': 'default',  # No trailing space
                    'scheduler': 'local',
                    'launcher': 'local',
                    'environs': ['builtin'],
                    'modules': []
                }
            ]
        },
        {
            'name': 'aion',
            'descr': 'Aion cluster',
            'hostnames': [r'aion-\d+'],
            'modules_system': 'lmod',
            'partitions': [
                {
                    'name': 'cpu',  # No trailing space
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'environs': ['builtin'],
                    'modules': []
                }
            ]
        }
    ],
    'environments': [
        {
            'name': 'builtin',
            'cc': 'mpicc',
            'cxx': 'mpicxx',
            'ftn': 'mpif90',
            'target_systems': ['aion_standalone', 'aion']
        }
    ]
}
