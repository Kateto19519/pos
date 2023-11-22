from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp, sp
from kivy.utils import rgba, QueryDict
from kivy.lang import Builder
from kivy.clock import Clock,mainthread
from kivy.properties import StringProperty,ListProperty, ColorProperty, NumericProperty

from kivymd.uix.toolbar import MDToolbar
from kivymd.icon_definitions import md_icons
from kivymd.app import MDApp
from kivymd.uix.list import OneLineIconListItem
Builder.load_file("views/posApp/posApp.kv")

class posApp(BoxLayout):
    def __init__(self, **kw) ->None:
         super().__init__(**kw)
         Clock.schedule_once(self.render, .1)

    def render(self, _):
        pass