import hashlib

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from db_connector import mydb
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
Builder.load_file("views/auth/auth.kv")
class Auth(BoxLayout):
    def __init__(self, **kw):
        super().__init__(**kw)

    def reload(self,instace):
        App.get_running_app().root.ids.scrn_mngr.current = "scrn_auth"
        self.ids.password_field.text = ""
        self.dialog.dismiss()

    def authenticate(self):
        # the password from the form
        password = self.ids.password_field.text
        # hashed password from the form
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        # the type and the password from the database
        mycursor = mydb.cursor()
        mycursor.execute('SELECT password, staff_type FROM staff WHERE password=%s ', (hashed_password,))# tuple so i can avoid sql injection
        user_data = mycursor.fetchone() # returns None or True

        if user_data:
            stored_password, staff_type = user_data
            print("Authentication succesfull")
            if staff_type == 'waiter':
                App.get_running_app().root.ids.scrn_mngr.current = "scrn_home"
            elif staff_type == 'admin':
                App.get_running_app().root.ids.scrn_mngr.current= "home_admin"
            else:
                self.show_authentication_failed_dialog()

        else:
            self.show_authentication_failed_dialog()

    def show_authentication_failed_dialog(self):
        self.dialog = MDDialog(
            title="Authentication failed!",
            text="Please try again.",
            buttons=[
                MDFlatButton(
                    text="CLOSE",
                    on_press=self.reload
                )
            ],
            radius= [30,30,30,30],
            background_color=(1, 0, 0.12),

        )
        self.dialog.open()
        print("Authentication failed")





