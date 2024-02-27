
from os.path import dirname, join

from kivy.core.window import Window

from app import MainApp
from db_connector import mydb


MainApp().run()
mydb.close()
