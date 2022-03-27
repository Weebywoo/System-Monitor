#!/usr/bin/env python
# ===== IMPORTS ===== #
from system_monitor.lib.system_monitor import SystemMonitor
import os
import time


def main() -> None:
    app = SystemMonitor()

    while(True):
        os.system("mode con cols=83 lines=22")
        os.system("cls")
        app.print()
        app.update()
        time.sleep(1)


if __name__ == "__main__":
    main()
