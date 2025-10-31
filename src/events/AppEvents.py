from events.Event import Event


class AppEvents:
    def __init__(self):
        self.route_changed = Event()
