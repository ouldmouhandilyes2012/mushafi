from __future__ import annotations

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from screens.base import BaseScreen
from services.review_engine import ReviewEngine


class ReviewScreen(BaseScreen):
    def __init__(self, name: str, app=None, **kwargs):
        super().__init__(name=name, app=app, **kwargs)
        self.title_label.text = "المراجعة"
        self.app = app
        self.review_engine = ReviewEngine()

        self.container = BoxLayout(orientation="vertical", spacing=12, padding=12)

        self.dashboard = self.app.db.get_profile() if self.app and hasattr(self.app, "db") else {}
        self.stats = self._get_review_stats()

        self.stats_row = BoxLayout(size_hint_y=None, height=90, spacing=10)
        self.stats_row.add_widget(Button(text=f"اليوم\n{self.stats.get('today', 0)}", background_color=(0.35, 0.75, 0.38, 1), color=(1, 1, 1, 1)))
        self.stats_row.add_widget(Button(text=f"قادمة\n{self.stats.get('upcoming', 0)}", background_color=(0.95, 0.7, 0.25, 1), color=(0.2, 0.2, 0.2, 1)))
        self.stats_row.add_widget(Button(text=f"متأخرة\n{self.stats.get('overdue', 0)}", background_color=(0.85, 0.35, 0.35, 1), color=(1, 1, 1, 1)))
        self.container.add_widget(self.stats_row)

        self.title_today = Label(text="مراجعات اليوم", halign="right", font_size=20, size_hint_y=None, height=40)
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
            self.reviews_box.add_widget(Label(text="لا توجد مراجعات", halign="right", font_size=18))
            return

        reviews = self.review_engine.list_due_reviews(self.app.db.connection)
        if not reviews:
            self.reviews_box.add_widget(Label(text="No reviews due today", halign="right", font_size=18))
            return

        for review in reviews[:5]:
            item = BoxLayout(orientation="horizontal", spacing=10, size_hint_y=None, height=70)
            label_text = f"السورة {review['surah']}: الآية {review['ayah_start']}-{review['ayah_end']}\nالموعد: {review['due_date']}"
            item.add_widget(Label(text=label_text, halign="right", font_size=16))
            complete_btn = Button(text="تمت", size_hint_x=0.25)
            complete_btn.bind(on_release=lambda btn, r_id=review["id"]: self._mark_complete(r_id))
            item.add_widget(complete_btn)
            self.reviews_box.add_widget(item)

    def _mark_complete(self, review_id: int):
        if self.app and hasattr(self.app, "db"):
            self.review_engine.mark_review_done(self.app.db.connection, review_id)
            self.reviews_box.clear_widgets()
            self.stats = self._get_review_stats()
            self._refresh_reviews()
