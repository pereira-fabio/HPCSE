import reframe as rfm, reframe.utility.sanity as sn


class OMB_EasyBuild(rfm.CompileOnlyRegressionTest):
    """Build OSU Micro-Benchmarks 7.2 with EasyBuild (gompi/2023b toolchain)."""

    valid_systems = ["aion:batch", "iris:batch"]
    valid_prog_environs = ["system-gcc"]  # any env is fine; we load EB below
    build_system = "EasyBuild"

    # ------------------------------------------------------------------
    # build phase
    # ------------------------------------------------------------------
    prebuild_cmds = [
        'module use "${EASYBUILD_PREFIX}/modules/all"',
        "module load tools/EasyBuild",
    ]

    @run_before("compile")
    def setup_build_system(self):
        self.build_system.easyconfigs = ["OSU-Micro-Benchmarks-7.2-gompi-2023b.eb"]
        self.build_system.options = ["-f"]

    # ------------------------------------------------------------------
    # stash the install path for downstream run-tests
    # ------------------------------------------------------------------
    @run_before("compile")
    def stash_path(self):
        self.postbuild_cmds = [
            "module load perf/OSU-Micro-Benchmarks/7.2-gompi-2023b",
            # grab the prefix from the module’s environment var
        ]

        # 'echo "${EBROOTOSUMINMICROMINBENCHMARKS}/libexec/osu-micro-benchmarks/mpi/pt2pt" > omb.path',
