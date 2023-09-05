import subprocess
import sys
from subprocess import Popen
from typing import Any


def run_sp(*args, **kwargs) -> Popen[bytes] | Popen[Any]:
    pid = subprocess.Popen(args, **kwargs, stdout=subprocess.PIPE)
    for bs in iter(pid.stdout.readline, b''):
        sys.stdout.buffer.write(bs)
        sys.stdout.flush()
    return pid
