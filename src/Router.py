import flet as ft
from Events import AppEvents
from view.FolderView import FolderView
from Core import System
from view.BaseView import BaseView
from view.TerminalView import TerminalView


class Router:
    history_backward = []
    history_forward = []
    current_route: str | None = None
    created_views: dict[str, BaseView]
    view: BaseView
    routes_map = {"__TerminalView__": TerminalView}

    def __init__(self, page: ft.Page, events: AppEvents, system: System):
        self.page = page
        self.events = events
        self.system = system
        self.body = ft.Container(margin=ft.margin.only(bottom=50, top=25))
        self.created_views = {}
        self.view = None

    def on_route_change(self, route: ft.RouteChangeEvent):
        prev_route = self.get_previuos_route()
        next_route = self.get_next_route()

        is_forward = False
        is_backward = route.route and prev_route and route.route == prev_route
        is_forward = route.route and next_route and route.route == next_route

        # обычный переход - не назад и не вперёд
        if not is_forward and not is_backward:
            if self.current_route:
                self.history_backward.append(self.current_route)
            self.history_forward.clear()
            self.current_route = route.route
        # переход назад
        elif is_backward:
            self.history_forward.insert(0, self.current_route)
            self.current_route = prev_route
            self.history_backward.pop()
        # переход вперёд
        elif is_forward:
            self.history_backward.append(self.current_route)
            self.current_route = next_route
            self.history_forward.pop(0)

        self.change_view(route)
        self.events.route_changed.trigger(
            route=route.route, is_forward=is_forward, is_backward=is_backward
        )

    def change_view(self, route: ft.RouteChangeEvent):
        view_class = FolderView
        view_name = "FolderView"
        if route.route in self.routes_map:
            view_class = self.routes_map[route.route]
            view_name = route.route

        # создать и кэшировать view, если он ещё не был создан
        if not self.created_views.get(view_name):
            self.created_views[view_name] = view_class(
                page=self.page, system=self.system, events=self.events
            )

        if self.view:
            self.view.on_unmount()

        self.view = self.created_views[view_name]
        self.view.on_mounted()
        self.body.content = self.view.view
        self.body.update()

    def get_previuos_route(self):
        if len(self.history_backward) > 0:
            return self.history_backward[-1]
        else:
            return None

    def get_next_route(self):
        if len(self.history_forward) > 0:
            return self.history_forward[0]
        else:
            return None

    def go_prev_route(self):
        if len(self.history_backward) > 0 and self.history_backward[-1]:
            self.page.go(self.history_backward[-1])

    def go_next_route(self):
        if len(self.history_forward) > 0 and self.history_forward[0]:
            self.page.go(self.history_forward[0])
