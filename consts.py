import os

PROVISIONER_NAME = os.getenv("PROVISIONER_NAME", "rawfile.csi.openebs.io")
PROVISIONER_VERSION = "0.8.2"
DATA_DIR = "/data"
CONFIG = {}
D_PERMS = 0o700
F_PERMS = 0o600
OWNER_UMASK = 0o077
RESOURCE_EXHAUSTED_EXIT_CODE = 101
VOLUME_IN_USE_EXIT_CODE = 102
