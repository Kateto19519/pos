from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

class MainWindow(BoxLayout):

    def __init__(self, **kw):
        super().__init__(**kw)

    def logout(self, item, text):
        if text == 'Log out':
            # Perform logout functionality here
            App.get_running_app().stop()

