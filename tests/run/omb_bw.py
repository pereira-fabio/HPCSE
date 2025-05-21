import reframe as rfm, reframe.utility.sanity as sn
import os, pathlib
from omb_generic_build import OMB_GenericBuild
from omb_easybuild_build import OMB_EasyBuild


@rfm.simple_test
class OMB_Latency(rfm.RunOnlyRegressionTest):
    # sweep three binary sources and four placements
    flavour = parameter(["generic", "easybuild", "eessi"])
    placing = parameter(["intra_numa", "cross_numa", "cross_socket", "inter_node"])

    descr = "OSU bandwidth 1MB"
    valid_systems = ["aion:batch", "iris:batch"]
    valid_prog_environs = ["foss"]
    source_build_binary = fixture(OMB_GenericBuild, scope="environment")
    source_build_binary1 = fixture(OMB_EasyBuild, scope="environment")
    # eessi_build_binary = fixture(OMB_GenericBuild, scope="environment")
    # --- run parameters -----------------------------------------
    num_tasks = 2
    message_size = 1048576
    metric = "osu_bw"

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
        self.executable_opts = (
            [str(self.message_size)]
            if self.current_system.name == "iris" and self.flavour == "easybuild"
            else ["-x", "3", "-i", "10", "-m", str(self.message_size)]
        )

    @run_after("run")
    def set_sanity(self):
        self.sanity_patterns = sn.assert_found(r"^1048576\s+\S+", self.stdout)

    @run_before("performance")
    def set_perf_and_ref(self):
        perf = sn.extractsingle(r"^1048576\s+(\S+)", self.stdout, 1, float)

        if self.placing == "inter_node":
            ref_bw, tol = 12300, 0.05
        elif self.placing == "cross_socket":
            ref_bw, tol = 9000, 0.15
        elif self.placing == "cross_numa":
            ref_bw, tol = 12000, 0.20
        elif self.placing == "intra_numa":
            ref_bw, tol = 14000, 0.10

        self.reference = {
            "aion:batch": {"bandwidth": (ref_bw, -tol, tol, "MB/s")},
            "*": {"bandwidth": (ref_bw, -1.0, 10.0, "MB/s")},
        }

        self.perf_patterns = {"bandwidth": perf}
