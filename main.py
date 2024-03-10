from app import MainApp
from db_connector import mydb


MainApp().run()
mydb.close()
