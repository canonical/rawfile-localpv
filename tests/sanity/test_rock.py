#
# Copyright 2024 Canonical, Ltd.
#
from pathlib import Path

import pytest
import yaml
from k8s_test_harness.util import docker_util, env_util


TEST_PATH = Path(__file__)
REPO_PATH = TEST_PATH.parent.parent.parent


def _image_versions():
    all_rockcrafts = REPO_PATH.glob("**/rockcraft.yaml")
    yamls = [yaml.safe_load(rock.read_bytes()) for rock in all_rockcrafts]
    return [rock["version"] for rock in yamls]


@pytest.mark.parametrize("image_version", _image_versions())
def test_sanity(image_version):
    rock = env_util.get_build_meta_info_for_rock_version(
        "rawfile-localpv", image_version, "amd64"
    )
    image = rock.image
    args = ["python3", "-c", "import app.consts; print(app.consts.PROVISIONER_VERSION)"]
    try:
        process = docker_util.run_in_docker(image, args)
    except docker_util.subprocess.CalledProcessError as e:
        assert False, e.stderr or e.stdout
    assert image_version in process.stdout, process.stderr
