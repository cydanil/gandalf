import subprocess


def main(*args):
    ret = subprocess.check_output(["sensors"]).decode()
    return ret
