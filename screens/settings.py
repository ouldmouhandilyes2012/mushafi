from __future__ import annotations

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.switch import Switch

from screens.base import BaseScreen


class SettingsScreen(BaseScreen):
    def __init__(self, name: str, app=None, **kwargs):
        super().__init__(name=name, app=app, **kwargs)
        self.title_label.text = "الإعدادات"

        self.container = BoxLayout(orientation="vertical", spacing=10, padding=12)
        self.container.add_widget(Label(text="اختيار الرواية: hafs", halign="right", font_size=18))
        self.container.add_widget(Label(text="اختيار القارئ: غير محدد", halign="right", font_size=18))
        self.container.add_widget(Label(text="حجم الخط: 22", halign="right", font_size=18))
        self.container.add_widget(Label(text="الوضع الليلي", halign="right", font_size=18))
        self.container.add_widget(Switch(active=False))
        self.container.add_widget(Label(text="التنبيهات المحلية: مفعل", halign="right", font_size=18))
        self.container.add_widget(Label(text="إدارة المحتوى المحمل", halign="right", font_size=18))
        self.container.add_widget(Label(text="حذف التسجيلات الشخصية", halign="right", font_size=18))
        self.container.add_widget(Label(text="حذف بيانات التطبيق", halign="right", font_size=18))
        self.add_widget(self.container)
