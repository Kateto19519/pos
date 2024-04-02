from datetime import datetime
import mysql
import qrcode
from kivy._event import defaultdict
from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDIconButton, MDRectangleFlatIconButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from db_connector import mydb
from views.posApp import posApp

Builder.load_file('views/menu/menu.kv')


class BillParent(MDBoxLayout):
    bill_holder_inst = ObjectProperty(None)


class MenuItem(MDBoxLayout):
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

    def on_menu_item_selected(self, button_instance):
        MenuItem.selected_items.append({'id_food_item': self.id_food_item, 'name': self.name, 'price': self.price})
        total = 0
        for item in MenuItem.selected_items:
            if 'name' in item and 'price' in item:
                total += item['price']
        print("Item name :" + item['name'] + " Item price: " + str(item['price']))
        print(f"Total: ${total}")

        bill_holder = self.parent.parent.parent.bill_holder_inst
        bill_holder.add_to_bill(self.name, self.price)


class Menu(MDScreen):
    def go_back(self):
        self.manager.current = 'scrn_home'

class MenuTable(MDScrollView):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.do_scroll_x = False
        self.size_hint_y = None
        self.menu_layout = MDGridLayout(cols=3, size_hint_y=None, size_hint_x=1,
                                        adaptive_height=True, adaptive_width=True, spacing=dp(5),
                                        padding=dp(10))
        self.add_widget(self.menu_layout)
        self.load_menu_items()

    def clear_widgets_in_scrollview(self):
        self.menu_layout.clear_widgets()

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
        self.do_scroll_y = True
        self.bar_width = '12dp'
        self.bill_layout = MDGridLayout(cols=1, size_hint_y=None, spacing='10dp', padding='10dp')
        self.bill_layout.bind(minimum_height=self.bill_layout.setter('height'))
        self.add_widget(self.bill_layout)
        self.total_label = MDLabel(text="Total: $0.00", size_hint=(None, None), size=(dp(200), dp(40)),
                                   theme_text_color="Error")

        # Horizontal layout to hold buttons
        self.button_layout = MDBoxLayout(size_hint_y=None, height=dp(40), spacing='10dp')

        self.receipt_label = MDLabel(text="Receipt", size_hint_y=None, height=dp(40), font_size='40dp',
                                     theme_text_color="Error", halign="center")
        self.bill_layout.add_widget(self.receipt_label)

        # Button for finishing
        self.finish_button = MDRectangleFlatIconButton(icon='printer-pos', text="Finish", on_press=self.generate_pdf)

        # Add the buttons to the button layout
        self.button_layout.add_widget(self.finish_button)

        # Add the button layout to the bill layout
        self.bill_layout.add_widget(self.button_layout)

    def generate_pdf(self, instance):
        try:
            print("Generating PDF with order details...")
            c = canvas.Canvas('order_receipt.pdf', pagesize=letter)
            width, height = letter
            margin = 72
            line_height = 14
            current_height = height - margin

            # Header setup
            c.setFont("Helvetica-Bold", 12)
            c.drawString(margin, current_height, "Katy's Restaurant")
            current_height -= line_height * 2

            # Table headers
            c.setFont("Helvetica", 10)
            c.drawString(margin, current_height, "Qty")
            c.drawString(margin + 50, current_height, "Item")
            c.drawString(width - margin - 100, current_height, "Unit Price")
            c.drawString(width - margin - 50, current_height, "Sum")
            current_height -= line_height

            # Aggregate items by name
            item_aggregate = defaultdict(lambda: {'quantity': 0, 'price': 0})
            for item in MenuItem.selected_items:
                item_aggregate[item['name']]['quantity'] += 1
                item_aggregate[item['name']]['price'] = item['price']  # Assuming all items have the same price

            # Item listing
            for item_name, details in item_aggregate.items():
                quantity = details['quantity']
                price = details['price']
                sum_price = quantity * price
                c.drawString(margin, current_height, str(quantity))
                c.drawString(margin + 50, current_height, item_name)
                c.drawString(width - margin - 100, current_height, f"${price:.2f}")
                c.drawString(width - margin - 50, current_height, f"${sum_price:.2f}")
                current_height -= line_height

            # Draw the total
            c.setFont("Helvetica-Bold", 10)
            total = sum(details['price'] * details['quantity'] for details in item_aggregate.values())
            c.drawString(width - margin - 100, current_height, "Total:")
            c.drawString(width - margin - 50, current_height, f"${total:.2f}")
            current_height -= line_height * 2  # Add an extra line space before the QR code

            # Add the current date and time below and to the left of the QR code
            current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            c.drawString(margin, margin, f"Date: {current_date_time}")

            # Barcode and QR code generation
            barcode_value = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{total:.2f}"
            # The QR Code generation
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(barcode_value)
            qr.make(fit=True)
            qr_code = qr.make_image(fill_color="black", back_color="white")

            # Save QR code to a file
            qr_code_path = 'qr_code.png'
            qr_code.save(qr_code_path)

            # Draw QR code onto the PDF
            barcode_width = 100  # Adjust this width based on the barcode size
            barcode_x = (width - margin - barcode_width) / 2

            # Calculate the position to center the barcode vertically
            barcode_height = 100  # Adjust this height based on the barcode size
            barcode_y = current_height - barcode_height - line_height * 2  # Adjust the y position as needed

            # Draw QR code onto the PDF
            c.drawInlineImage(qr_code_path, barcode_x, barcode_y, width=barcode_width, height=barcode_height)

            # Save the PDF
            c.showPage()
            c.save()

            print('PDF generated successfully.')


            app = App.get_running_app()
            app.root.ids.scrn_mngr.current = 'scrn_home'

        except Exception as e:
            print("Failed to generate PDF:", e)

    def add_to_bill(self, name, price):
        label = MDLabel(text=f"{name} - ${price}", size_hint=(None, None), size=(dp(200), dp(40)))
        self.bill_layout.add_widget(label)

        # Calculate total price, including the newly added item but excluding the total label and labels without prices
        total_price = sum(float(child.text.split("$")[-1]) for child in self.bill_layout.children
                          if child not in [self.total_label, self.receipt_label]
                          and "$" in getattr(child, "text", ""))
        self.total_label.text = f"Total: ${total_price:.2f}"

        # Remove total label if already added
        if self.total_label in self.bill_layout.children:
            self.bill_layout.remove_widget(self.total_label)

        self.bill_layout.add_widget(self.total_label)


    def add_to_db(self, instance):
        try:
            print("Adding order to the database...")

            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                port=8111,
                database="pos_system"
            )

            cursor = mydb.cursor()

            # Hardcoded table
            table = posApp.get_table()

            # List to store food item IDs
            food_ids = [item['id_food_item'] for item in MenuItem.selected_items]  # Extract IDs from dictionaries

            print("Food IDs:", food_ids)

            # Insert each food item ID into the order_items table
            for food_id in food_ids:
                sql = "INSERT INTO order_items (`table_id`, `food_item_id`) VALUES (%s, %s)"
                val = (table, food_id)
                cursor.execute(sql, val)

            # Commit changes
            mydb.commit()
            print("Order successfully added to the database.")

            # Close cursor and connection
            cursor.close()

            # Optional: Clear the bill layout and reset total label after finishing the order
            self.bill_layout.clear_widgets()
            self.total_label.text = "Total: $0.00"

        except mysql.connector.Error as error:
            print("Failed to insert record into MySQL table:", error)
