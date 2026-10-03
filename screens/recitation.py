from __future__ import annotations

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

from screens.base import BaseScreen


class RecitationScreen(BaseScreen):
    def __init__(self, name: str, app=None, **kwargs):
        super().__init__(name=name, app=app, **kwargs)
        self.title_label.text = "التسميع"
        self.app = app
        self.recording_in_progress = False

        self.container = BoxLayout(orientation="vertical", spacing=10, padding=12)

        self.info_box = BoxLayout(orientation="vertical", spacing=8, size_hint_y=None, height=100)
        self.info_box.add_widget(Label(text="اختر السورة ونطاق الآيات وسجل تلاوتك.", halign="right", font_size=18))
        self.info_box.add_widget(Label(text="التسجيلات تحفظ محليًا على الجهاز مباشرة بدون رفع.", halign="right", font_size=16))
        self.container.add_widget(self.info_box)

        self.input_row = BoxLayout(size_hint_y=None, height=60, spacing=8)
        self.surah_btn = Button(text="السورة: 1", size_hint_x=0.5)
        self.ayah_range_btn = Button(text="1-10", size_hint_x=0.5)
        self.input_row.add_widget(self.surah_btn)
        self.input_row.add_widget(self.ayah_range_btn)
        self.container.add_widget(self.input_row)

        self.controls = BoxLayout(size_hint_y=None, height=60, spacing=8)
        self.record_btn = Button(text="بدء التسجيل", background_color=(0.35, 0.75, 0.38, 1), color=(1, 1, 1, 1))
        self.stop_btn = Button(text="u0627لإيقاف", background_color=(0.85, 0.35, 0.35, 1), color=(1, 1, 1, 1))
        self.playback_btn = Button(text="تشغيل", background_color=(0.5, 0.5, 0.8, 1), color=(1, 1, 1, 1))
        self.record_btn.bind(on_release=self._start_recording)
        self.stop_btn.bind(on_release=self._stop_recording)
        self.playback_btn.bind(on_release=self._playback)
        self.controls.add_widget(self.record_btn)
        self.controls.add_widget(self.stop_btn)
        self.controls.add_widget(self.playback_btn)
        self.container.add_widget(self.controls)

        self.status_label = Label(
            text="التسجيلات المحفوظة",
            halign="right",
            font_size=18,
            size_hint_y=None,
            height=40,
        )
        self.container.add_widget(self.status_label)

        self.recordings_scroll = ScrollView(do_scroll_x=False)
        self.recordings_box = GridLayout(cols=1, spacing=8, size_hint_y=None, padding=(0, 4))
        self.recordings_box.bind(minimum_height=self.recordings_box.setter("height"))
        self.recordings_scroll.add_widget(self.recordings_box)
        self.container.add_widget(self.recordings_scroll)

        self.add_widget(self.container)
        self._refresh_recordings()

    def _start_recording(self, instance):
        self.recording_in_progress = True
        self.record_btn.disabled = True
        self.status_label.text = "جاري التسجيل..."

    def _stop_recording(self, instance):
        if self.recording_in_progress:
            self.recording_in_progress = False
            self.record_btn.disabled = False
            self.status_label.text = "تم الأيقاف بنجاح"
            self._save_recording()
            self._refresh_recordings()

    def _playback(self, instance):
        self.status_label.text = "لا توجد تسجيلات لتشغيلها"

    def _save_recording(self):
        if not self.app or not hasattr(self.app, "db"):
            return
        self.app.db.execute(
            "INSERT INTO recordings(name, file_path, duration_seconds, is_personal) VALUES (?, ?, ?, ?)",
            (f"السورة 1", "path/to/recording", 0.0, 1),
        )

    def _refresh_recordings(self):
        if not self.app or not hasattr(self.app, "db"):
            return
        self.recordings_box.clear_widgets()
        recordings = self.app.db.fetch_all("SELECT * FROM recordings WHERE is_personal = 1 ORDER BY created_at DESC LIMIT 10")
        if not recordings:
            self.recordings_box.add_widget(Label(text="لا توجد تسجيلات", halign="right", font_size=16, size_hint_y=None, height=40))
            return
        for rec in recordings:
            item = BoxLayout(orientation="horizontal", spacing=8, size_hint_y=None, height=50)
            item.add_widget(Label(text=rec["name"], halign="right", font_size=16))
            delete_btn = Button(text="u062dذf", size_hint_x=0.2)
            delete_btn.bind(on_release=lambda btn, rid=rec["id"]: self._delete_recording(rid))
            item.add_widget(delete_btn)
            self.recordings_box.add_widget(item)

    def _delete_recording(self, recording_id: int):
        if self.app and hasattr(self.app, "db"):
            self.app.db.execute("DELETE FROM recordings WHERE id = ?", (recording_id,))
            self._refresh_recordings()
