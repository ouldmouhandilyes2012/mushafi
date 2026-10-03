from __future__ import annotations

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from screens.base import BaseScreen


class HomeScreen(BaseScreen):
    def __init__(self, name: str, app=None, **kwargs):
        super().__init__(name=name, app=app, **kwargs)
        self.title_label.text = "مصحفي"

        self.grid = GridLayout(cols=2, spacing=12, padding=12, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter("height"))

        cards = [
            ("القرآن", "quran", (0.96, 0.89, 0.76, 1)),
            ("قلب القرآن ❤️", "heart", (1, 0.85, 0.85, 1)),
            ("التفسير", "tafsir", (0.85, 0.95, 1, 1)),
            ("المراجعة", "review", (1, 0.95, 0.85, 1)),
            ("التسميع", "recitation", (0.95, 0.9, 0.8, 1)),
            ("العلامات", "bookmarks_notes", (0.9, 0.95, 0.85, 1)),
            ("الإحصائيات", "statistics", (0.8, 0.9, 1, 1)),
            ("الملف الشخصي", "profile", (0.9, 0.85, 0.95, 1)),
            ("الإعدادات", "settings", (0.85, 0.9, 0.95, 1)),
        ]

        for label, target, color in cards:
            btn = Button(
                text=label,
                size_hint_y=None,
                height=92,
                background_color=color,
                color=(0.18, 0.18, 0.18, 1),
                font_size=18,
            )
            btn.bind(on_release=lambda instance, screen_name=target: self._open(screen_name))
            self.grid.add_widget(btn)

        scroll = ScrollView(do_scroll_x=False)
        scroll.add_widget(self.grid)
        self.add_widget(scroll)

    def _open(self, screen_name: str):
        if self.app and hasattr(self.app, "screen_manager"):
            self.app.screen_manager.current = screen_name
