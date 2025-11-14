import flet as ft, pty, threading, os
from view.BaseView import BaseView
from Core import System
from Events import AppEvents


class TerminalView(BaseView):
    def __init__(self, page: ft.Page, system: System, events: AppEvents):
        super().__init__(page=page, system=system, events=events)
        
        self.title = "Терминал"

    def on_mounted(self):
        self.exit_event = threading.Event()

        # создание терминала
        self.pid, self.master_fd = pty.fork()

        if self.pid == 0:  # Дочерний процесс
            # запустить оболочку bash, заменяющую текущий дочерний процесс
            os.execvp('bash', ['bash'])
            os._exit(1) # Этот код не должен выполниться, если execvp сработал

        self.events.terminal_message.subscribe(self.on_message)

        self.read_thread = threading.Thread(target=self.read_output)
        self.read_thread.daemon = True
        self.read_thread.start()

        self.build_view()

    def on_unmount(self):
        # Сигнализировать потоку о завершении
        self.exit_event.set()
        
        # Завершить дочерний процесс bash
        try:
            os.kill(self.pid, 15)  # Отправить сигнал SIGTERM
        except ProcessLookupError:
            pass  # Процесс мог уже завершиться

        self.events.terminal_message.unsubscribe(self.on_message)
        os.close(self.master_fd)

    def build_view(self):
        self.terminal_output = ft.Text(
            "", selectable=True, no_wrap=False, font_family="monospace", color=ft.Colors.WHITE
        )
        self.output_view = ft.ListView(
            expand=True, auto_scroll=True, controls=[self.terminal_output], height=350
        )

        self.input_field = ft.TextField(
            hint_text="Введите команду и нажмите Enter",
            autofocus=True,
            multiline=False,
            on_submit=lambda e: self.send_command(e.control.value),
        )

        self.view = ft.Column(
            expand=True,
            controls=[
                ft.Container(
                    content=self.output_view, expand=True, bgcolor=ft.Colors.BLACK
                ),
                self.input_field,
            ],
        )

    def send_command(self, command):
        """Отправляет команду в терминал."""
        full_command = command + "\n"
        os.write(self.master_fd, full_command.encode("utf-8"))
        self.input_field.value = ""
        self.input_field.focus()
        self.page.update()

    def read_output(self):
        """Читает вывод из терминала в отдельном потоке."""
        while not self.exit_event.is_set():
            try:
                output = os.read(self.master_fd, 65536)
                if output:
                    self.events.terminal_message.trigger(
                        output.decode("utf-8", errors="ignore")
                    )
                else:  # Если прочитано 0 байт, значит дочерний процесс завершился
                    break
            except OSError:
                # Исключение возникнет, когда дескриптор будет закрыт в on_disconnect
                break
        self.events.terminal_message.trigger(f"\n[Процесс завершен]")

    def on_message(self, message: str):
        """Получает сообщение от потока и обновляет UI."""
        self.terminal_output.value += message
        self.page.update()
