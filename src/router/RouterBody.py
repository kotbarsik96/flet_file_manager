import flet as ft
from AppContext import AppContext
from router.views.FolderView import FolderView


class RouterBody:
    app: AppContext
    body: ft.Container

    def __init__(self, app: AppContext):
        self.app = app
        self.body = ft.Container(
            margin=ft.margin.only(bottom=50, top=25)
        )

    def route_change(self, route):
        fletRouter = self.app.router
        events = self.app.events

        prev_route = fletRouter.get_previuos_route()
        next_route = fletRouter.get_next_route()

        is_forward = False
        is_backward = route.route and prev_route and route.route == prev_route
        is_forward = route.route and next_route and route.route == next_route

        # обычный переход - не назад и не вперёд
        if not is_forward and not is_backward:
            if fletRouter.current_route:
                fletRouter.history_backward.append(fletRouter.current_route)
            fletRouter.history_forward.clear()
            fletRouter.current_route = route.route
        # переход назад
        elif is_backward:
            fletRouter.history_forward.insert(0, fletRouter.current_route)
            fletRouter.current_route = prev_route
            fletRouter.history_backward.pop()
        # переход вперёд
        elif is_forward:
            fletRouter.history_backward.append(fletRouter.current_route)
            fletRouter.current_route = next_route
            fletRouter.history_forward.pop(0)

        self.body.content = FolderView(self.app).view
        self.body.update()
        events.route_changed.trigger(
            route=route.route, is_forward=is_forward, is_backward=is_backward
        )
