import time, threading


def format_seconds(seconds: float | int):
    minutes = seconds / 60
    hours = minutes / 60
    days = hours / 24
    
    str = ""
    if(days > 0):
        str += f"{days} дн."
    if(hours > 0):
        str += f"{hours} ч."
    if(minutes > 0):
        str += f"{minutes} мин."
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
