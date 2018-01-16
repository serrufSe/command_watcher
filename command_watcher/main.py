import argparse
from functools import partial

from lya import lya
from rx import Observable
from rx.concurrency import timeout_scheduler


from command_watcher.launcher import observe_process
from command_watcher.observer import CommandObserver


def start():
    parser = argparse.ArgumentParser()
    parser.add_argument("--command", type=str)
    parser.add_argument("--config", type=str)
    args = parser.parse_args()

    cfg = lya.AttrDict.from_yaml(args.config)

    Observable.create(partial(observe_process, command=args.command))\
        .buffer_with_time(cfg.timespan, scheduler=timeout_scheduler)\
        .where(lambda buffer: len(buffer) >= cfg.count_trigger)\
        .subscribe(CommandObserver(cfg.telegram.bot_token, cfg.telegram.chat_id, cfg.video_source))


if __name__ == '__main__':
    start()