import argparse
from functools import partial

from lya import lya
from rx import Observable

from command_watcher.launcher import observe_process
from command_watcher.observer import CommandObserver


cfg = lya.AttrDict.from_yaml('../config.yaml')


def start():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", type=str)
    args = parser.parse_args()

    Observable.create(partial(observe_process, command=args.command))\
        .subscribe(CommandObserver(cfg.telegram.bot_token, cfg.telegram.chat_id))


if __name__ == '__main__':
    start()