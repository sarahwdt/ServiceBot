from db.core.db import DB
from interface.windows.client_window import ClientOrderWindow

database = DB("C:/Users/nastya/Desktop/db.txt")

if __name__ == '__main__':
    ClientOrderWindow(database).mainloop()
