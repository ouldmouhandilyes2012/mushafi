from __future__ import annotations

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout


class HeartCell(Button):
    def __init__(self, surah_number: int, status: str = "unmemorized", **kwargs):
        super().__init__(**kwargs)
        self.surah_number = surah_number
        self.status = status
        self.text = str(surah_number)
        self.font_size = 18
        self.background_color = self._status_color(status)
        self.color = (0.2, 0.2, 0.2, 1)

    def _status_color(self, status: str):
        if status == "memorized":
            return (0.35, 0.75, 0.38, 1)
        if status == "review":
            return (0.95, 0.7, 0.25, 1)
        return (0.85, 0.35, 0.35, 1)


class HeartGridWidget(GridLayout):
    def __init__(self, statuses=None, **kwargs):
        super().__init__(**kwargs)
        self.cols = 6
        self.spacing = 8
        self.padding = 10
        self.size_hint_y = None
        self.bind(minimum_height=self.setter("height"))
        statuses = statuses or {}
        self.cells = []
        for surah in range(1, 115):
            status = statuses.get(surah, "unmemorized")
            cell = HeartCell(surah, status)
            self.cells.append(cell)
            self.add_widget(cell)
