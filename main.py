from __future__ import annotations

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from database.database import Database
from screens.home import HomeScreen
from screens.quran import QuranScreen
from screens.heart import HeartScreen
from screens.recitation import RecitationScreen
from screens.review import ReviewScreen
from screens.tafsir import TafsirScreen
from screens.statistics import StatisticsScreen
from screens.profile import ProfileScreen
from screens.settings import SettingsScreen


class MushafiApp(App):
    title = "مصحفي"

    def build(self):
        self.db = Database()
        self.screen_manager = ScreenManager()

        self.home_screen = HomeScreen(name="home", app=self)
        self.quran_screen = QuranScreen(name="quran", app=self)
        self.heart_screen = HeartScreen(name="heart", app=self)
        self.recitation_screen = RecitationScreen(name="recitation", app=self)
        self.review_screen = ReviewScreen(name="review", app=self)
        self.tafsir_screen = TafsirScreen(name="tafsir", app=self)
        self.statistics_screen = StatisticsScreen(name="statistics", app=self)
        self.profile_screen = ProfileScreen(name="profile", app=self)
        self.settings_screen = SettingsScreen(name="settings", app=self)

        for screen in [
            self.home_screen,
            self.quran_screen,
            self.heart_screen,
            self.recitation_screen,
            self.review_screen,
            self.tafsir_screen,
            self.statistics_screen,
            self.profile_screen,
            self.settings_screen,
        ]:
            self.screen_manager.add_widget(screen)

        self.screen_manager.current = "home"
        return self.screen_manager


if __name__ == "__main__":
    MushafiApp().run()
