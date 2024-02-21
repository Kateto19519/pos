from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty
from kivy.clock import Clock,mainthread
from kivymd.uix.scrollview import MDScrollView
from views.mi_add.menu_add import MenuAdd

Builder.load_file('views/home_admin/home_admin.kv')
class HomeAdmin(BoxLayout):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)




