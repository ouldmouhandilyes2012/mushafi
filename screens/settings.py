from __future__ import annotations

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.switch import Switch

from screens.base import BaseScreen


class SettingsScreen(BaseScreen):
    def __init__(self, name: str, app=None, **kwargs):
        super().__init__(name=name, app=app, **kwargs)
        self.title_label.text = "الإعدادات"
        self.app = app

        self.container = BoxLayout(orientation="vertical", spacing=12, padding=12)

        self.container.add_widget(Label(text="الرواية المفضلة", halign="right", font_size=18, size_hint_y=None, height=30))
        selected_riwayah = self.app.db.get_setting("selected_riwayah", "hafs") if self.app and hasattr(self.app, "db") else "hafs"
        self.riwayah_spinner = Spinner(
            text=selected_riwayah,
            values=("hafs", "warsh", "qalun"),
            size_hint_y=None,
            height=40,
        )
        self.container.add_widget(self.riwayah_spinner)

        self.container.add_widget(Label(text="حجم الخط", halign="right", font_size=18, size_hint_y=None, height=30))
        font_size = self.app.db.get_setting("font_size", "22") if self.app and hasattr(self.app, "db") else "22"
        self.font_spinner = Spinner(
            text=font_size,
            values=("18", "20", "22", "24", "26"),
            size_hint_y=None,
            height=40,
        )
        self.container.add_widget(self.font_spinner)

        self.container.add_widget(Label(text="الوضع الليلي", halign="right", font_size=18, size_hint_y=None, height=30))
        night_mode = self.app.db.get_setting("night_mode", "0") if self.app and hasattr(self.app, "db") else "0"
        self.night_mode_switch = Switch(active=(night_mode == "1"), size_hint_y=None, height=40)
        self.container.add_widget(self.night_mode_switch)

        self.container.add_widget(Label(text="التنبيهات المحلية", halign="right", font_size=18, size_hint_y=None, height=30))
        notifications = self.app.db.get_setting("local_notifications", "1") if self.app and hasattr(self.app, "db") else "1"
        self.notifications_switch = Switch(active=(notifications == "1"), size_hint_y=None, height=40)
        self.container.add_widget(self.notifications_switch)

        self.save_btn = Button(text="حفظ الإعدادات", size_hint_y=None, height=50)
        self.save_btn.bind(on_release=self._save_settings)
        self.container.add_widget(self.save_btn)

        scroll = ScrollView(do_scroll_x=False)
        scroll.add_widget(self.container)
        self.add_widget(scroll)

    def _save_settings(self, instance):
        if not self.app or not hasattr(self.app, "db"):
            return
        try:
            self.app.db.set_setting("selected_riwayah", self.riwayah_spinner.text)
            self.app.db.set_setting("font_size", self.font_spinner.text)
            self.app.db.set_setting("night_mode", "1" if self.night_mode_switch.active else "0")
            self.app.db.set_setting("local_notifications", "1" if self.notifications_switch.active else "0")
            self.title_label.text = "تم حفظ الإعدادات"
        except Exception as e:
            self.title_label.text = f"خطأ: {str(e)}"
