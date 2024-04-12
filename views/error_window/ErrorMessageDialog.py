from kivy.app import App
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.clock import mainthread

Builder.load_string('''
<ErrorMessageDialog>:
    orientation: "vertical"
    padding: "10dp"

    MDLabel:
        id: title_label
        font_style: "Subtitle1"
        theme_text_color: "Primary"
        size_hint_y: None
        height: self.texture_size[1] + dp(10)

    MDLabel:
        id: text_label
        font_style: "Body1"
        theme_text_color: "Secondary"
        size_hint_y: None
        height: self.texture_size[1]

    Widget:
        size_hint_y: None
        height: "10dp"
''')


class ErrorMessageDialog(BoxLayout):
    @mainthread
    def show_dialog(self, title, text):
        self.ids.title_label.text = title
        self.ids.text_label.text = text
        dialog = MDDialog(
            title="",
            type="custom",
            content_cls=self,
            buttons=[
                MDFlatButton(
                    text="CLOSE",
                    on_release=lambda *args: dialog.dismiss()
                )
            ]
        )
        dialog.open()