import flet as ft

class FletRouter:
    history_backward = []
    history_forward = []
    current_route: str | None = None

    def __init__(self, page: ft.Page):
        self.page = page

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
