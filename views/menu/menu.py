from kivy.app import App
from kivymd.uix.screen import MDScreen

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
Builder.load_file("views/menu/menu.kv")

class Menu(MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)





