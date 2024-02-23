from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout


Builder.load_file('views/users/users.kv')
class Users(BoxLayout):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)



