import pathlib, reframe as rfm


def _binary_path(test, flavour, build):
    if flavour == "eessi":
        return "osu_latency" if test == "lat" else "osu_bw"

    build_dir = pathlib.Path(open(build.stagedir / "omb.path").read().strip())
    return str(build_dir / ("osu_latency" if test == "lat" else "osu_bw"))
