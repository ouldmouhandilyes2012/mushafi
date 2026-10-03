from __future__ import annotations

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.switch import Switch

from screens.base import BaseScreen


class SettingsScreen(BaseScreen):
    def __init__(self, name: str, app=None, **kwargs):
        super().__init__(name=name, app=app, **kwargs)
        self.title_label.text = "الإعدادات"

        self.container = BoxLayout(orientation="vertical", spacing=12, padding=12)

        profile = self.app.db.get_profile() if self.app and hasattr(self.app, "db") else {}
        selected_riwayah = self.app.db.get_setting("selected_riwayah", "hafs") if self.app and hasattr(self.app, "db") else "hafs"
        night_mode = self.app.db.get_setting("night_mode", "0") if self.app and hasattr(self.app, "db") else "0"
        notifications = self.app.db.get_setting("local_notifications", "1") if self.app and hasattr(self.app, "db") else "1"

        self.container.add_widget(Label(text=f"اختيار الرواية: {selected_riwayah}", halign="right", font_size=18))
        self.container.add_widget(Label(text=f"القارئ المفضل: {profile.get('favorite_reader', 'غير محدد')}", halign="right", font_size=18))
        self.container.add_widget(Label(text=f"حجم الخط: {self.app.db.get_setting('font_size', '22') if self.app and hasattr(self.app, 'db') else '22'}", halign="right", font_size=18))
        self.container.add_widget(Label(text="الوضع الليلي", halign="right", font_size=18))
        self.container.add_widget(Switch(active=(night_mode == "1")))
        self.container.add_widget(Label(text=f"التنبيهات المحلية: {'مفعل' if notifications == '1' else 'متوقف'}", halign="right", font_size=18))
        self.container.add_widget(Label(text="إدارة المحتوى المحمل", halign="right", font_size=18))
        self.container.add_widget(Label(text="حذف التسجيلات الشخصية", halign="right", font_size=18))
        self.container.add_widget(Label(text="حذف بيانات التطبيق", halign="right", font_size=18))
        self.add_widget(self.container)
