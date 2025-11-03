import time, threading
from math import floor


def format_seconds(seconds: float | int):
    seconds = floor(seconds)

    days = floor(seconds / (24 * 3600))
    seconds = seconds - days * 24 * 3600
    
    hours = floor(seconds / 3600)
    seconds = seconds - hours * 3600
    
    minutes = floor(seconds / 60)
    seconds = seconds - minutes * 60

    str = ""
    if days > 0:
        str += f"{days} дн. "
    if hours > 0:
        str += f"{hours} ч. "
    if minutes > 0:
        str += f"{minutes} мин. "
    str += f"{seconds} сек."

    return str


class SetInterval:
    def __init__(self, callback: callable, interval: int):
        self.callback = callback
        self.interval = interval
        self.stopEvent = threading.Event()
        thread = threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self):
        nextTime = time.time() + self.interval
        while not self.stopEvent.wait(nextTime - time.time()):
            nextTime += self.interval
            self.callback()

    def cancel(self):
        self.stopEvent.set()
