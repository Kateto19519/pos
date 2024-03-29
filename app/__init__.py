
from kivymd.app import MDApp
from kivy.utils import QueryDict, rgba
from kivy.metrics import dp, sp
from kivy.properties import ColorProperty, ListProperty
from .view import MainWindow

class MainApp(MDApp):

    theme = "light"
    color_primary = ColorProperty(rgba("#3B0BFB"))
    color_secondary = ColorProperty(rgba("#65DDB2"))
    color_tertiary = ColorProperty(rgba("#F27373"))
    color_alternate = ColorProperty(rgba("#EFF9FF"))
    color_primary_bg = ColorProperty(rgba("#FFFFFF"))
    color_secondary_bg = ColorProperty(rgba("#EFEFEF"))
    color_primary_text = ColorProperty(rgba("#000000"))
    color_secondary_text = ColorProperty(rgba("#A4A4A4"))

    fonts = QueryDict()
    fonts.size = QueryDict()
    fonts.size.extra = dp(48)
    fonts.size.h1 = dp(24)
    fonts.size.h2 = dp(22)
    fonts.size.h3 = dp(18)
    fonts.size.h4 = dp(16)
    fonts.size.h5 = dp(14)
    fonts.size.h6 = dp(12)

    fonts.heading = 'assets/fonts/Roboto/Roboto-Bold.ttf'
    fonts.subheading = 'assets/fonts/Roboto/Roboto-Medium.ttf'
    fonts.body = 'assets/fonts/Roboto/Roboto-Regular.ttf'
    fonts.styled = 'assets/fonts/Lobster/Lobster-Regular.ttf'

    def build(self):
        return MainWindow()


