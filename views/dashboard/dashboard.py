import os

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout


Builder.load_file('views/dashboard/dashboard.kv')
class Dashboard(BoxLayout):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)

    def render(self,_):
        pass

    def logout(self, spinner, text):
        if text == 'Log out':
            self.clear_user_data()
            App.get_running_app().root.ids.scrn_mngr.current = "scrn_auth"


    def clear_user_data(self):
        # Specify the path to the CSV file
        csv_file_path = "user_info.csv"
        # Check if the file exists
        if os.path.exists(csv_file_path):
            # Open the file in write mode to clear its contents
            with open(csv_file_path, "w") as file:
                file.truncate(0)
        else:
            print("CSV file does not exist.")