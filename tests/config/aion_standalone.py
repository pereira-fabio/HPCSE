site_configuration = {
    'systems': [
        {
            'name': 'aion_standalone',
            'descr': 'Stand alone Aion node',
            'hostnames': [r'aion-[0-9]{4}'],
            'modules_system': 'nomod',
            'partitions': [
                {
                    'name': 'default',
                    'scheduler': 'local',
                    'launcher': 'local',
                    'environs': ['system-gcc'],
                }
            ]
        }
    ],
    'environments': [
        {
            'name': 'system-gcc',
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran',
            'target_systems': ['aion_standalone']
        },
        {
            'name': 'system-clang',
            'cc': 'clang',
            'cxx': 'clang++',
            'ftn': '',
            'target_systems': ['aion_standalone']
        },
    ]
}
