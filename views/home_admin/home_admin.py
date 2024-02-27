
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.screen import MDScreen

Builder.load_file('views/home_admin/home_admin.kv')
class HomeAdmin(BoxLayout):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)




