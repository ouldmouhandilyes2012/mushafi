from __future__ import annotations

import json
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

        self.root = Path(__file__).resolve().parent.parent
        self.importer = QuranDataImporter(self.root)
        self.current_surah = 1
        self.current_riwayah = "hafs"
        self.ayahs = []

        self.container = BoxLayout(orientation="vertical", spacing=10, padding=12)

        self.action_row = BoxLayout(size_hint_y=None, height=60, spacing=8)
        self.prev_button = Button(text="السورة السابقة", size_hint_x=0.3)
        self.next_button = Button(text="السورة التالية", size_hint_x=0.3)
        self.riwayah_button = Button(text="الرواية: hafs", size_hint_x=0.25)
        self.font_button = Button(text="A- A+", size_hint_x=0.15)

        self.prev_button.bind(on_release=self._prev_surah)
        self.next_button.bind(on_release=self._next_surah)
        self.riwayah_button.bind(on_release=self._toggle_riwayah)
        self.font_button.bind(on_release=self._toggle_font_size)

        self.action_row.add_widget(self.prev_button)
        self.action_row.add_widget(self.next_button)
        self.action_row.add_widget(self.riwayah_button)
        self.action_row.add_widget(self.font_button)
        self.container.add_widget(self.action_row)

        self.status_label = Label(
            text="نظام استيراد القرآن المحلي جاهز. ضع ملفات JSON موثقة داخل مجلدات assets/quran/...",
            halign="right",
            valign="top",
            font_size=18,
            text_size=(self.width, None),
            markup=True,
        )
        self.container.add_widget(self.status_label)

        self.display_box = BoxLayout(orientation="vertical", spacing=8, padding=(0, 4))
        self.verse_scroll = ScrollView(do_scroll_x=False)
        self.verse_scroll.add_widget(self.display_box)
        self.container.add_widget(self.verse_scroll)

        self.add_widget(self.container)
        self._refresh_ui()

    def _toggle_font_size(self, instance):
        font_size = 18 if self.status_label.font_size <= 18 else 22
        self.status_label.font_size = font_size
        for child in self.display_box.children:
            if hasattr(child, "font_size"):
                child.font_size = font_size + 4

    def _toggle_riwayah(self, instance):
        riwayah_list = ["hafs", "warsh", "qalun"]
        index = riwayah_list.index(self.current_riwayah)
        self.current_riwayah = riwayah_list[(index + 1) % len(riwayah_list)]
        self.riwayah_button.text = f"الرواية: {self.current_riwayah}"
        self._refresh_ui()

    def _prev_surah(self, instance):
        self.current_surah = max(1, self.current_surah - 1)
        self._refresh_ui()

    def _next_surah(self, instance):
        self.current_surah = min(114, self.current_surah + 1)
        self._refresh_ui()

    def _refresh_ui(self):
        files = self.importer.list_available_files()
        if files:
            self.status_label.text = f"تم العثور على {len(files)} ملفًا محليًا جاهزًا للاستيراد."
        else:
            self.status_label.text = "لا توجد ملفات قرآنية محلية في هذا المستودع. استخدم assets/quran/hafs/ أو warsh/ أو qalun/ مع ملفات JSON موثقة."

        self.ayahs = self._load_ayahs_for_current_surah()
        self.display_box.clear_widgets()

        if not self.ayahs:
            notice = Label(
                text="لا توجد آيات محلية للقراءة حاليًا. أضف ملف JSON صحيح لهذا السورة أو الرواية.",
                halign="right",
                valign="top",
                text_size=(self.width, None),
                font_size=18,
            )
            self.display_box.add_widget(notice)
            return

        title = Label(
            text=f"السورة {self.current_surah}",
            halign="right",
            font_size=22,
            size_hint_y=None,
            height=40,
        )
        self.display_box.add_widget(title)

        for ayah in self.ayahs:
            item = Label(
                text=f"{ayah.get('text', '')}",
                halign="right",
                valign="top",
                text_size=(self.width, None),
                font_size=22,
                size_hint_y=None,
                height=80,
                markup=True,
            )
            self.display_box.add_widget(item)

    def _load_ayahs_for_current_surah(self):
        files = self.importer.list_available_files()
        if not files:
            return []

        for path in files:
            file_path = Path(path)
            directory_name = file_path.parent.name.lower()
            if directory_name == self.current_riwayah:
                try:
                    with open(file_path, "r", encoding="utf-8") as handle:
                        rows = json.load(handle)
                    if not isinstance(rows, list):
                        continue
                    filtered = [
                        item for item in rows
                        if int(item.get("surah_number", 0)) == self.current_surah
                    ]
                    return sorted(filtered, key=lambda x: int(x.get("ayah_number", 0)))
                except (OSError, ValueError, TypeError, json.JSONDecodeError):
                    continue

        return []
