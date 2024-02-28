import hashlib
from threading import Thread
import mysql.connector
from kivy.clock import mainthread, Clock
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.modalview import ModalView
from kivymd.uix.boxlayout import MDBoxLayout
import datetime
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from db_connector import mydb

Builder.load_file('views/stocks/stocks.kv')

class Stocks(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.render, .1)

    def render(self,_):
        pass

#     def render(self, _):
#         t1 = Thread(target=self.get_food_items, daemon=True)
#         t1.start()
#
#     def get_menu_items_from_db(self):
#         mycursor = mydb.cursor()
#         mycursor.execute("SELECT * FROM food_item")
#
#         rows = mycursor.fetchall()
#
#         food_items = []
#         for row in rows:
#             food_item = {
#                 'Name': row[1],
#                 'price': row[2],
#                 'category_id': row[3],
#                 'img_name': str(row[4]),  # Convert to string
#
#             }
#             food_items.append(food_item)
#
#         mycursor.close()
#         return food_items
#
#     def add_new(self):
#         md = ModStock(callback=self.add_food_item)
#         md.open()
#
#     def add_food_item(self, food_item_data):
#         # Method to add user data to UI
#         grid = self.ids.gl_stocks
#         ut = FoodItemTile()
#         ut.name = food_item_data['name']
#         ut.price = food_item_data['price']
#         ut.category = food_item_data['category']
#         ut.img_name = food_item_data['img_name']
#
#         grid.add_widget(ut)
#
#     def get_food_items(self):
#         # Fetch users from the database
#         users = self.get_menu_items_from_db()
#         self.set_food_items(users)
#
#     @mainthread
#     def set_food_items(self, food_items: list):
#         grid = self.ids.gl_stocks
#         grid.clear_widgets()
#
#         for fi in food_items:
#             fi = FoodItemTile()
#             fi.name = fi['name']
#             fi.password = fi['price']
#             fi.staff_type = fi['category']
#             fi.salary = fi['img_name']
#             fi.callback= self.delete_food_item
#             fi.bind(on_release=self.update_food_item)
#             grid.add_widget(fi)
#
#     def update_food_item(self, food_item):
#         mv = ModStock()
#         mv.name= food_item.name
#         mv.price= food_item.price
#         mv.category= food_item.category
#         mv.img_name= self.img_name
#
#         mv.open()
#
#     def set_update(self, mv):
#         print("Updating....")
#
#     def delete_food_item(self, user):
#         dc = DeleteConfirm()
#         dc.open()
#
#
#
# class FoodItemTile(ButtonBehavior,MDBoxLayout):
#     name = StringProperty("")
#     price = StringProperty("")
#     category = StringProperty("")
#     img_name = StringProperty("")
#     callback = ObjectProperty(allowone=True)
#     food_item_data = ObjectProperty(None)
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         Clock.schedule_once(self.render, .1)
#
#     def render(self, _):
#         pass
#
#     def delete_food_item(self):
#         if self.callback:
#             self.callback(self)
#
# class DeleteConfirm(ModalView):
#     callback= ObjectProperty(allowone= True)
#     food_item_data= ObjectProperty(None)
#
#     def __init__(self, user_data=None, **kw) -> None:
#         super().__init__(**kw)
#         self.food_item_data = user_data
#         Clock.schedule_once(self.render, .1)
#
#     def render(self, _):
#         pass
#     def complete(self):
#         self.dismiss()
#
#         if self.callback:
#             self.callback(self)
#
# class ModStock(ModalView):
#     name = StringProperty("")
#     price = StringProperty("")
#     category = StringProperty("")
#     img_name = StringProperty("")
#     callback = ObjectProperty(allownone=True)
#
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#
#     def render(self, _):
#         pass
#
#     def spinner_clicked(self, value):
#         print(value)
#         self.staff_type = value  # Set the staff_type property in ModifyUser
#         self.selected_staff_type = value  # Store selected staff type
#         return value
#
#     def add_food_item(self):
#         name = self.ids.name_field.text.strip()
#         price = self.ids.price_field.text
#         categopry_id = self.ids.category.text
#         img_name = self.ids.img_name.text
#
#         if not (name and price and categopry_id and img_name):
#             self.show_dialog("Couldn't add a new staff member.", "Please fill in all the fields.")
#             return
#
#
#
#         mycursor = mydb.cursor()
#         sql = "INSERT INTO food_item (name, price, category_id, img_name) VALUES (%s, %s, %s, %s, %s)"
#         val = (name, price, categopry_id, img_name)
#
#         try:
#             mycursor.execute(sql, val)
#             mydb.commit()
#
#             food_item = {
#                 "name": name,
#                 "price": price,
#                 "category_id": categopry_id,
#                 "img_name": img_name,
#
#             }
#
#             # Close the cursor before invoking the callback
#             mycursor.close()
#
#             # Call the callback function provided by the Users class to update the UI
#             if self.callback:
#                 self.callback(food_item)
#
#             self.show_dialog("Menu item added successfully.", f"{food_item} was added successfully to the database.")
#
#         except mysql.connector.Error:
#             self.show_dialog("Couldn't add a new staff member.",
#                              "An error occurred while adding the user. "
#                              "Try entering the details again or contact the developer for more information.")
#             mydb.rollback()
#         finally:
#             mycursor.close()
#     def update_menu_item(self):
#         pass
#     def on_username(self, inst, username):
#         self.ids.username_field.text= username
#         self.ids.btn_confirm.text= "Update"
#         self.ids.title.text="Update User"
#         self.ids.subtitle.text= "Enter the details below to update the staff member"
#
#     def on_staff_type(self, inst, staff_type):
#         self.ids.staff_type.text = staff_type
#         self.ids.title.text = "Update User"
#         self.ids.subtitle.text = "Enter the details below to update the staff member"
#
#     def on_salary(self, inst, salary):
#         self.ids.salary_field.text = salary
#         self.ids.title.text = "Update User"
#         self.ids.subtitle.text = "Enter the details below to update the staff member"
#
#     @mainthread
#     def show_dialog(self, title, text):
#         dialog = MDDialog(
#             title=title,
#             text=text,
#             buttons=[
#                 MDFlatButton(
#                     text="CLOSE",
#                     on_release=lambda *args: dialog.dismiss()
#                 )
#             ]
#         )
#         dialog.open()