import flet as ft
from AppContext import AppContext

class ViewBase:
    view: ft.Control
    
    def __init__(self, app: AppContext):        
        self.app = app
        self.build_view()