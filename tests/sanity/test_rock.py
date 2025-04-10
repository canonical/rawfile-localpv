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
    args = ["pebble", "enter", "-v", "start", "rawfile"]
    process = docker_util.run_in_docker(image, args, check_exit_code=False)
    assert process.returncode == 1, "\n".join(process.stderr, process.stdout)
    assert "Configuration file ~/.kube/config not found" in process.stdout
