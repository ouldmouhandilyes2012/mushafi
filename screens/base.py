from __future__ import annotations

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView


class BaseScreen(BoxLayout):
    def __init__(self, name: str, app=None, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.name = name
        self.app = app
        self.top_bar = BoxLayout(size_hint_y=None, height=70, spacing=10, padding=(12, 10))
        self.top_bar.canvas.before.clear()

        self.title_label = Label(
            text="مصحفي",
            font_size=28,
            halign="right",
            valign="middle",
            color=(0.45, 0.25, 0.05, 1),
            text_size=(self.width, None),
            bold=True,
        )
        self.back_button = Button(text="رجوع", size_hint_x=0.2, background_color=(0.85, 0.35, 0.35, 1), color=(1, 1, 1, 1))
        self.back_button.bind(on_release=self._go_back)
        self.top_bar.add_widget(self.title_label)
        self.top_bar.add_widget(self.back_button)
        self.add_widget(self.top_bar)

    def _go_back(self, instance):
        if self.app and hasattr(self.app, "screen_manager"):
            self.app.screen_manager.current = "home"
