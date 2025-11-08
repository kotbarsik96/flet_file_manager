from events.Event import Event
from Core import System
import time
from utils.time import format_date

class AppEvents:
    def __init__(self, system: System):
        self.route_changed = Event()
        self.system = system
        
        self.log_events()
        
    def log_events(self):
        self.route_changed.subscribe(lambda route, **_: self.system.logger.write_log(f"Переход на маршрут: {route} | {format_date(time.time())}"))


class Event:
    def __init__(self):
        self.listeners = []

    def subscribe(self, cb: callable):
        self.listeners.append(cb)

    def unsubscribe(self, cb: callable):
        self.listeners.remove(cb)

    def trigger(self, *args, **kwargs):
        for cb in self.listeners:
            cb(*args, **kwargs)
