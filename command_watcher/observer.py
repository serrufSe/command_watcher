from typing import Any
from io import BytesIO

import telegram
from logging import getLogger, StreamHandler, DEBUG
from rx import Observer
import cv2


logger = getLogger('observer')
logger.setLevel(DEBUG)
logger.addHandler(StreamHandler())


class CommandObserver(Observer):

    def __init__(self, bot_token: str, chat_id: str, video_source) -> None:
        super().__init__()
        self._chat_id = chat_id
        self._tg = telegram.Bot(token=bot_token)
        self._cap = cv2.VideoCapture(video_source)

    def on_next(self, value: Any):
        self._tg.send_message(self._chat_id, "Trigger")

        success, frame = self._cap.read()

        if success:
            bio = BytesIO(cv2.imencode(".jpg", frame)[1].tostring())

            self._tg.send_photo(self._chat_id, bio)
        else:
            logger.info('opencv read error')

        logger.info("Received {0}".format(value))

    def on_completed(self):
        logger.info('Done!')

    def on_error(self, error):
        logger.error("Error Occurred: {0}".format(error))