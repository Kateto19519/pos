from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView

from db_connector import mydb

Builder.load_file('views/menu/menu.kv')


class BillParent(MDBoxLayout):
    bill_holder_inst = ObjectProperty(None)


# това е класа, който е кутия в която слагам снимката, името и цената на продукта, които са взети от базата.
# Всяко ястие или напитка седи в такава кутия
class MenuItem(MDBoxLayout):
    # масив, който се пълни с елементите, които съм селектирала като съм натиснала бутона на конкретното ястието
    selected_items = []

    def __init__(self, id_food_item, name, price, category, img_name):
        super().__init__(orientation='vertical', adaptive_height=True, adaptive_width=True, padding=25, spacing=5,
                         size_hint_y=None)
        self.id_food_item = id_food_item
        self.name = name
        self.price = price
        self.category = category
        self.img_name = img_name
        img_path = f'assets/imgs/food_items/{img_name}'
        image = Image(source=img_path, height=100, width=100, size_hint=(None, None))
        button_name = MDFlatButton(text=name, halign='center', id=img_name, on_press=self.on_menu_item_selected)
        label_price = MDLabel(text=f'Price: ${price}', halign='center')
        # adding the kivy widgets to the ui after we have the information
        self.add_widget(image)
        self.add_widget(button_name)
        self.add_widget(label_price)

    @classmethod
    def from_db_record(cls, db_record):
        id_food_item = db_record['id_food_item']
        name = db_record['name']
        price = db_record['price']
        category = db_record['category']
        img_name = db_record['img_name']
        return cls(id_food_item, name, price, category, img_name)

    # !!!!!това е единия метод, който трябва да се пренапишa, така че да може да взима информацията за
    # продукта-цена и име, и да я добавя като киви лейбъл в BillHolder scrollview-то. Предполагам просто трябва да прекарам информацияат
    # до Billholder класа и там да
    # създам самия лейбъл, защото за да добавя лейбъл ми е нужно да имам грида bill_layout
    def on_menu_item_selected(self, button_instance):
        # принтирането е само за да пробвам дали работи, в конзолата се принтират с правилната информация от базата,
        # просто трябва да се визуализира и като ui в BillHolder класа
        MenuItem.selected_items.append({'name': self.name, 'price': self.price})
        total = 0
        for item in MenuItem.selected_items:
            if 'name' in item and 'price' in item:
                total += item['price']
        print("Item name :" + item['name'] + " Item price: " + str(item['price']))
        print(f"Total: ${total}")

        bill_holder = self.parent.parent.parent.bill_holder_inst
        bill_holder.add_to_bill(self.name, self.price)
        # bill_holder.add_widget(MDLabel(text= f" Total: ${total}"))

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

    # method which i use when i want to select a specific type of meal(i have buttons for soups, salads etc.)
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

    # method which i use when i want to select all type of meals(i have button  'all')
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


# това е класа с който искам да направя връзка(между него и меню айтем класа). Добавила съм лейбъли за да видя дали работи както трябва.
# вместо тези лейбъли трябва да се визуализира име и цена на ястието, на което съм натиснала бутона
class BillHolder(MDScrollView):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.do_scroll_y = True
        self.bar_width = '12dp'
        # тук създавам въпросния bill_layout(грида), за да добавям в него лейбълите с цена и име на ястие
        self.bill_layout = MDGridLayout(cols=1, size_hint_y=None, spacing='10dp', padding='10dp')
        self.bill_layout.bind(minimum_height=self.bill_layout.setter('height'))
        self.add_widget(self.bill_layout)
        # # просто за тест дали изглежда окей когато сложа лейбъли във scrollviewto
        # for i in range(10):
        #     label = MDLabel(text=f"Item {i} Price: $3,50", size_hint=(None, None), size=(dp(200), dp(40)))
        #     self.bill_layout.add_widget(label)

    # !!!!! втория метод, който използвам за логиката със сметката. Връзката предполагам трябва да е между този метод и
    # on_menu_item_selected в MenuItems
    # но така и не успях да направя връзката между двата класа и двата метода
    def add_to_bill(self, name, price):
        label = MDLabel(text=f"{name} - ${price}", size_hint=(None, None), size=(dp(200), dp(40)))
        self.bill_layout.add_widget(label)
