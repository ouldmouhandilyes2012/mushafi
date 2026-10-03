from __future__ import annotations

from pathlib import Path

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner

from screens.base import BaseScreen
from services.tafsir_service import TafsirService


class TafsirScreen(BaseScreen):
    def __init__(self, name: str, app=None, **kwargs):
        super().__init__(name=name, app=app, **kwargs)
        self.title_label.text = "التفسير"
        self.app = app

        root = Path(__file__).resolve().parent.parent
        self.tafsir_service = TafsirService(root)

        self.container = BoxLayout(orientation="vertical", spacing=10, padding=12)

        self.input_row = BoxLayout(size_hint_y=None, height=60, spacing=8)
        self.surah_input = Spinner(
            text="السورة: 1",
            values=tuple(f"{i}" for i in range(1, 115)),
            size_hint_x=0.5,
        )
        self.ayah_input = Spinner(
            text="الآية: 1",
            values=tuple(f"{i}" for i in range(1, 300)),
            size_hint_x=0.3,
        )
        self.search_btn = Button(text="بحث", size_hint_x=0.2)
        self.search_btn.bind(on_release=self._search_tafsir)
        self.input_row.add_widget(self.surah_input)
        self.input_row.add_widget(self.ayah_input)
        self.input_row.add_widget(self.search_btn)
        self.container.add_widget(self.input_row)

        self.tafsir_scroll = ScrollView(do_scroll_x=False)
        self.tafsir_label = Label(
            text="اختر سورة وآية مبحثا. البيانات التفسيرية يتم قراءتها من assets/tafsir/ محليًا.",
            halign="right",
            valign="top",
            text_size=(self.width, None),
            font_size=18,
        )
        self.tafsir_scroll.add_widget(self.tafsir_label)
        self.container.add_widget(self.tafsir_scroll)

        self.add_widget(self.container)

    def _search_tafsir(self, instance):
        try:
            surah = int(self.surah_input.text)
            ayah = int(self.ayah_input.text)
        except ValueError:
            self.tafsir_label.text = "بيانات غير صحيحة. ادخل رقم السورة والآية."
            return

        result = self.tafsir_service.find_tafsir_for_ayah(surah, ayah)
        if result:
            self.tafsir_label.text = f"التفسير:\n{result.get('text', '')}\n\nالمصدر: {result.get('source', '')}"
        else:
            self.tafsir_label.text = f"لم يتم العثور على تفسير للسورة {surah} الآية {ayah}. أضف بيانات التفسير ل assets/tafsir/tafsir.json"
