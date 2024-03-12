from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.image import Image
from kivymd.uix.label import MDLabel
from db_connector import mydb

Builder.load_file('views/menu/menu.kv')

# menuitem class is a box where i put the information for a single item(name, price, img_name)
class MenuItem(MDBoxLayout):
    # array used in one of the methods, it stores the selected items when a button of an item is pressed
    selected_items= []
    def __init__(self, id_food_item, name, price, category, img_name):
        super().__init__(orientation='vertical', adaptive_height=True, adaptive_width=True, padding=25, spacing=5,size_hint_y=None)
        self.id_food_item= id_food_item
        self.name = name
        self.price = price
        self.category = category
        self.img_name = img_name
        img_path = f'assets/imgs/food_items/{img_name}'
        image = Image(source=img_path, height=100, width=100, size_hint=(None, None))
        button_name = MDFlatButton(text=name, halign='center', id= img_name, on_press= self.on_menu_item_selected)
        label_price = MDLabel(text=f'Price: ${price}', halign='center')
        # adding the kivy widgets to the ui after we have the information
        self.add_widget(image)
        self.add_widget(button_name)
        self.add_widget(label_price)


    @classmethod
    def from_db_record(cls, db_record):
        id_food_item= db_record['id_food_item']
        name = db_record['name']
        price = db_record['price']
        category = db_record['category']
        img_name = db_record['img_name']
        return cls(id_food_item,name, price, category, img_name)

    #!!!!!thats the method i want to wrewrite so when i press a button the name
    # and the price of the pressed menu item should be added in the bill_layout(its a grid widget in the billholder scrollview
    # problem is i cant call bill_layout and i cant add the information to the scrollview.)!!!!!!
    def on_menu_item_selected(self, button_instance):
        # Append selected item to the class attribute selected_items
        MenuItem.selected_items.append({'name': self.name, 'price': self.price})
        # Calculate total price and add the selected item to the bill
        total = 0
        for item in MenuItem.selected_items:
            if 'name' in item and 'price' in item:
                total += item['price']
        print("Item name :"+ item['name']+" Item price: "+ str(item['price']) )
        # self.bill_holder.add_menu_item_to_bill(self.name, self.price)
        print(f"Total: ${total}")


class Menu(MDScreen):
    pass

# the scrollview where i vizualize all the menu items from the db
class MenuTable(MDScrollView):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.do_scroll_x = False
        self.size_hint_y = None  # Set size_hint_y to None

        self.menu_layout = MDGridLayout(cols=3, size_hint_y=None, size_hint_x=1,
                                        adaptive_height=True, adaptive_width=True, spacing=dp(5),
                                        padding=dp(10))
        self.add_widget(self.menu_layout)
        self.load_menu_items()

        # # Bind the function to be called when the window size changes
        # Window.bind(on_resize=self.on_window_resize)

    def clear_widgets_in_scrollview(self):
        self.menu_layout.clear_widgets()

    # method which i use when i want to select a specific type of meal(i have buttons for souprs, salads etc.)
    def load_type_of_meal(self, category):
        self.clear_widgets_in_scrollview()
        mycursor = mydb.cursor()
        query = f'SELECT * FROM food_item where category_id= "{category}"'
        mycursor.execute(query)
        results = mycursor.fetchall()

        for result in results:
            menu_item = MenuItem.from_db_record({
                'id_food_item': result[0],
                'name': result[1],
                'price': result[2],
                'category': result[3],
                'img_name': result[4]
            })
            self.menu_layout.add_widget(menu_item)

    # method which i use when i want to select all type of meals(i have button for all)
    def load_menu_items(self):
        self.clear_widgets_in_scrollview()
        mycursor = mydb.cursor()
        mycursor.execute('SELECT * FROM food_item')
        menu_items_data = mycursor.fetchall()
        for record in menu_items_data:
            menu_item = MenuItem.from_db_record({
                'id_food_item': record[0],
                'name': record[1],
                'price': record[2],
                'category': record[3],
                'img_name': record[4]
            })
            self.menu_layout.add_widget(menu_item)


# thats the class in which i want to put the information of the menu item
# (i should put it in the bill_layout like i put the labels as an example below(self.bill_layout.add_widget(label))).
# Its work is like a receipt
class BillHolder(MDScrollView):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.do_scroll_y = True  # Enable vertical scrolling
        self.bar_width = '12dp'  # Adjust the scrollbar width if needed
        # self.size_hint_y = None  # Set size_hint_y to None
        # self.height = Window.height  # Set the height to match parent height

        #  Create a grid layout to hold the content because in kivy we cant have only a scrollview in which we put the items
        self.bill_layout = MDGridLayout(cols=1, size_hint_y=None, spacing='10dp', padding='10dp')
        self.bill_layout.bind(minimum_height=self.bill_layout.setter('height'))
        #we add the grid widget to the scrollview
        self.add_widget(self.bill_layout)

        # Add some labels as example content so i cna see if the scrollview works properly (replace with the menu items content )
        for i in range(20):
            label = MDLabel(text=f"Item {i}", size_hint=(None, None), size=(dp(200), dp(40)))
            self.bill_layout.add_widget(label)