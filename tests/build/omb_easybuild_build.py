import pathlib, reframe as rfm, reframe.utility.sanity as sn


@rfm.simple_test
class OMB_EasyBuild(rfm.CompileOnlyRegressionTest):
    """Build OSU Micro-Benchmarks 7.2 with EasyBuild (gompi/2023b toolchain)."""

    valid_systems = ["aion:batch", "iris:batch"]
    valid_prog_environs = ["foss"]  # any env is fine; we load EB below
    build_system = "EasyBuild"

    # ------------------------------------------------------------------
    # build phase
    # ------------------------------------------------------------------
    prebuild_cmds = [
        'module use "${EASYBUILD_PREFIX}/modules/all"',
        # Load EasyBuild itself and the meta-toolchain module
        "module load tools/EasyBuild",
        # Build OSU 7.2 with the gompi/2023b toolchain in "try" mode
        # "eb --try-software=OSU-Micro-Benchmarks,7.2 "
        # "   --try-toolchain=gompi,2023b "
        # "   --robot --quiet --force",
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
            'echo "${EBROOTOSUMINMICROMINBENCHMARKS}/libexec/osu-micro-benchmarks/mpi/pt2pt" > omb.path',
        ]

    @run_after("compile")
    def set_sanity(self):
        path_file = pathlib.Path(self.stagedir) / "omb.path"
        self.sanity_patterns = sn.assert_found(r"OSU", str(path_file))
