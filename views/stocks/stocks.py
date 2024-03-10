from threading import Thread

from kivy.clock import Clock, mainthread
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from db_connector import mydb

Builder.load_file('views/stocks/stocks.kv')


class Stocks(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.render, .1)

    def render(self, _):
        Clock.schedule_once(self.get_food_items, 0.1)

    def get_food_items(self, _):
        t1 = Thread(target=self.fetch_food_items, daemon=True)
        t1.start()

    def fetch_food_items(self):
        food_items = self.get_food_items_from_db()
        self.set_food_items(food_items)

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

    @mainthread
    def set_food_items(self, food_items: list):
        grid = self.ids.gl_stocks
        grid.clear_widgets()

        for fi in food_items:
            food_tile = FoodItemTile()
            food_tile.name = fi['name']
            food_tile.price = fi['price']
            food_tile.category = self.get_category_name(fi['category_id'])  # Get category name
            food_tile.img_name = fi['img_name']
            # food_tile.callback = self.delete_food_item
            # food_tile.bind(on_release=self.update_food_item)
            grid.add_widget(food_tile)

    def get_category_name(self, category_id):
        # Fetch category name from your categories table based on the category ID
        mycursor = mydb.cursor()
        mycursor.execute("SELECT category_name FROM food_category WHERE id = %s", (category_id,))
        category = mycursor.fetchone()
        mycursor.close()

        if category:
            return category[0]  # Return category name
        else:
            return ""  # Return empty string if category not found


class FoodItemTile(ButtonBehavior, MDBoxLayout):
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
            self.callback(self)
