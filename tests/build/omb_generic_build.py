import os, pathlib
import reframe as rfm
import reframe.utility.typecheck as typ
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


@rfm.simple_test
class OMB_GenericBuild(rfm.CompileOnlyRegressionTest):
    descr = "Build OMB benchmarks"
    valid_systems = ["iris:batch", "aion:batch"]
    build_system = "Autotools"
    valid_prog_environs = ["system-gcc"]
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
        _p = os.path.join(
            self.stagedir, self.build_prefix, "c", "mpi", "pt2pt/standard"
        )

        self.postbuild_cmds = [f'echo "{_p}" > omb.path', "echo 'hello world'"]

    @run_after("compile")
    def validate_compile(self):
        path_file = pathlib.Path(self.stagedir) / "omb.path"

        return sn.assert_found(r"mpi", str(path_file))
