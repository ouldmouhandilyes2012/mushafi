from __future__ import annotations

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from screens.base import BaseScreen


class ProfileScreen(BaseScreen):
    def __init__(self, name: str, app=None, **kwargs):
        super().__init__(name=name, app=app, **kwargs)
        self.title_label.text = "الملف الشخصي"
        self.app = app

        self.container = BoxLayout(orientation="vertical", spacing=12, padding=12)

        profile = self.app.db.get_profile() if self.app and hasattr(self.app, "db") else {}

        self.container.add_widget(Label(text="الاسم:", halign="right", font_size=16, size_hint_y=None, height=30))
        self.name_input = TextInput(
            text=profile.get("display_name", "المستخدم"),
            multiline=False,
            font_size=18,
            size_hint_y=None,
            height=40,
        )
        self.container.add_widget(self.name_input)

        self.container.add_widget(Label(text="هدف الحفظ (عدد السور):", halign="right", font_size=16, size_hint_y=None, height=30))
        self.goal_input = TextInput(
            text=str(profile.get("memorization_goal", 30)),
            multiline=False,
            input_filter="int",
            font_size=18,
            size_hint_y=None,
            height=40,
        )
        self.container.add_widget(self.goal_input)

        self.container.add_widget(Label(text="هدف المراجعة (عدد الجلسات):", halign="right", font_size=16, size_hint_y=None, height=30))
        self.review_goal_input = TextInput(
            text=str(profile.get("review_goal", 10)),
            multiline=False,
            input_filter="int",
            font_size=18,
            size_hint_y=None,
            height=40,
        )
        self.container.add_widget(self.review_goal_input)

        self.save_btn = Button(text="حفظ", size_hint_y=None, height=50)
        self.save_btn.bind(on_release=self._save_profile)
        self.container.add_widget(self.save_btn)

        scroll = ScrollView(do_scroll_x=False)
        scroll.add_widget(self.container)
        self.add_widget(scroll)

    def _save_profile(self, instance):
        if not self.app or not hasattr(self.app, "db"):
            return
        try:
            self.app.db.update_profile(
                display_name=self.name_input.text,
                memorization_goal=int(self.goal_input.text) if self.goal_input.text else 30,
                review_goal=int(self.review_goal_input.text) if self.review_goal_input.text else 10,
            )
            self.title_label.text = "تم الحفظ بنجاح"
        except Exception as e:
            self.title_label.text = f"خطأ: {str(e)}"
