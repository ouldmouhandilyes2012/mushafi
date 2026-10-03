from __future__ import annotations

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from screens.base import BaseScreen


class StatisticsScreen(BaseScreen):
    def __init__(self, name: str, app=None, **kwargs):
        super().__init__(name=name, app=app, **kwargs)
        self.title_label.text = "الإحصائيات"
        self.app = app

        self.container = BoxLayout(orientation="vertical", spacing=12, padding=12)

        stats = self.app.db.get_statistics_summary() if self.app and hasattr(self.app, "db") else {"memorized": 0, "review": 0, "unmemorized": 114}
        profile = self.app.db.get_profile() if self.app and hasattr(self.app, "db") else {}

        progress_percent = int((stats.get("memorized", 0) / 114) * 100) if stats.get("memorized", 0) > 0 else 0

        self.container.add_widget(Label(text="بيانات الحفظ", halign="right", font_size=22, size_hint_y=None, height=40))
        self.container.add_widget(Label(
            text=f"عدد السور المحفوظة: {stats.get('memorized', 0)}/114",
            halign="right",
            font_size=20,
            size_hint_y=None,
            height=35,
        ))
        self.container.add_widget(Label(
            text=f"التقدم: {progress_percent}%",
            halign="right",
            font_size=20,
            size_hint_y=None,
            height=35,
        ))
        self.container.add_widget(Label(
            text=f"عدد السور الباقية: {stats.get('unmemorized', 114)}",
            halign="right",
            font_size=20,
            size_hint_y=None,
            height=35,
        ))

        self.container.add_widget(Label(text="بيانات المراجعة", halign="right", font_size=22, size_hint_y=None, height=40))
        self.container.add_widget(Label(
            text=f"عدد السور بحاجة مراجعة: {stats.get('review', 0)}",
            halign="right",
            font_size=20,
            size_hint_y=None,
            height=35,
        ))

        self.container.add_widget(Label(text="بيانات المستخدم", halign="right", font_size=22, size_hint_y=None, height=40))
        self.container.add_widget(Label(
            text=f"هدف الحفظ: {profile.get('memorization_goal', 30)} سورة",
            halign="right",
            font_size=18,
            size_hint_y=None,
            height=35,
        ))
        self.container.add_widget(Label(
            text=f"هدف المراجعة: {profile.get('review_goal', 10)} جلسات",
            halign="right",
            font_size=18,
            size_hint_y=None,
            height=35,
        ))

        scroll = ScrollView(do_scroll_x=False)
        scroll.add_widget(self.container)
        self.add_widget(scroll)
