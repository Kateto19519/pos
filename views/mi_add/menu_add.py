from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen

Builder.load_file('views/mi_add/menu_add.kv')
class MenuAdd(MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)

