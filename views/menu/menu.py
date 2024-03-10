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

class MenuItem(MDBoxLayout):
    def __init__(self, id_food_item, name, price, category, img_name):
        super().__init__(orientation='vertical', adaptive_height=True, adaptive_width=True, padding=25, spacing=5,size_hint_y=None)
        self.id_food_item= id_food_item
        self.name = name
        self.price = price
        self.category = category
        self.img_name = img_name
        img_path = f'assets/imgs/food_items/{img_name}'
        image = Image(source=img_path, height=100, width=100, size_hint=(None, None))
        # !!!!!! id= img_name which is in the database
        button_name = MDFlatButton(text=name, halign='center', id= img_name)
        label_price = MDLabel(text=f'Price: ${price}', halign='center')
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

class Menu(MDScreen):

    pass

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

    # with type of meal
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

    # every meal
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



class BillHolder(MDScrollView):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.do_scroll_y = True  # Enable vertical scrolling
        self.bar_width = '12dp'  # Adjust the scrollbar width if needed
        # self.size_hint_y = None  # Set size_hint_y to None
        # self.height = Window.height  # Set the height to match parent height
        # # Create a grid layout to hold the content
        self.bill_layout = MDGridLayout(cols=1, size_hint_y=None, spacing='10dp', padding='10dp')
        self.bill_layout.bind(minimum_height=self.bill_layout.setter('height'))
        self.add_widget(self.bill_layout)

        # Add some labels as example content (replace with your own content)
        for i in range(20):
            label = MDLabel(text=f"Item {i}", size_hint=(None, None), size=(dp(200), dp(40)))
            self.bill_layout.add_widget(label)



