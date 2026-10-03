from __future__ import annotations

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from screens.base import BaseScreen
from widgets.heart_grid import HeartGridWidget


class HeartScreen(BaseScreen):
    def __init__(self, name: str, app=None, **kwargs):
        super().__init__(name=name, app=app, **kwargs)
        self.title_label.text = "قلب القرآن"

        self.layout = BoxLayout(orientation="vertical", spacing=12, padding=12)

        self.legend = BoxLayout(size_hint_y=None, height=60, spacing=8)
        self.legend.add_widget(Button(text="محفوظ", background_color=(0.35, 0.75, 0.38, 1), color=(1, 1, 1, 1)))
        self.legend.add_widget(Button(text="يحتاج مراجعة", background_color=(0.95, 0.7, 0.25, 1), color=(0.2, 0.2, 0.2, 1)))
        self.legend.add_widget(Button(text="غير محفوظ", background_color=(0.85, 0.35, 0.35, 1), color=(1, 1, 1, 1)))
        self.layout.add_widget(self.legend)

        self.grid = HeartGridWidget(statuses=self._load_statuses())
        self._bind_grid_events()
        self.layout.add_widget(self.grid)
        self.add_widget(self.layout)

    def _load_statuses(self):
        if not self.app or not hasattr(self.app, "db"):
            return {}
        return self.app.db.get_surah_statuses()

    def _bind_grid_events(self):
        for cell in getattr(self.grid, "cells", []):
            cell.bind(on_release=self._toggle_status)

    def _toggle_status(self, instance):
        if not self.app or not hasattr(self.app, "db"):
            return

        current = instance.status
        if current == "unmemorized":
            new_status = "memorized"
        elif current == "memorized":
            new_status = "review"
        else:
            new_status = "unmemorized"

        instance.status = new_status
        instance.background_color = self._status_color(new_status)
        self.app.db.update_surah_status(instance.surah_number, new_status)

    def _status_color(self, status: str):
        if status == "memorized":
            return (0.35, 0.75, 0.38, 1)
        if status == "review":
            return (0.95, 0.7, 0.25, 1)
        return (0.85, 0.35, 0.35, 1)
