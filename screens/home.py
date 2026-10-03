from __future__ import annotations

from kivy.uix.button import Button
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
            ("القرآن", "quran"),
            ("الحفظ", "heart"),
            ("قلب القرآن ❤️", "heart"),
            ("المراجعة", "review"),
            ("التسميع", "recitation"),
            ("التفسير", "tafsir"),
            ("العلامات", "quran"),
            ("الملاحظات", "tafsir"),
            ("الإحصائيات", "statistics"),
            ("الملف الشخصي", "profile"),
            ("الإعدادات", "settings"),
        ]

        for label, target in cards:
            btn = Button(
                text=label,
                size_hint_y=None,
                height=92,
                background_color=(0.96, 0.89, 0.76, 1),
                color=(0.18, 0.18, 0.18, 1),
                font_size=20,
            )
            btn.bind(on_release=lambda instance, screen_name=target: self._open(screen_name))
            self.grid.add_widget(btn)

        scroll = ScrollView(do_scroll_x=False)
        scroll.add_widget(self.grid)
        self.add_widget(scroll)

    def _open(self, screen_name: str):
        if self.app and hasattr(self.app, "screen_manager"):
            self.app.screen_manager.current = screen_name
