#!/usr/bin/env python3

units = {"B": 1, "KB": 1 << 10, "MB": 1 << 20, "GB": 1 << 30}


def to_bytes(size):
    if len(size.split()) == 1:
        return int(size.strip())
    number, unit = [string.strip() for string in size.split()]
    return int(float(number)*units[unit.upper()])


def to_human_readable_size(size, decimal_places=2):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if size < 1024.0 or unit == 'PB':
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"
