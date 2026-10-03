from __future__ import annotations

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from screens.base import BaseScreen


class ReviewScreen(BaseScreen):
    def __init__(self, name: str, app=None, **kwargs):
        super().__init__(name=name, app=app, **kwargs)
        self.title_label.text = "المراجعة"

        self.container = BoxLayout(orientation="vertical", spacing=12, padding=12)
        self.container.add_widget(Label(text="مراجعات اليوم", halign="right", font_size=24))
        self.container.add_widget(Label(text="مراجعات قادمة", halign="right", font_size=18))
        self.container.add_widget(Label(text="متأخرات", halign="right", font_size=18))
        self.add_widget(self.container)
