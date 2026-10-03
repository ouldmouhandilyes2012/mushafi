from __future__ import annotations

from datetime import datetime
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

from screens.base import BaseScreen
from services.review_engine import ReviewEngine


class ReviewScreen(BaseScreen):
    def __init__(self, name: str, app=None, **kwargs):
        super().__init__(name=name, app=app, **kwargs)
        self.title_label.text = "المراجعة"
        self.app = app
        self.review_engine = ReviewEngine()

        self.container = BoxLayout(orientation="vertical", spacing=12, padding=12)

        self.stats = self._get_review_stats()

        self.stats_row = GridLayout(cols=3, spacing=10, size_hint_y=None, height=100)
        self.stats_row.add_widget(Button(
            text=f"اليوم\n[{self.stats.get('today', 0)}]",
            background_color=(0.35, 0.75, 0.38, 1),
            color=(1, 1, 1, 1),
            font_size=16,
        ))
        self.stats_row.add_widget(Button(
            text=f"قادمة\n[{self.stats.get('upcoming', 0)}]",
            background_color=(0.95, 0.7, 0.25, 1),
            color=(0.2, 0.2, 0.2, 1),
            font_size=16,
        ))
        self.stats_row.add_widget(Button(
            text=f"متأخرة\n[{self.stats.get('overdue', 0)}]",
            background_color=(0.85, 0.35, 0.35, 1),
            color=(1, 1, 1, 1),
            font_size=16,
        ))
        self.container.add_widget(self.stats_row)

        self.title_today = Label(
            text=f"مراجعات اليوم ({self.stats.get('today', 0)})",
            halign="right",
            font_size=20,
            bold=True,
            size_hint_y=None,
            height=40,
        )
        self.container.add_widget(self.title_today)

        self.reviews_scroll = ScrollView(do_scroll_x=False)
        self.reviews_box = BoxLayout(orientation="vertical", spacing=8, size_hint_y=None, padding=(0, 4))
        self.reviews_box.bind(minimum_height=self.reviews_box.setter("height"))
        self.reviews_scroll.add_widget(self.reviews_box)
        self.container.add_widget(self.reviews_scroll)

        self.add_widget(self.container)
        self._refresh_reviews()

    def _get_review_stats(self):
        if not self.app or not hasattr(self.app, "db"):
            return {"today": 0, "upcoming": 0, "overdue": 0}
        return self.review_engine.get_dashboard(self.app.db.connection)

    def _refresh_reviews(self):
        if not self.app or not hasattr(self.app, "db"):
            self.reviews_box.add_widget(Label(text="لا توجد بيانات", halign="right", font_size=18, size_hint_y=None, height=40))
            return

        reviews = self.review_engine.list_due_reviews(self.app.db.connection)
        if not reviews:
            self.reviews_box.add_widget(Label(
                text="u0644ا توجد مراجعات محدثة",
                halign="right",
                font_size=18,
                size_hint_y=None,
                height=40,
            ))
            return

        for review in reviews[:10]:
            item = BoxLayout(orientation="horizontal", spacing=10, size_hint_y=None, height=80, padding=(8, 4))
            label_box = BoxLayout(orientation="vertical", spacing=4)
            label_text = fالسورة {review['surah']}: {review['ayah_start']}-{review['ayah_end']}"
            label_box.add_widget(Label(text=label_text, halign="right", font_size=16, size_hint_y=0.5))
            label_box.add_widget(Label(
                text=fموعد: {review['due_date']}",
                halign="right",
                font_size=12,
                color=(0.5, 0.5, 0.5, 1),
                size_hint_y=0.5,
            ))
            item.add_widget(label_box)
            complete_btn = Button(text="✓", size_hint_x=0.15, background_color=(0.35, 0.75, 0.38, 1), color=(1, 1, 1, 1))
            complete_btn.bind(on_release=lambda btn, r_id=review["id"]: self._mark_complete(r_id))
            item.add_widget(complete_btn)
            self.reviews_box.add_widget(item)

    def _mark_complete(self, review_id: int):
        if self.app and hasattr(self.app, "db"):
            self.review_engine.mark_review_done(self.app.db.connection, review_id)
            self.reviews_box.clear_widgets()
            self.stats = self._get_review_stats()
            self.title_today.text = fمراجعات اليوم ({self.stats.get('today', 0)})"
            self._refresh_reviews()
