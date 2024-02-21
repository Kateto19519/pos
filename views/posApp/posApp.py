from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock, mainthread
from kivy.properties import StringProperty, ListProperty, ColorProperty, NumericProperty, ObjectProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView


Builder.load_file("views/posApp/posApp.kv")

class PosApp(MDScreen):
    selected_table_id= StringProperty("")
    def __init__(self, **kw) ->None:
         super().__init__(**kw)
         Clock.schedule_once(self.render, .1)
    def menu_appear(self, table_id):
        self.selected_table_id = table_id
        App.get_running_app().root.ids.scrn_mngr.current= "scrn_menu"

    def render(self, _):
        pass


class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

