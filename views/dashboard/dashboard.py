from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout


Builder.load_file('views/dashboard/dashboard.kv')
class Dashboard(BoxLayout):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)

