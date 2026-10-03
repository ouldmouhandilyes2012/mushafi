from __future__ import annotations

from pathlib import Path

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from screens.base import BaseScreen
from services.quran_service import QuranDataImporter


class QuranScreen(BaseScreen):
    def __init__(self, name: str, app=None, **kwargs):
        super().__init__(name=name, app=app, **kwargs)
        self.title_label.text = "القرآن"

        root = Path(__file__).resolve().parent.parent
        self.importer = QuranDataImporter(root)

        self.container = BoxLayout(orientation="vertical", spacing=10, padding=12)

        self.action_row = BoxLayout(size_hint_y=None, height=60, spacing=8)
        self.action_row.add_widget(Button(text="السورة: 1", size_hint_x=0.5))
        self.action_row.add_widget(Button(text="الرواية: hafs", size_hint_x=0.4))
        self.action_row.add_widget(Button(text="A- A+", size_hint_x=0.2))
        self.container.add_widget(self.action_row)

        self.status_label = Label(
            text="نظام الاستيراد المحلي جاهز. ضع ملفات JSON لكل رواية داخل مجلدات assets/quran/...",
            halign="right",
            valign="top",
            font_size=18,
            text_size=(self.width, None),
            markup=True,
        )
        self.container.add_widget(self.status_label)

        files = self.importer.list_available_files()
        if files:
            self.status_label.text = f"تم العثور على {len(files)} ملفًا محليًا جاهزًا للاستيراد."

        scroll = ScrollView(do_scroll_x=False)
        scroll.add_widget(self.container)
        self.add_widget(scroll)
