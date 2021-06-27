from db.core.db import DB
from interface.windows.login_window import Login

database = DB("C:/Users/nastya/Desktop/db.txt")

if __name__ == '__main__':
    Login(database).mainloop()
