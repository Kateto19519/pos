import hashlib
import csv
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from db_connector import mydb

Builder.load_file("views/auth/auth.kv")

# Function to write user information to the CSV file
def write_user_info_to_csv(user_info):
    with open('user_info.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(user_info)

class Auth(BoxLayout):
    id_staff = StringProperty("")

    def __init__(self, **kw):
        super().__init__(**kw)

    def reload(self, instance):
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
        mycursor.execute('SELECT password,id_staff, staff_type FROM staff WHERE password=%s ', (hashed_password,))# tuple so i can avoid sql injection
        user_data = mycursor.fetchone() # returns None or True

        if user_data:
            stored_password, id_staff, staff_type = user_data  # Adjust the order of columns
            print("Authentication successful")
            self.id_staff = str(id_staff)

            # Write user information to the CSV file
            user_info = [staff_type, id_staff]
            write_user_info_to_csv(user_info)

            if staff_type == 'waiter':
                App.get_running_app().root.ids.scrn_mngr.current = "scrn_home"
            elif staff_type == 'admin':
                App.get_running_app().root.ids.scrn_mngr.current = "home_admin"
            else:
                self.show_authentication_failed_dialog()
        else:
            self.show_authentication_failed_dialog()
            print("No user data")

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
