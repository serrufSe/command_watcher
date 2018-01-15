from typing import List, Any

import telegram
from logging import getLogger
from rx import Observer


logger = getLogger('observer')


class CommandObserver(Observer):

    def __init__(self, bot_token: str, chat_id: str) -> None:
        super().__init__()
        self._chat_id = chat_id
        self._tg = telegram.Bot(token=bot_token)

    def on_next(self, value: Any):
        self._tg.send_message(self._chat_id, "Trigger")
        print("Received {0}".format(value))

    def on_completed(self):
        print("Done!")

    def on_error(self, error):
        print("Error Occurred: {0}".format(error))