from __future__ import annotations

from pathlib import Path

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner

from screens.base import BaseScreen


class QuranBookmarksNotesScreen(BaseScreen):
    def __init__(self, name: str, app=None, **kwargs):
        super().__init__(name=name, app=app, **kwargs)
        self.title_label.text = "العلامات والملاحظات"
        self.app = app

        self.container = BoxLayout(orientation="vertical", spacing=10, padding=12)

        self.tabs = BoxLayout(size_hint_y=None, height=60, spacing=8)
        self.bookmarks_tab = Button(text="العلامات", background_color=(0.35, 0.75, 0.38, 1), color=(1, 1, 1, 1))
        self.notes_tab = Button(text="الملاحظات", background_color=(0.95, 0.7, 0.25, 1), color=(0.2, 0.2, 0.2, 1))
        self.bookmarks_tab.bind(on_release=lambda x: self._show_bookmarks())
        self.notes_tab.bind(on_release=lambda x: self._show_notes())
        self.tabs.add_widget(self.bookmarks_tab)
        self.tabs.add_widget(self.notes_tab)
        self.container.add_widget(self.tabs)

        self.items_scroll = ScrollView(do_scroll_x=False)
        self.items_box = BoxLayout(orientation="vertical", spacing=8, size_hint_y=None, padding=(0, 4))
        self.items_box.bind(minimum_height=self.items_box.setter("height"))
        self.items_scroll.add_widget(self.items_box)
        self.container.add_widget(self.items_scroll)

        self.add_widget(self.container)
        self._show_bookmarks()

    def _show_bookmarks(self):
        self.bookmarks_tab.background_color = (0.35, 0.75, 0.38, 1)
        self.notes_tab.background_color = (0.95, 0.7, 0.25, 1)
        self.items_box.clear_widgets()

        if not self.app or not hasattr(self.app, "db"):
            self.items_box.add_widget(Label(text="u0644ا توجد بيانات", halign="right", font_size=16, size_hint_y=None, height=40))
            return

        bookmarks = self.app.db.fetch_all("SELECT * FROM bookmarks ORDER BY created_at DESC")
        if not bookmarks:
            self.items_box.add_widget(Label(text="u0644ا توجد علامات", halign="right", font_size=16, size_hint_y=None, height=40))
            return

        for bm in bookmarks:
            item = BoxLayout(orientation="horizontal", spacing=8, size_hint_y=None, height=50)
            label_text = fالسورة {bm['surah_number']}:{bm['ayah_number']} - {bm['label']}"
            item.add_widget(Label(text=label_text, halign="right", font_size=16))
            delete_btn = Button(text="u062dذf", size_hint_x=0.15)
            delete_btn.bind(on_release=lambda btn, bid=bm["id"]: self._delete_bookmark(bid))
            item.add_widget(delete_btn)
            self.items_box.add_widget(item)

    def _show_notes(self):
        self.bookmarks_tab.background_color = (0.95, 0.7, 0.25, 1)
        self.notes_tab.background_color = (0.35, 0.75, 0.38, 1)
        self.items_box.clear_widgets()

        if not self.app or not hasattr(self.app, "db"):
            self.items_box.add_widget(Label(text="u0644ا توجد بيانات", halign="right", font_size=16, size_hint_y=None, height=40))
            return

        notes = self.app.db.fetch_all("SELECT * FROM notes ORDER BY created_at DESC")
        if not notes:
            self.items_box.add_widget(Label(text="u0644ا توجد ملاحظات", halign="right", font_size=16, size_hint_y=None, height=40))
            return

        for note in notes:
            item = BoxLayout(orientation="vertical", spacing=4, size_hint_y=None, height=80)
            title = fالسورة {note['surah_number']}:{note['ayah_number']}"
            item.add_widget(Label(text=title, halign="right", font_size=14, size_hint_y=0.3))
            item.add_widget(Label(text=note['note'], halign="right", font_size=14, text_size=(self.width, None), size_hint_y=0.7))
            self.items_box.add_widget(item)

    def _delete_bookmark(self, bookmark_id: int):
        if self.app and hasattr(self.app, "db"):
            self.app.db.execute("DELETE FROM bookmarks WHERE id = ?", (bookmark_id,))
            self._show_bookmarks()
