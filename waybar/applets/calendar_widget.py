import calendar
import tkinter as tk
from datetime import datetime

# Catppuccin Mocha
BG = "#1e1e2e"
SURFACE = "#313244"
HOVER = "#45475a"
TODAY = "#89b4fa"
TEXT = "#cdd6f4"
MUTED = "#7f849c"

WIDTH = 360
HEIGHT = 320
RADIUS = 12


def round_rect(canvas, x1, y1, x2, y2, r, **kwargs):
    points = [
        x1 + r,
        y1,
        x2 - r,
        y1,
        x2,
        y1,
        x2,
        y1 + r,
        x2,
        y2 - r,
        x2,
        y2,
        x2 - r,
        y2,
        x1 + r,
        y2,
        x1,
        y2,
        x1,
        y2 - r,
        x1,
        y1 + r,
        x1,
        y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendar")
        self.root.configure(bg=BG)
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.resizable(False, False)

        self.year = datetime.now().year
        self.month = datetime.now().month
        self.today = datetime.now().day

        header = tk.Frame(root, bg=BG)
        header.pack(pady=8)

        tk.Button(
            header,
            text="◀",
            command=self.prev_month,
            bg=BG,
            fg=TEXT,
            bd=0,
            font=("JetBrains Mono", 14),
        ).pack(side="left", padx=12)

        self.title = tk.Label(
            header, fg=TEXT, bg=BG, font=("JetBrains Mono SemiBold", 14)
        )
        self.title.pack(side="left")

        tk.Button(
            header,
            text="▶",
            command=self.next_month,
            bg=BG,
            fg=TEXT,
            bd=0,
            font=("JetBrains Mono", 14),
        ).pack(side="left", padx=12)

        self.canvas = tk.Canvas(root, bg=BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.draw()

    def draw(self):
        self.canvas.delete("all")
        self.title.config(text=f"{calendar.month_name[self.month]} {self.year}")

        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        cell_w = 44
        cell_h = 36
        start_x = 20
        start_y = 20

        for i, d in enumerate(days):
            self.canvas.create_text(
                start_x + i * cell_w + cell_w / 2,
                start_y,
                text=d,
                fill=MUTED,
                font=("JetBrains Mono", 9),
            )

        cal = calendar.monthcalendar(self.year, self.month)

        for r, week in enumerate(cal):
            for c, day in enumerate(week):
                if day == 0:
                    continue

                x1 = start_x + c * cell_w
                y1 = start_y + 12 + r * cell_h
                x2 = x1 + cell_w - 6
                y2 = y1 + cell_h - 6

                is_today = (
                    day == self.today
                    and self.month == datetime.now().month
                    and self.year == datetime.now().year
                )

                color = TODAY if is_today else SURFACE

                rect = round_rect(
                    self.canvas, x1, y1, x2, y2, RADIUS, fill=color, outline=""
                )

                text = self.canvas.create_text(
                    (x1 + x2) / 2,
                    (y1 + y2) / 2,
                    text=str(day),
                    fill=BG if is_today else TEXT,
                    font=("JetBrains Mono", 11),
                )

                def on_enter(e, r=rect, t=is_today):
                    if not t:
                        self.canvas.itemconfig(r, fill=HOVER)

                def on_leave(e, r=rect, t=is_today):
                    if not t:
                        self.canvas.itemconfig(r, fill=SURFACE)

                self.canvas.tag_bind(rect, "<Enter>", on_enter)
                self.canvas.tag_bind(rect, "<Leave>", on_leave)
                self.canvas.tag_bind(text, "<Enter>", on_enter)
                self.canvas.tag_bind(text, "<Leave>", on_leave)

    def prev_month(self):
        self.month -= 1
        if self.month == 0:
            self.month = 12
            self.year -= 1
        self.draw()

    def next_month(self):
        self.month += 1
        if self.month == 13:
            self.month = 1
            self.year += 1
        self.draw()


if __name__ == "__main__":
    root = tk.Tk()
    CalendarApp(root)
    root.mainloop()
