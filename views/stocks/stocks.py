from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout


Builder.load_file('views/stocks/stocks.kv')
class Stocks(BoxLayout):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)

    def render(self,_):
        pass