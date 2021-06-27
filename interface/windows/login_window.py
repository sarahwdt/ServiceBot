from tkinter import Label, Entry, Button, messagebox, BOTH

from interface.window import Window
from interface.windows.menu_window import Menu


class Login(Window):
    def __init__(self, database, prev=None, screenName=None, baseName=None, className='Tk', useTk=1, sync=0, use=None):
        super().__init__(database, prev, screenName, baseName, className, useTk, sync, use)
        self.loginLabel = Label(master=self, text='Логин').pack()
        self.loginEntry = Entry(master=self)
        self.loginEntry.pack(fill=BOTH)
        self.loginButton = Button(master=self, text='Войти', command=self.login).pack()

    def login(self):
        result = False
        for admin in self.database.admins:
            if admin.login == self.loginEntry.get():
                result = True
                self.next(Menu(user=admin, database=self.database, prev=self), "Меню")
        if not result:
            messagebox.showinfo(title="Администратор не найден",
                                message="Пользователь c логином \"" + self.loginEntry.get() + "\" не найден")
