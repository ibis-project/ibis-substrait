import os
import subprocess


def build(setup_kwargs):
    if (proto_dir := os.environ.get("PROTO_DIR")) is not None:
        subprocess.run(["./gen-protos.sh", proto_dir], check=True)
