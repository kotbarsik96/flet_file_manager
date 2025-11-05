import os


def format_bytes_to_string(file_size_bytes: int, round_to_decimals: int = 0) -> str:
    num = file_size_bytes

    for unit in ("Байт", "КБ", "МБ", "ГБ", "ТБ"):
        if abs(num) < 1024.0:
            if round_to_decimals > 0:
                num = round(num, round_to_decimals)
            else:
                num = round(num)
            return f"{num} {unit}"
        num = num / 1024.0


def get_dir_size(directoryPath: str) -> int:
    size = 0

    try:
        for el in os.scandir(directoryPath):
            size += os.path.getsize(el)
    except (FileNotFoundError, PermissionError):
        pass

    return size
