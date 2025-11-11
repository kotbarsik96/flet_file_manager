import flet as ft
import os
import pty
import threading
import subprocess

def main(page: ft.Page):
    page.title = "Flet Terminal"

    exit_event = threading.Event()

    terminal_output = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True, auto_scroll=True)
    command_input = ft.TextField(
        hint_text="Введите команду...",
        expand=True,
        on_submit=lambda e: send_command(e.control.value),
        text_size=14,
        border_color="transparent",
    )

    # Используем pty.fork() для правильной настройки терминала
    pid, master_fd = pty.fork()

    if pid == 0:  # Дочерний процесс
        # Запускаем оболочку bash, которая заменяет текущий дочерний процесс
        # pty.fork() уже позаботился о настройке терминала
        os.execvp('bash', ['bash'])
        os._exit(1) # Этот код не должен выполниться, если execvp сработал

    # --- Родительский процесс ---
    def read_output(master_fd):
        """Читает вывод из терминала в отдельном потоке."""
        while not exit_event.is_set():
            try:
                # Увеличиваем размер буфера для чтения
                output = os.read(master_fd, 65536)
                if output:
                    page.pubsub.send_all(output.decode('utf-8', errors='ignore'))
                else:
                    break
            except OSError:
                break
        page.pubsub.send_all(f"\n[Процесс завершен]")

    def on_message(message):
        """Получает сообщение от потока и обновляет UI."""
        terminal_output.controls.append(ft.Text(message, font_family="monospace", size=14))
        page.update()

    page.pubsub.subscribe(on_message)

    read_thread = threading.Thread(target=read_output, args=(master_fd,))
    read_thread.daemon = True
    read_thread.start()

    def on_disconnect(e):
        """Очистка при закрытии окна."""
        exit_event.set()
        # Завершаем дочерний процесс bash
        try:
            os.kill(pid, 15) # Отправляем сигнал SIGTERM
        except ProcessLookupError:
            pass # Процесс мог уже завершиться
        os.close(master_fd)


    page.on_disconnect = on_disconnect

    def send_command(command):
        """Отправляет команду в терминал."""
        full_command = command + "\n"
        os.write(master_fd, full_command.encode('utf-8'))
        command_input.value = ""
        page.update()

    page.add(
        ft.Container(
            content=terminal_output,
            border=ft.border.all(1, ft.Colors.OUTLINE),
            border_radius=ft.border_radius.all(5),
            padding=10,
            expand=True,
        ),
        ft.Row([ft.Text(">"), command_input]),
    )

    page.window_width = 800
    page.window_height = 600
    page.update()

if __name__ == "__main__":
    ft.app(target=main)