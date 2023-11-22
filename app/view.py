from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

class MainWindow(BoxLayout):
    username= StringProperty("first.samuel")
    role= StringProperty("user")
    def __init__(self, **kw):
        super().__init__(**kw)
