from script.utils.shell import run_sp
from script.utils.json_tools import seek_modify
import os
import subprocess
import polling2
import json
import argparse

with open('config.json', 'r') as f:
    conf = json.load(f)

parser = argparse.ArgumentParser(description='Initiates setup for pymesh docker container sandbox.')
parser.add_argument('--compile-new-py', nargs='?', const=False, default=False, type=bool)
parser.add_argument('--python-version', nargs='?', const=conf['Python']['Ver'], default=conf['Python']['Ver'],
                    type=str)
parser.add_argument('--wipe-container', nargs='?', const=False, default=False, type=bool)
args = parser.parse_args()


if __name__ == "__main__":

    # Windows setup
    if os.name == 'nt':

        if args.wipe_container:
            seek_modify('config.json', None, 'Meta', 'ContainerId')

        def check_daemon_alive():
            return not subprocess.run('docker ps', shell=True, stdout=subprocess.DEVNULL,
                                      stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL).returncode

        # Poll until the daemon starts
        @polling2.poll_decorator(step=conf['Meta']['DaemonPollRate'], timeout=conf['Meta']['DaemonTimeout'],
                                 check_success=lambda d: d)
        def poll_daemon_start():
            return check_daemon_alive()


        try:
            if not check_daemon_alive():
                subprocess.Popen(f'{os.environ["ProgramFiles"]}\Docker\Docker\Docker Desktop.exe', shell=True)
                poll_daemon_start()
        except TimeoutError as e:
            raise RuntimeError(e)

        run_sp('powershell', '& ''./script/win/docker_setup.ps1''', f'{args.compile_new_py}',
               f'{args.python_version}')
