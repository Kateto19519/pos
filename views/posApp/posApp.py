import kv
from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp, sp
from kivy.utils import rgba, QueryDict
from kivy.lang import Builder
from kivy.clock import Clock, mainthread
from kivy.properties import StringProperty, ListProperty, ColorProperty, NumericProperty, ObjectProperty

from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView


Builder.load_file("views/posApp/posApp.kv")

class PosApp(MDScreen):
    def __init__(self, **kw) ->None:
         super().__init__(**kw)
         Clock.schedule_once(self.render, .1)

    def render(self, _):
        pass


class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

