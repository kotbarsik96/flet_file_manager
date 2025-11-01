import os


def format_bytes_to_string(file_size_bytes: int, round_to_decimals: int = 0) -> str:
    num = file_size_bytes

    for unit in ("Байт", "КБ", "МБ", "ТБ"):
        if abs(num) < 1024.0:
            if round_to_decimals > 0: 
                num = round(num, round_to_decimals)
            else: 
                num = round(num)
            return f"{num} {unit}"
        num = num / 1024.0


def get_dir_size(directoryPath: str) -> int:
    total = 0

    try:
        with os.scandir(directoryPath) as it:
            for entry in it:
                try:
                    if entry.is_dir():
                        total += get_dir_size(entry.path)
                    else:
                        total += entry.stat().st_size
                except (PermissionError, FileNotFoundError):
                    continue
    except (PermissionError, FileNotFoundError):
        return 0

    return total
