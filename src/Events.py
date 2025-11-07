from events.Event import Event


class AppEvents:
    def __init__(self):
        self.route_changed = Event()


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
