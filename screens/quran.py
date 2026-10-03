from __future__ import annotations

import json
from pathlib import Path

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner

from screens.base import BaseScreen
from services.quran_service import QuranDataImporter


class QuranScreen(BaseScreen):
    def __init__(self, name: str, app=None, **kwargs):
        super().__init__(name=name, app=app, **kwargs)
        self.title_label.text = "القرآان"

        self.root = Path(__file__).resolve().parent.parent
        self.importer = QuranDataImporter(self.root)
        self.current_surah = 1
        self.current_riwayah = "hafs"
        self.ayahs = []
        self.font_size = 22

        self.container = BoxLayout(orientation="vertical", spacing=10, padding=12)

        self.action_row = BoxLayout(size_hint_y=None, height=70, spacing=8)
        self.prev_button = Button(text="◀ السابقة", size_hint_x=0.25, background_color=(0.8, 0.8, 0.8, 1), color=(0.2, 0.2, 0.2, 1))
        self.next_button = Button(text="u0627لتالية ▶", size_hint_x=0.25, background_color=(0.8, 0.8, 0.8, 1), color=(0.2, 0.2, 0.2, 1))
        self.riwayah_button = Button(text="رواية: hafs", size_hint_x=0.3, background_color=(0.9, 0.85, 0.7, 1), color=(0.2, 0.2, 0.2, 1))
        self.font_button = Button(text="A±", size_hint_x=0.2, background_color=(0.7, 0.8, 0.9, 1), color=(0.2, 0.2, 0.2, 1))

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
            text="نظام القرآان المحلي جاهز. ضع ملفات JSON موثقة داخل assets/quran/...",
            halign="right",
            valign="top",
            font_size=14,
            text_size=(self.width, None),
            markup=True,
            size_hint_y=None,
            height=50,
        )
        self.container.add_widget(self.status_label)

        self.display_box = BoxLayout(orientation="vertical", spacing=8, padding=(0, 4))
        self.verse_scroll = ScrollView(do_scroll_x=False)
        self.verse_scroll.add_widget(self.display_box)
        self.container.add_widget(self.verse_scroll)

        self.add_widget(self.container)
        self._refresh_ui()

    def _toggle_font_size(self, instance):
        self.font_size = 18 if self.font_size >= 24 else self.font_size + 2
        self.font_button.text = f"A± [{self.font_size}]"
        self._refresh_ui()

    def _toggle_riwayah(self, instance):
        riwayah_list = ["hafs", "warsh", "qalun"]
        index = riwayah_list.index(self.current_riwayah)
        self.current_riwayah = riwayah_list[(index + 1) % len(riwayah_list)]
        self.riwayah_button.text = f"رواية: {self.current_riwayah}"
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
            self.status_label.text = f"ملفات متاحة: {len(files)}"
        else:
            self.status_label.text = "لا توجد بيانات قرآنية محلية"

        self.ayahs = self._load_ayahs_for_current_surah()
        self.display_box.clear_widgets()

        if not self.ayahs:
            notice = Label(
                text=f"لا توجد آيات للسورة {self.current_surah} برواية {self.current_riwayah}",
                halign="right",
                valign="top",
                text_size=(self.width, None),
                font_size=16,
                size_hint_y=None,
                height=60,
            )
            self.display_box.add_widget(notice)
            return

        title = Label(
            text=f"السورة {self.current_surah}",
            halign="right",
            font_size=24,
            size_hint_y=None,
            height=50,
            bold=True,
        )
        self.display_box.add_widget(title)

        for ayah in self.ayahs:
            item = BoxLayout(
                orientation="vertical",
                spacing=4,
                size_hint_y=None,
                height=self.font_size * 3,
                padding=(8, 4),
            )
            ayah_num = Label(
                text=f"الآية {ayah.get('ayah_number', '')}",
                halign="right",
                font_size=12,
                color=(0.5, 0.5, 0.5, 1),
                size_hint_y=0.2,
            )
            text_label = Label(
                text=ayah.get("text", ""),
                halign="right",
                valign="top",
                text_size=(self.width - 16, None),
                font_size=self.font_size,
                size_hint_y=0.8,
            )
            item.add_widget(ayah_num)
            item.add_widget(text_label)
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
