from __future__ import annotations

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from screens.base import BaseScreen


class TafsirScreen(BaseScreen):
    def __init__(self, name: str, app=None, **kwargs):
        super().__init__(name=name, app=app, **kwargs)
        self.title_label.text = "التفسير"

        self.container = BoxLayout(orientation="vertical", spacing=12, padding=12)
        self.container.add_widget(Label(text="حدد آية ثم افتح زر التفسير. البيانات تُقرأ محليًا من مجلد assets/tafsir/.", halign="right", font_size=18, text_size=(self.width, None)))
        self.add_widget(self.container)
