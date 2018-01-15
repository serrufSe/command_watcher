import shlex
import subprocess
from rx import Observable


def observe_process(observer: Observable, command: str):
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)

    while True:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            break
        if output:
            observer.on_next(output.decode('cp866'))


    observer.on_completed()