import os
import mysql.connector
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel

import app

Builder.load_file('views/dashboard/dashboard.kv')

class Dashboard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            port=8111,
            database="pos_system"
        )
        # Schedule the update_best_sellers method to run after a short delay
        Clock.schedule_once(self.update_best_sellers)

    def update_best_sellers(self, dt):
        cursor = self.mydb.cursor()

        # Query to select top 5 best-selling products with their IDs
        query = """
        SELECT food_item_id, COUNT(*) AS count 
        FROM pos_system.order_items 
        GROUP BY food_item_id 
        ORDER BY count DESC 
        LIMIT 5
        """
        cursor.execute(query)
        top_sellers_with_ids = cursor.fetchall()

        # Access the ScrollView by ID
        best_sellers_scrollview = self.ids.best_sellers_scrollview

        # Clear existing children
        best_sellers_scrollview.clear_widgets()

        # Create a layout widget to contain the text widgets
        layout = MDGridLayout(cols=1, spacing=5, size_hint_y=None)

        # Retrieve names of the top-selling items based on their IDs
        top_seller_names = []
        for food_item_id, _ in top_sellers_with_ids:
            name_query = "SELECT name FROM food_item WHERE id_food_item = %s"
            cursor.execute(name_query, (food_item_id,))
            result = cursor.fetchone()
            if result:
                top_seller_names.append(result[0])
            else:
                top_seller_names.append("Unknown")

        # Add new children (best-selling items) to the layout
        number=1
        for name in top_seller_names:
            text_widget = MDLabel(text=str(number)+"."+ name, size_hint_y=None, height=30)
            layout.add_widget(text_widget)
            number+=1

        # Add the layout as the single child of the ScrollView
        best_sellers_scrollview.add_widget(layout)

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