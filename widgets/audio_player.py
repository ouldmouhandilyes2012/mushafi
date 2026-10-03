from __future__ import annotations

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class AudioPlayer(BoxLayout):
    def __init__(self, file_path: str = "", **kwargs):
        super().__init__(orientation="horizontal", spacing=8, **kwargs)
        self.file_path = file_path
        self.play_button = Button(text="تشغيل")
        self.play_button.bind(on_release=self._play_audio)
        self.label = Label(text=file_path or "لا توجد ملفات صوتية محلية.", halign="right", font_size=16, text_size=(self.width, None))
        self.add_widget(self.label)
        self.add_widget(self.play_button)

    def _play_audio(self, instance):
        if not self.file_path:
            return
        from services.audio_service import AudioService
        AudioService().play_local_audio(self.file_path)
