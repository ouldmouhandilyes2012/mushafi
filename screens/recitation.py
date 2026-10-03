from __future__ import annotations

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from screens.base import BaseScreen
from widgets.audio_player import AudioPlayer


class RecitationScreen(BaseScreen):
    def __init__(self, name: str, app=None, **kwargs):
        super().__init__(name=name, app=app, **kwargs)
        self.title_label.text = "التسميع"

        self.container = BoxLayout(orientation="vertical", spacing=10, padding=12)
        self.container.add_widget(Label(text="اختر السورة، اختر الآيات، واحفظ التسجيل محليًا على الجهاز.", halign="right", font_size=18, text_size=(self.width, None)))
        self.container.add_widget(Label(text="التسجيل يظل محليًا فقط، ولا يتم رفعه إلى خادم خارجي.", halign="right", font_size=16, text_size=(self.width, None)))
        self.container.add_widget(AudioPlayer(file_path=""))
        self.add_widget(self.container)
