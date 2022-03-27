#!/usr/bin/env python
"""
Provides a rough overview over system infortmation such as system, system 
version, username and machinename as well as general system usage such as 
logic cpu cores, ram and drives/disks.
"""
# ===== IMPORTS ===== #
import psutil
import cursor
import ctypes
import time
import os

# ===== CUSTOM IMPORTS ===== #
from system_monitor.lib.get_system_info import (
    get_core_count,
    get_cpu_usage,
    get_disk_usage,
    get_memory_usage,
    get_scaled_bytes,
    get_sys_info)
from system_monitor.lib.progress_bar import ProgressBar


class SystemMonitor:

    def __init__(self) -> None:
        ctypes.windll.kernel32.SetConsoleTitleW(
            "System Ressource Monitor by Emily")
        os.chdir("\\".join(__file__.split("\\")[:-1]))
        cursor.hide()

        self.core_progress_bars, self.memory_progress_bar, self.disk_progress_bars = self.create_progress_bars()
        self.sys_info = get_sys_info()

    def create_progress_bars(self) -> ProgressBar:
        # CPU Progress Bars
        core_count = psutil.cpu_count()
        lenght_core_digit = get_core_count(core_count)
        core_progress_bars = [ProgressBar(
            20, f"Logic {f'{i}'.rjust(lenght_core_digit)}") for i in range(core_count)]
        core_progress_bars.append(ProgressBar(50, "Total CPU Usage"))

        # Memory Progress Bar
        memory_progress_bar = ProgressBar(42, "Used", " 00.00B / 00.00B")

        # Partition Progress Bars
        disk_partitions = psutil.disk_partitions()
        disk_progress_bars = [ProgressBar(
            41, partition.mountpoint.strip("\\"), "0000.00B / 0000.00B") for partition in disk_partitions]

        return core_progress_bars, memory_progress_bar, disk_progress_bars

    def print(self) -> None:
        print("\u001b[38;2;255;255;255m")
        title = f"  ╔{'═' * 32} System Info {'═' * 32}╗"
        print(title)
        for information in self.sys_info:
            current_sys_info = f"{information}: {self.sys_info[information]}"
            print(
                f"  ║ {current_sys_info.ljust(76)}║")

        title = f"  ╠{'═' * 33} CPU Info {'═' * 34}╣"
        print(title)

        for index, core_usage in enumerate(self.core_progress_bars[:-1]):
            if index % 2 == 0:
                print("  ║", end=" ")
            print(core_usage.string, end=" ")

            if index % 2 == 1:
                print("║")

        print("  ║", self.core_progress_bars[-1].string, "║")

        title = f"  ╠{'═' * 32} Memory Info {'═' * 32}╣"
        print(title)
        print("  ║", self.memory_progress_bar.string, "║")

        title = f"  ╠{'═' * 33} Disk Info {'═' * 33}╣"
        print(title)
        for disk in self.disk_progress_bars:
            print("  ║", disk.string, "║")
        print(f"  ╚{'═' * 77}╝")

    def update(self) -> None:
        cpu_usage = get_cpu_usage()
        memory_usage = get_memory_usage()
        disk_usage = get_disk_usage()

        for core_pb, core_percent in zip(self.core_progress_bars, cpu_usage):
            new_lenght = 20 * (core_percent / 100)
            core_pb.set_progress_bar(new_lenght)

        self.core_progress_bars[-1].set_progress_bar(
            sum(cpu_usage) / len(cpu_usage), "")

        new_lenght = 42 * (memory_usage["percent"] / 100)

        memory_usage_used_sized = get_scaled_bytes(
            memory_usage["used"])

        memory_usage_total_sized = get_scaled_bytes(
            memory_usage["total"])

        self.memory_progress_bar.set_progress_bar(
            new_lenght, f"{memory_usage_used_sized} / {memory_usage_total_sized}")

        biggest_disk_int = 0
        biggest_disk_string = ""

        for disk in disk_usage:
            if disk_usage[disk]["total"] > biggest_disk_int:
                biggest_disk_int = disk_usage[disk]["total"]
                biggest_disk_string = get_scaled_bytes(biggest_disk_int)

        for disk_pb, disk in zip(self.disk_progress_bars, disk_usage):
            new_lenght = 40 * (disk_usage[disk]["percent"] / 100)

            disk_usage_used_sized = f"{get_scaled_bytes(disk_usage[disk]['used'])}".rjust(
                len(biggest_disk_string))

            disk_usage_total_sized = f"{get_scaled_bytes(disk_usage[disk]['total'])}".rjust(
                len(biggest_disk_string))

            disk_pb.set_progress_bar(
                new_lenght, f"{disk_usage_used_sized} / {disk_usage_total_sized}")
