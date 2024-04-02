import hashlib
import os
from shutil import copyfile
from threading import Thread
import mysql.connector
from kivy.clock import mainthread, Clock
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.uix import popup
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.modalview import ModalView
from kivy.uix.popup import Popup
from kivymd.uix.boxlayout import MDBoxLayout
import datetime
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from db_connector import mydb
from decimal import Decimal

Builder.load_file('views/stocks/stocks.kv')

class Stocks(MDBoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.render, .1)

    def render(self, _):
        t1 = Thread(target=self.get_food_items, daemon=True)
        t1.start()

    def get_food_items_from_db(self):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM food_item")

        rows = mycursor.fetchall()

        food_items = []
        for row in rows:
            food_item = {
                'id_food_item': row[0],
                'name': str(row[1]),
                'price': str(row[2]),
                'category_id': int(row[3]),  # Store category ID as int
                'img_name': str(row[4]),  # Convert to string
            }
            food_items.append(food_item)

        mycursor.close()
        return food_items

    def add_new_food_item(self):
        md = ModFoodItem(stocks_instance=self, callback=self.add_food_item)
        md.open()

    def add_food_item(self, food_item_data):
        grid = self.ids.gl_stocks
        ft = FoodItemTile()
        ft.name = food_item_data['name']
        ft.price = str(food_item_data['price'])
        ft.category = food_item_data['category']
        ft.img_name = food_item_data['img_name']
        ft.callback = self.delete_food_item
        grid.add_widget(ft)

    def get_food_items(self):
        food_items = self.get_food_items_from_db()
        self.set_food_items(food_items)

    @mainthread
    def set_food_items(self, food_items: list):
        grid = self.ids.gl_stocks
        grid.clear_widgets()

        for fi in food_items:
            ft = FoodItemTile()
            ft.name = fi['name']
            ft.price = fi['price']
            ft.category = self.get_category_name(fi['category_id'])  # Get category name
            ft.img_name = fi['img_name']
            ft.callback = self.delete_food_item
            grid.add_widget(ft)

    def get_category_name(self, category_id):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT category_name FROM food_category WHERE id = %s", (category_id,))
        category = mycursor.fetchone()
        mycursor.close()

        if category:
            return category[0]  # Return category name
        else:
            return ""  # Return empty string if category not found

    def delete_food_item(self, food_item_id):
        if food_item_id:
            dc = DeleteConfirm(callback=self.remove_food_item_from_ui, food_item_id=food_item_id)
            dc.open()

    def remove_food_item_from_ui(self, food_item_id):
        for widget in self.ids.gl_stocks.children:
            if isinstance(widget, FoodItemTile) and widget.id_food_item == food_item_id:
                self.ids.gl_stocks.remove_widget(widget)
                break

class FoodItemTile(ButtonBehavior, MDBoxLayout):
    id_food_item = NumericProperty()
    name = StringProperty("")
    price = StringProperty("")
    category = StringProperty("")
    img_name = StringProperty("")
    callback = ObjectProperty(allowone=True)
    food_item_data = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.render, .1)

    def render(self, _):
        pass

    def delete_food_item(self):
        if self.callback:
            self.callback(self.id_food_item)

class DeleteConfirm(ModalView):
    callback = ObjectProperty(allowone=True)
    food_item_data = ObjectProperty(None)
    food_item_id = NumericProperty(None)

    def __init__(self, callback=None, food_item_data=None, food_item_id=None, **kw) -> None:
        super().__init__(**kw)
        self.callback = callback
        self.food_item_data = food_item_data
        self.food_item_id = food_item_id
        Clock.schedule_once(self.render, .1)

    def render(self, _):
        pass

    def delete_from_db(self):
        if self.food_item_id:
            mycursor = mydb.cursor()
            sql = "DELETE FROM food_item WHERE id_food_item = %s"
            val = (self.food_item_id,)

            try:
                mycursor.execute(sql, val)
                mydb.commit()
                print("Food item deleted successfully.")
                if self.callback:
                    self.callback(self.food_item_id)
            except mysql.connector.Error as e:
                print("Error deleting food item:", e)
                mydb.rollback()
            finally:
                mycursor.close()

        self.dismiss()

    @classmethod
    @mainthread
    def show_dialog(cls, title, text):
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

class ModFoodItem(ModalView):
    name = StringProperty("")
    price = StringProperty("")
    category = StringProperty("")
    img_name = StringProperty("")
    callback = ObjectProperty(allownone=True)
    id_food_item = NumericProperty(None)
    stocks_instance = ObjectProperty(None)
    selected_photo_path = StringProperty("")  # Store the selected photo path

    def __init__(self, id_food_item=None, food_item_data=None, stocks_instance=None, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.render, .1)
        self.id_food_item = id_food_item
        self.food_item_data = food_item_data
        self.stocks_instance = stocks_instance
        self.selected_photo_path = ""  # Initialize selected photo path

        if food_item_data:
            self.name = food_item_data.get('name', '')
            self.price = food_item_data.get('price', '')
            self.category = food_item_data.get('category', '')
            self.img_name = food_item_data.get('img_name', '')
            self.ids.btn_confirm.text = "Update"
            self.ids.title.text = "Update Food Item"
            self.ids.subtitle.text = "Enter the details below to update the food item"
        else:
            self.ids.btn_confirm.text = "Add"
            self.ids.title.text = "Add Food Item"
            self.ids.subtitle.text = "Enter the details below to add a new food item"

    def render(self, _):
        pass

    def select_photo(self):
        file_chooser = FileChooserIconView()
        file_chooser.bind(on_submit=self.photo_selected)

        popup = Popup(title="Select Photo", content=file_chooser, size_hint=(None, None), size=(400, 400))
        popup.open()

    def photo_selected(self, chooser, selection):
        if selection:
            self.selected_photo_path = selection[0]  # Store selected file path
            img_name_field = self.ids.img_name_field
            img_name_field.text = os.path.basename(self.selected_photo_path)  # Update the text input with the selected filename
            chooser.parent.dismiss()  # Dismiss the popup after selecting the file

    def add_food_item(self):
        name = self.ids.name_field.text.strip()
        price = self.ids.price_field.text.strip()
        category_name = self.ids.category_field.text.strip()  # Get category name
        img_name = self.ids.img_name_field.text.strip()

        if not (name and price and category_name and img_name):
            DeleteConfirm.show_dialog("Couldn't add a new food item.", "Please fill in all the fields.")
            return

        try:
            price = Decimal(price)  # Convert price to Decimal
        except ValueError:
            DeleteConfirm.show_dialog("Couldn't add a new food item.", "Price should be a valid number.")
            return

        mycursor = mydb.cursor()
        # Query to fetch category ID from food_category table based on category name
        category_query = "SELECT id FROM food_category WHERE category_name = %s"
        category_val = (category_name,)
        mycursor.execute(category_query, category_val)
        category_result = mycursor.fetchone()

        if category_result:
            category_id = category_result[0]  # Extract category ID
        else:
            # If category name not found, show error dialog and return
            DeleteConfirm.show_dialog("Couldn't add a new food item.", "Invalid category name.")
            mycursor.close()
            return

        sql = "INSERT INTO food_item (name, price, category_id, img_name) VALUES (%s, %s, %s, %s)"
        val = (name, price, category_id, img_name)

        try:
            mycursor.execute(sql, val)
            mydb.commit()

            food_item = {
                "name": name,
                "price": str(price),  # Assign price as string
                "category": category_name,
                "img_name": img_name,
            }

            mycursor.close()

            if self.callback:
                self.callback(food_item)

            DeleteConfirm.show_dialog("Food item added successfully.", f"{name} was added successfully.")

            # Copy uploaded photo to the specified directory
            if self.selected_photo_path:
                # Get the full path of the uploaded file
                uploaded_file_path = self.selected_photo_path
                # Define the destination directory and filename
                destination_directory = os.path.join("assets", "imgs", "food_items")
                destination_file_path = os.path.join(destination_directory, img_name)
                # Create the destination directory if it doesn't exist
                os.makedirs(destination_directory, exist_ok=True)
                # Copy the uploaded file to the destination directory with the specified filename
                copyfile(uploaded_file_path, destination_file_path)

        except mysql.connector.Error:
            DeleteConfirm.show_dialog("Couldn't add a new food item.",
                                      "An error occurred while adding the food item. "
                                      "Try entering the details again or contact the developer for more information.")
            mydb.rollback()
        finally:
            mycursor.close()

    def on_name(self, inst, name):
        self.ids.name_field.text = name
        self.ids.btn_confirm.text = "Update" if name else "Add"
        self.ids.title.text = "Update Food Item" if name else "Add Food Item"
        self.ids.subtitle.text = "Enter the details below to update the food item" if name else "Enter the details below to add a new food item"

    def on_price(self, inst, price):
        self.ids.price_field.text = price

    def on_category(self, inst, category):
        self.ids.category_field.text = category

    def on_img_name(self, inst, img_name):
        self.ids.img_name_field.text = img_name