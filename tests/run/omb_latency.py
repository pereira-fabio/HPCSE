import reframe as rfm, reframe.utility.sanity as sn
import os
from omb_generic_build import OMB_GenericBuild
from omb_easybuild_build import OMB_EasyBuild


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


class fetch_osu_benchmarks(rfm.RunOnlyRegressionTest):
    descr = "Fetch OSU benchmarks"
    version = variable(str, value="7.2")
    executable = "wget"
    executable_opts = [
        f"http://mvapich.cse.ohio-state.edu/download/mvapich/osu-micro-benchmarks-{version}.tar.gz"  # noqa: E501
    ]
    local = True

    @sanity_function
    def validate_download(self):
        return sn.assert_eq(self.job.exitcode, 0)


class OMB_GenericBuild(rfm.CompileOnlyRegressionTest):
    descr = "Build OMB benchmarks"
    valid_systems = ["iris:batch", "aion:batch"]
    build_system = "Autotools"
    valid_prog_environs = ["foss"]
    build_prefix = variable(str)
    osu_benchmarks = fixture(fetch_osu_benchmarks, scope="session")

    @run_before("compile")
    def prepare_build(self):
        tarball = f"osu-micro-benchmarks-{self.osu_benchmarks.version}.tar.gz"
        self.build_prefix = tarball[:-7]  # remove .tar.gz extension

        fullpath = os.path.join(self.osu_benchmarks.stagedir, tarball)
        self.prebuild_cmds = [
            "module load toolchain/foss/2023b",
            f"cp {fullpath} {self.stagedir}",
            f"tar xzf {tarball}",
            f"cd {self.build_prefix}",
        ]
        self.build_system.max_concurrency = 8


@rfm.simple_test
class OMB_Latency(rfm.RunOnlyRegressionTest):
    # sweep three binary sources and four placements
    flavour = parameter(["generic", "easybuild", "eessi"])
    placing = parameter(["intra_numa", "cross_numa", "cross_socket", "inter_node"])

    descr = "OSU latency 8 KiB"
    valid_systems = ["aion:batch", "iris:batch"]
    valid_prog_environs = ["foss"]
    source_build_binary = fixture(OMB_GenericBuild, scope="environment")
    source_build_binary1 = fixture(OMB_EasyBuild, scope="environment")
    # eessi_build_binary = fixture(OMB_GenericBuild, scope="environment")
    # --- run parameters -----------------------------------------
    num_tasks = 2
    message_size = 8192
    metric = "osu_latency"

    @run_before("run")
    def set_launcher_opts(self):
        # node / binding policy
        if self.placing == "inter_node":
            self.num_tasks_per_node = 1
            self.job.options = ["--nodes=2"]
            self.job.launcher.options = ["--cpu-bind=cores"]
        else:
            self.num_tasks_per_node = self.num_tasks
            self.exclusive_access = True
            config = self.current_system.json()
            bindings = dict(config["env_vars"])
            bind = bindings[self.placing]
            self.job.options = ["--nodes=1"]
            self.job.launcher.options = [f"--cpu-bind={bind}"]

    @run_before("run")
    def set_executable(self):
        # self.executable = str(_binary_path("lat", self.flavour, build))
        if self.flavour == "generic":
            self.executable = os.path.join(
                self.source_build_binary.stagedir,
                self.source_build_binary.build_prefix,
                "c",
                "mpi",
                "pt2pt/standard",
                self.metric,
            )

        if self.flavour == "easybuild":
            self.modules = self.source_build_binary1.build_system.generated_modules
            self.executable = self.metric
        if self.flavour == "eessi":
            self.modules = ["EESSI", "OSU-Micro-Benchmarks/7.2-gompi-2023b"]
            self.executable = self.metric
        # when using "-x" "-i" parameter in iris with easybuild, it because of the compatibility of ABI
        self.executable_opts = (
            [str(self.message_size)]
            if self.current_system.name == "iris" and self.flavour == "easybuild"
            else ["-x", "3", "-i", "10", "-m", str(self.message_size)]
        )

    @run_after("run")
    def set_sanity(self):
        self.sanity_patterns = sn.assert_found(r"^8192\s+\S+", self.stdout)

    @run_before("performance")
    def set_perf_and_ref(self):
        perf = sn.extractsingle(r"^8192\s+(\S+)", self.stdout, 1, float)

        ref = {
            "inter_node": 4.2,
            "cross_socket": 6.2,
            "cross_numa": 4.3,
            "intra_numa": 2.4,
        }[self.placing]

        # 20 % tolerance (i.e., ±0.20 of the reference)
        tol = 0.20

        self.reference = {
            "aion:batch": {"latency": (ref, -tol, tol, "us")},
            "*": {"latency": (ref, -1.0, 10.0, "us")},  # wide open
        }

        self.perf_patterns = {"latency": perf}
