# ReFrame site configuration for ULHPC clusters
site_configuration = {
    "systems": [
        # ------------------------------------------------------------------
        # AION
        # ------------------------------------------------------------------
        {
            "name": "aion",
            "descr": "ULHPC Aion cluster",
            "hostnames": [r"aion-[0-9]{4}"],
            "modules_system": "lmod",
            "partitions": [
                {
                    "name": "batch",
                    "scheduler": "slurm",
                    "launcher": "srun",
                    "access": ["--partition=batch", "--qos=normal"],
                    "environs": ["foss", "system-gcc"],  # defined below
                    "descr": "Aion regular CPU",
                },
            ],
            "env_vars": [
                ["intra_numa", "map_cpu:0,1"],
                ["cross_numa", "map_cpu:0,16"],
                ["cross_socket", "map_cpu:0,64"],
            ],
        },
        # ------------------------------------------------------------------
        # IRIS
        # ------------------------------------------------------------------
        {
            "name": "iris",
            "descr": "ULHPC Iris cluster",
            "hostnames": [r"iris-[0-9]{3}"],
            "modules_system": "lmod",
            "partitions": [
                {
                    "name": "batch",
                    "scheduler": "slurm",
                    "launcher": "srun",
                    "access": ["--partition=batch", "--qos=normal"],
                    "environs": ["foss", "system-gcc"],
                    "descr": "Iris regular CPU",
                },
            ],
            "env_vars": [
                ["intra_numa", "map_cpu:0,1"],
                ["cross_numa", "map_cpu:0,14"],
                ["cross_socket", "map_cpu:0,14"],
            ],
        },
    ],
    # ----------------------------------------------------------------------
    # Programming environments
    # ----------------------------------------------------------------------
    "environments": [
        {
            "name": "foss",
            "modules": ["env/testing/2023b", "toolchain/foss/2023b"],
            "cxx": "mpicxx",
            "cc": "mpicc",
            "ftn": "gfortran",
            "target_systems": ["aion", "iris"],
        },
        {
            "name": "system-gcc",
            "cc": "gcc",
            "cxx": "g++",
            "ftn": "gfortran",
            "target_systems": ["aion", "iris"],
        },
    ],
}
