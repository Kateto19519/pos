from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp, sp
from kivy.utils import rgba, QueryDict
from kivy.lang import Builder
from kivy.clock import Clock, mainthread
from kivy.properties import StringProperty, ListProperty, ColorProperty, NumericProperty, ObjectProperty

from kivymd.uix.navigationdrawer import (
    MDNavigationLayout,
    MDNavigationDrawer,
    MDNavigationDrawerMenu,
    MDNavigationDrawerHeader,
    MDNavigationDrawerLabel,
    MDNavigationDrawerDivider,
    MDNavigationDrawerItem,
)
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.toolbar import MDTopAppBar



from kivymd.icon_definitions import md_icons

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivymd.icon_definitions import md_icons
from kivymd.uix.list import OneLineIconListItem

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

