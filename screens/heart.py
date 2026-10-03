from __future__ import annotations

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

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
        self.layout.add_widget(HeartGridWidget())
        self.add_widget(self.layout)
