#!/usr/bin/env python
"""
Creates progress bars for 'SystemMonitor.py
"""


class ProgressBar:

    def __init__(self, max_lenght: int, title: str = "Title", description: str = "") -> None:
        self.max_lenght = max_lenght
        self.title = title
        self.description = description
        self.current_lenght = 0
        self.string = ""
        self.update_progress_bar_string()

    def set_progress_bar(self, new_lenght: float, description: str = None) -> None:
        self.current_lenght = min(new_lenght, self.max_lenght)
        if description != None:
            self.description = description

        self.update_progress_bar_string()

    def update_progress_bar_string(self) -> None:
        percent_float = 100 * (self.current_lenght / self.max_lenght)
        percent_str = f"{round(percent_float, 1)}%".rjust(6)

        infill_colored = self.set_colors(self.current_lenght)
        self.string = f"{self.title} [{infill_colored}] {percent_str}"

        if self.description:
            self.string += f" | {self.description}"

    def udpate(self, step_size: float = 0) -> None:
        self.current_lenght += step_size
        self.update_progress_bar_string()

    def set_colors(self, current_lenght: int) -> str:
        current_lenght_int = int(round(current_lenght))
        colored_string = ""

        for index in range(1, current_lenght_int + 1):
            current_percent = index / self.max_lenght

            if 0.0 <= current_percent <= 0.33:
                r, g, b = (0, 255, 0)
            elif 0.33 < current_percent <= 0.66:
                r, g, b = (255, 255, 0)
            elif 0.66 < current_percent <= 1.0:
                r, g, b = (255, 0, 0)

            colored_string += f"\u001b[38;2;{r};{g};{b}m|"

        colored_string += (
            '\x1b[38;2;63;63;63m|' * (self.max_lenght - current_lenght_int)
            + "\u001b[38;2;255;255;255m"
        )

        return colored_string


if __name__ == "__main__":
    pb = ProgressBar(20, "Title", "Description")
    pb.set_progress_bar(17, "dada")
    progressbar = pb.string

    print(progressbar)
