import os
import subprocess
import tempfile
from pathlib import Path

from util import run


def be_absent(path):
    path = Path(path)
    if path.is_symlink():
        path.unlink()
    elif path.is_file():
        path.unlink()
    elif path.is_dir():
        path.rmdir()
        # XXX: should we `shutil.rmtree(path)` instead?
    elif not path.exists():
        return
    else:
        raise Exception("Unknown file type")


def be_symlink(path, to):
    path = Path(path)
    to = Path(to)
    if path.is_symlink():
        if os.readlink(path) == str(to):
            return
    be_absent(path)
    path.symlink_to(to)


def be_mounted(dev, mountpoint):
    dev = Path(dev).resolve()
    mountpoint = Path(mountpoint)

    if mountpoint.is_mount():
        if True:  # TODO: verify that the right device is mounted
            return
        # noinspection PyUnreachableCode
        be_unmounted(mountpoint)

    fs = current_fs(dev)
    if fs == "ext4":
        run(["mount", "-t", "ext4", str(dev), str(mountpoint)])
    elif fs == "btrfs":
        run(["mount", "-t", "btrfs", "-o", "flushoncommit", str(dev), str(mountpoint)])
    elif fs == "xfs":
        run(["mount", "-t", "xfs", str(dev), str(mountpoint)])
    else:
        raise Exception(f"Unsupported fs type: {fs}")


def be_unmounted(path):
    path = Path(path)
    while path.is_mount():
        run(["umount", str(path)])


def current_fs(device):
    res = subprocess.run(
        ["blkid", "-o", "value", "-s", "TYPE", str(device)], capture_output=True
    )
    if res.returncode == 2:  # specified token was not found
        return None
    return res.stdout.decode().strip()


def be_formatted(dev, fs):
    def init_fs(device):
        if fs == "ext4":
            run(["mkfs.ext4", "-m", "0", str(device)])
        elif fs == "btrfs":
            run(["mkfs.btrfs", str(device)])
            tmp_mnt = tempfile.mkdtemp(prefix="mnt-")
            default_subvol = f"{tmp_mnt}/default"
            # Multi-step btrfs setup requires a shell script; inputs are
            # locally-generated tempdir paths, not user-controlled.
            run(
                f"""
                set -ex
                mkdir -p {tmp_mnt}
                mount -t btrfs {device} {tmp_mnt}
                btrfs subvolume create {default_subvol}
                btrfs subvolume set-default {default_subvol}
                umount {tmp_mnt}
                rmdir {tmp_mnt}
                """
            )
        elif fs == "xfs":
            run(["mkfs.xfs", str(device)])
        else:
            raise Exception(f"Unsupported fs type: {fs}")

    dev = Path(dev).resolve()
    current = current_fs(dev)
    if current is None:
        init_fs(dev)
    else:
        if current != fs:
            raise Exception(f"Existing filesystem does not match: {current}/{fs}")


def be_fs_expanded(dev, path):
    dev = Path(dev).resolve()
    fs = current_fs(dev)
    path = Path(path).resolve()
    if fs == "ext4":
        run(["resize2fs", str(dev)])
    elif fs == "btrfs":
        run(["btrfs", "filesystem", "resize", "max", str(path)])
    elif fs == "xfs":
        run(["xfs_growfs", "-d", str(path)])
    else:
        raise Exception(f"Unsupported fsType: {fs}")
