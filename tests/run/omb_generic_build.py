import os
import reframe as rfm
import reframe.utility.sanity as sn


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
