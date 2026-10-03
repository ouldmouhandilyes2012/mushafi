from __future__ import annotations

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from screens.base import BaseScreen


class ProfileScreen(BaseScreen):
    def __init__(self, name: str, app=None, **kwargs):
        super().__init__(name=name, app=app, **kwargs)
        self.title_label.text = "الملف الشخصي"

        self.container = BoxLayout(orientation="vertical", spacing=12, padding=12)
        self.container.add_widget(Label(text="الاسم: المستخدم", halign="right", font_size=20))
        self.container.add_widget(Label(text="الرواية المفضلة: hafs", halign="right", font_size=20))
        self.container.add_widget(Label(text="القارئ المفضل: غير محدد", halign="right", font_size=20))
        self.container.add_widget(Label(text="هدف الحفظ: 30 سورة", halign="right", font_size=20))
        self.container.add_widget(Label(text="هدف المراجعة: 10 جلسات", halign="right", font_size=20))
        self.add_widget(self.container)
