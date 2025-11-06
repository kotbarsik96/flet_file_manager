import flet as ft
from Core import AppContext
from router.views.BaseView import BaseView
from router.views.FolderView import FolderView
from router.views.TrashView import TrashView

class RouterBody:
    app: AppContext
    body: ft.Container
    current_view: BaseView

    def __init__(self, app: AppContext):
        self.app = app
        self.body = ft.Container(
            margin=ft.margin.only(bottom=50, top=25)
        )
        
    def get_static_routes(self):
        return {
            f"{self.app.app_root_path}trash": TrashView
        }

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

        self.body.content = self.create_view(route).view
        self.body.update()
        events.route_changed.trigger(
            route=route.route, is_forward=is_forward, is_backward=is_backward
        )
        
    def create_view(self, route):
        static_routes = self.get_static_routes()
        view = None
        
        if(route.route in static_routes):
            view = static_routes[route.route](self.app)
        else:
            view = FolderView(self.app)
        
        return view