import os

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView

from views.auth import Auth

Builder.load_file("views/posApp/posApp.kv")


class PosApp(MDScreen):
    selected_table_id = NumericProperty(0)

    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        Clock.schedule_once(self.render, .1)

    def menu_appear(self, table_id):
        self.selected_table_id = table_id
        print(self.selected_table_id)
        App.get_running_app().root.ids.scrn_mngr.current = "scrn_menu"

    @classmethod
    def get_table(cls):
        selected_table = cls.selected_table_id
        print(selected_table)
        return selected_table

    def render(self, _):
        pass



class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()
