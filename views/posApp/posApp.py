import os

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView

from views.auth import Auth
from views.error_window.ErrorMessageDialog import ErrorMessageDialog

Builder.load_file("views/posApp/posApp.kv")




class PosApp(MDScreen):

    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_once(self.render, .1)

    def menu_appear(self, table_id):
        global selected_table_id
        selected_table_id = table_id
        print("Selected table ID:", selected_table_id)
        App.get_running_app().root.ids.scrn_mngr.current = "scrn_menu"

    def get_table(self):
        print(selected_table_id)
        return selected_table_id

    def render(self, _):
        pass


class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()
