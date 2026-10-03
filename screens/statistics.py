from __future__ import annotations

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from screens.base import BaseScreen


class ProfileScreen(BaseScreen):
    def __init__(self, name: str, app=None, **kwargs):
        super().__init__(name=name, app=app, **kwargs)
        self.title_label.text = "الملف الشخصي"

        self.container = BoxLayout(orientation="vertical", spacing=12, padding=12)

        profile = self.app.db.get_profile() if self.app and hasattr(self.app, "db") else {}
        self.container.add_widget(Label(text=f"الاسم: {profile.get('display_name', 'المستخدم')}", halign="right", font_size=20))
        self.container.add_widget(Label(text=f"الرواية المفضلة: {profile.get('favorite_riwayah', 'hafs')}", halign="right", font_size=20))
        self.container.add_widget(Label(text=f"القارئ المفضل: {profile.get('favorite_reader', 'غير محدد')}", halign="right", font_size=20))
        self.container.add_widget(Label(text=f"هدف الحفظ: {profile.get('memorization_goal', 30)} سورة", halign="right", font_size=20))
        self.container.add_widget(Label(text=f"هدف المراجعة: {profile.get('review_goal', 10)} جلسات", halign="right", font_size=20))
        self.add_widget(self.container)
