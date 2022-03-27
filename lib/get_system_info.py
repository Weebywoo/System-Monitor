#!/usr/bin/env python
# ===== IMPORTS ===== #
import itertools as itt
import platform
import psutil


def get_sys_info() -> dict:
    system = platform.uname()
    user_names = [user.name for user in psutil.users()]
    users = ", ".join(user_names)

    if len(users) > 68:
        users = ", ".join(users[:5].split(", ")[:-1]) + \
            f" ... {len(user_names) - len(users.split(', '))} more"

    return {"Users": users,
                   "System": system.system,
                   "Node": system.node,
                   "Release": system.release,
                   "Version": system.version,
                   "Machine": system.machine,
                   "Processor": system.processor}


def get_cpu_usage() -> list:
    return psutil.cpu_percent(percpu=True, interval=1)


def get_memory_usage() -> dict:
    memory = psutil.virtual_memory()
    return {
        "total": memory.total,
        "used": memory.used,
        "percent": memory.percent
    }


def get_disk_usage() -> dict:
    disks = psutil.disk_partitions()
    disk_usage = {}
    for disk in disks:
        usage = psutil.disk_usage(disk.mountpoint)
        disk_usage[disk.mountpoint[:-1]] = {
            "total": usage.total,
            "used": usage.used,
            "percent": usage.percent
        }

    return disk_usage


def get_scaled_bytes(bytes: int = 0) -> str:
    factor = 1024

    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}B"

        bytes /= factor

    return bytes


def get_core_count(core_count: int = 1) -> int:
    factor = 10

    for len in itt.count(1):
        if core_count < factor:
            return len

        core_count /= factor
