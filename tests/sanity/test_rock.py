#
# Copyright 2024 Canonical, Ltd.
#
import subprocess
import pytest
from k8s_test_harness.util import docker_util, env_util


@pytest.mark.parametrize("image_version", ["0.8.0"])
def test_sanity(image_version):
    rock = env_util.get_build_meta_info_for_rock_version(
        "rawfile-localpv", image_version, "amd64"
    )
    image = rock.image
    args = ["python3", "-c", "import app.consts; print(app.consts.PROVISIONER_VERSION)"]
    try:
        process = docker_util.run_in_docker(image, args)
    except subprocess.CalledProcessError as e:
        assert False, e.stderr or e.stdout
    assert image_version in process.stdout, process.stderr
