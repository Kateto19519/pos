import hashlib
from threading import Thread
import mysql.connector
from kivy.clock import mainthread, Clock
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.modalview import ModalView
from kivymd.uix.boxlayout import MDBoxLayout
import datetime
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from db_connector import mydb

Builder.load_file('views/users/users.kv')

class Users(MDBoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.render, .1)

    def render(self, _):
        t1 = Thread(target=self.get_users, daemon=True)
        t1.start()

    def get_users_from_db(self):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM staff")

        rows = mycursor.fetchall()

        users = []
        for row in rows:
            user = {
                'id_staff': row[0], # we get the id but vizualize show it(for delete and update)
                'username': row[1],
                'password': row[2],
                'staff_type': row[3],
                'salary': str(row[4]),  # Convert to string
                'account_created': str(row[5])  # Convert to string
            }
            users.append(user)

        mycursor.close()
        return users

    def add_new(self):
        md = ModUser(callback=self.add_user)
        md.open()

    def add_user(self, user_data):
        # Method to add user data to UI
        grid = self.ids.gl_users
        ut = UserTile()
        ut.username = user_data['username']
        ut.password = user_data['password']
        ut.staff_type = user_data['staff_type']
        ut.salary = user_data['salary']
        ut.account_created = user_data['account_created']
        ut.callback = self.delete_user
        grid.add_widget(ut)
        self.get_users()

    def get_users(self):
        # Fetch users from the database
        users = self.get_users_from_db()
        self.set_users(users)


    @mainthread
    def set_users(self, users: list):
        grid = self.ids.gl_users
        grid.clear_widgets()

        for u in users:
            ut = UserTile()
            ut.id_staff=u['id_staff']
            ut.username = u['username']
            ut.password = u['password']
            ut.staff_type = u['staff_type']
            ut.salary = u['salary']
            ut.account_created = u['account_created']
            ut.callback= self.delete_user
            ut.bind(on_release=self.update_user)
            grid.add_widget(ut)



    def update_user(self, user):
        mv = ModUser()
        mv.username= user.username
        mv.staff_type= user.staff_type
        mv.salary= user.salary
        mv.callback= self.set_update
        mv.open()

    def set_update(self):
        print("Updating....")

    def delete_user(self, staff_id):
        # Method to delete the staff member from the database
        if staff_id:
            dc = DeleteConfirm(callback=self.remove_user_from_ui, staff_id=staff_id)
            dc.open()

    def remove_user_from_ui(self, staff_id):
        # Method to remove the user from UI based on staff_id
        for widget in self.ids.gl_users.children:
            if isinstance(widget, UserTile) and widget.id_staff == staff_id:
                self.ids.gl_users.remove_widget(widget)
                break





class UserTile(ButtonBehavior, MDBoxLayout):
    id_staff = NumericProperty()
    username = StringProperty("")
    password = StringProperty("")
    staff_type = StringProperty("")
    salary = StringProperty("")
    account_created = StringProperty("")
    callback = ObjectProperty(allowone=True)
    user_data = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.render, .1)

    def render(self, _):
        pass

    def delete_user(self):
        if self.callback:
            self.callback(self.id_staff)


class DeleteConfirm(ModalView):
    callback = ObjectProperty(allowone=True)
    user_data = ObjectProperty(None)
    id_staff = NumericProperty()

    def __init__(self, callback=None, user_data=None, staff_id=None, **kw) -> None:
        super().__init__(**kw)
        self.callback = callback
        self.user_data = user_data
        self.id_staff = staff_id
        Clock.schedule_once(self.render, .1)

    def render(self, _):
        pass

    def delete_from_db(self):
        if self.id_staff:
            mycursor = mydb.cursor()
            sql = "DELETE FROM staff WHERE id_staff = %s"
            val = (self.id_staff,)

            try:
                mycursor.execute(sql, val)
                mydb.commit()
                print("User deleted successfully.")
                if self.callback:
                    self.callback(self.id_staff)
            except mysql.connector.Error as e:
                print("Error deleting user:", e)
                mydb.rollback()
            finally:
                mycursor.close()

        self.dismiss()

class ModUser(ModalView):
    username = StringProperty("")
    staff_type = StringProperty("")
    salary = StringProperty("")
    account_created = StringProperty("")
    callback = ObjectProperty(allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def render(self, _):
        pass

    def spinner_clicked(self, value):
        print(value)
        self.staff_type = value  # Set the staff_type property in ModUser
        self.selected_staff_type = value  # Store selected staff type
        return value

    def add_user(self):
        username = self.ids.username_field.text.strip()
        password = self.ids.passcode_field.text
        confirmed_passcode = self.ids.passcode_confirm_field.text
        staff_type = self.ids.staff_type.text
        salary = self.ids.salary_field.text
        account_created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not (username and password and confirmed_passcode and staff_type and salary):
            self.show_dialog("Couldn't add a new staff member.", "Please fill in all the fields.")
            return

        if len(username) < 2:
            self.show_dialog("Couldn't add a new staff member.", "Username should be more than two letters.")
            return
        elif password != confirmed_passcode:
            self.show_dialog("Couldn't add a new staff member.", "Passwords do not match.")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        mycursor = mydb.cursor()
        sql = "INSERT INTO staff (username, password, staff_type, salary, account_created) VALUES (%s, %s, %s, %s, %s)"
        val = (username, hashed_password, staff_type, salary, account_created)

        try:
            mycursor.execute(sql, val)
            mydb.commit()

            user = {
                "username": username,
                "password": hashed_password,
                "staff_type": staff_type,
                "salary": salary,
                "account_created": account_created
            }

            # Close the cursor before invoking the callback
            mycursor.close()

            # Call the callback function provided by the Users class to update the UI
            if self.callback:
                self.callback(user)

            self.show_dialog("Staff member added successfully.", f"{username} was added successfully to the database.")

        except mysql.connector.Error:
            self.show_dialog("Couldn't add a new staff member.",
                             "An error occurred while adding the user. "
                             "Try entering the details again or contact the developer for more information.")
            mydb.rollback()
        finally:
            mycursor.close()
    def update_user(self):
        pass
    def on_username(self, inst, username):
        self.ids.username_field.text= username
        self.ids.btn_confirm.text= "Update"
        self.ids.title.text="Update User"
        self.ids.subtitle.text= "Enter the details below to update the staff member"

    def on_staff_type(self, inst, staff_type):
        self.ids.staff_type.text = staff_type


    def on_salary(self, inst, salary):
        self.ids.salary_field.text = salary


    @mainthread
    def show_dialog(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(
                    text="CLOSE",
                    on_release=lambda *args: dialog.dismiss()
                )
            ]
        )
        dialog.open()