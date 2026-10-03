from __future__ import annotations

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class VerseWidget(BoxLayout):
    def __init__(self, surah_number: int, ayah_number: int, text: str = "", **kwargs):
        super().__init__(orientation="vertical", spacing=6, padding=(12, 8), **kwargs)
        self.size_hint_y = None
        self.height = 120
        self.add_widget(Label(text=f"{surah_number}:{ayah_number}", halign="right", valign="middle", color=(0.25, 0.25, 0.25, 1), font_size=18, text_size=(self.width, None)))
        self.add_widget(Label(text=text or "", halign="right", valign="middle", font_size=22, text_size=(self.width, None), multiline=True))
