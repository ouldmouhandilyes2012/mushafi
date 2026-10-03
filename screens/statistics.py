from __future__ import annotations

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from screens.base import BaseScreen


class StatisticsScreen(BaseScreen):
    def __init__(self, name: str, app=None, **kwargs):
        super().__init__(name=name, app=app, **kwargs)
        self.title_label.text = "الإحصائيات"

        self.container = BoxLayout(orientation="vertical", spacing=10, padding=12)
        self.container.add_widget(Label(text="عدد السور المحفوظة: 0", halign="right", font_size=20))
        self.container.add_widget(Label(text="عدد السور المتقنة: 0", halign="right", font_size=20))
        self.container.add_widget(Label(text="عدد السور التي تحتاج مراجعة: 0", halign="right", font_size=20))
        self.container.add_widget(Label(text="عدد الآيات المحفوظة: 0", halign="right", font_size=20))
        self.container.add_widget(Label(text="عدد جلسات التسميع: 0", halign="right", font_size=20))
        self.container.add_widget(Label(text="عدد الأخطاء: 0", halign="right", font_size=20))
        self.container.add_widget(Label(text="أيام المراجعة: 0", halign="right", font_size=20))
        self.add_widget(self.container)
