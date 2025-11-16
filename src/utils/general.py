import flet as ft
import subprocess
import shutil
from Router import Router
import threading


def open_os_terminal(page: ft.Page, router: Router):
    msg = "Терминал открыт через файловый менеджер"

    if shutil.which("gnome-terminal"):
        return subprocess.Popen(
            [
                "gnome-terminal",
                "--",
                "bash",
                "-c",
                f"echo '{msg}'; cd {router.current_route}; exec bash",
            ]
        )
    elif shutil.which("xterm"):
        return subprocess.Popen(
            [
                "xterm",
                "-e",
                f"bash -lc echo '${msg}'; cd {router.current_route}; exec bash",
            ]
        )
    else:
        error_msg = "Не найден установленный терминал"
        open_info_dialog(
            page=page,
            title=ft.Text("Ошибка"),
            content=ft.Text(error_msg, size=18),
        )
        raise RuntimeError(error_msg)


def open_info_dialog(page: ft.Page, title: ft.Text, content: ft.Control):
    dlg = ft.AlertDialog(
        title,
        content,
        actions=[ft.TextButton("Закрыть", on_click=lambda _: page.close(dlg))],
    )
    page.open(dlg)
    return dlg


def debounce(wait_seconds: int):
    def decorator(fn):
        def debounced(*args, **kwargs):
            def call_fn():
                fn(*args, **kwargs)

            try:
                debounced.timer.cancel()
            except AttributeError:
                pass

            debounced.timer = threading.Timer(wait_seconds, call_fn)
            debounced.timer.start()

        return debounced

    return decorator
