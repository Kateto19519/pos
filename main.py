import atexit

from app import MainApp
from db_connector import mydb


def clear_csv_file():
    open('user_info.csv', 'w').close()

try:
    MainApp().run()

finally:
    atexit.register(clear_csv_file)
    mydb.close()
