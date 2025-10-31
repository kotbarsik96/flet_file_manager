import flet as ft
from AppContext import AppContext
from router.views.FolderView import FolderView


class RouterBody:
    app: AppContext
    body: ft.Container

    def __init__(self, app: AppContext):
        self.app = app
        self.body = ft.Container()

    def route_change(self, route):
        fletRouter = self.app.router
        events = self.app.events

        prev_route = fletRouter.get_previuos_route()
        next_route = fletRouter.get_next_route()

        # обычный переход - не назад и не вперёд
        if route.route and route.route != prev_route and route.route != next_route:
            if fletRouter.history_current:
                fletRouter.history_backward.append(fletRouter.history_current)
            fletRouter.history_forward.clear()
            fletRouter.history_current = route.route
        # переход назад
        elif prev_route and route.route == prev_route:
            fletRouter.history_forward.insert(0, fletRouter.history_current)
            fletRouter.history_current = prev_route
            fletRouter.history_backward.pop()
        # переход вперёд
        elif next_route and route.route == next_route:
            fletRouter.history_backward.append(fletRouter.history_current)
            fletRouter.history_current = next_route
            fletRouter.history_forward.pop(0)

        self.body.content = FolderView(self.app)
        self.body.update()
        
        # events.route_changed.trigger()
