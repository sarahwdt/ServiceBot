from tkinter import Button, LabelFrame, Label, E, W, BOTH, EW, S, Entry, messagebox, END

from db.entity.admin import Admin
from interface.modal import Modal
from interface.private_window import PrivateWindow


class Admins(PrivateWindow):
    def __init__(self, database, user, prev=None, screenName=None, baseName=None, className='Tk', useTk=1, sync=0,
                 use=None):
        super().__init__(database, user, prev, screenName, baseName, className, useTk, sync, use)
        label_frame = LabelFrame(self, text="Администраторы")
        Label(master=label_frame, text="id", borderwidth=1, relief="solid").grid(row=0, column=0, sticky=W)
        Label(master=label_frame, text="Логин", borderwidth=1, relief="solid").grid(row=0, column=1, sticky=E + W)
        Label(master=label_frame, text="Опции", borderwidth=1, relief="solid").grid(row=0, column=2, columnspan=3,
                                                                                    sticky=E + W)
        for i in range(len(self.database.admins)):
            Label(master=label_frame, text=self.database.admins[i].id).grid(row=i + 1, column=0, sticky=W)
            Label(master=label_frame, text=self.database.admins[i].login).grid(row=i + 1, column=1, sticky=EW)
            Button(master=label_frame, text="Открыть", command=lambda index=i: self.open(index)) \
                .grid(row=i + 1, column=2, sticky=E + W)
            Button(master=label_frame, text="Изменить", command=lambda index=i: self.upd(index)) \
                .grid(row=i + 1, column=3, sticky=E + W)
            if self.user.id != self.database.admins[i].id:
                Button(master=label_frame, text="Удалить", command=lambda index=i: self.delete(index)) \
                    .grid(row=i + 1, column=4, sticky=E + W)

        Button(master=label_frame, text="Добавить", command=self.add) \
            .grid(row=len(self.database.admins) + 2, column=0, columnspan=5, sticky=E + W + S)
        label_frame.grid_columnconfigure(1, weight=1)
        label_frame.grid_rowconfigure(len(self.database.admins) + 2, weight=1)
        label_frame.pack(expand=1, fill=BOTH)

    def add(self):
        modal = Modal(self)
        modal.title("Новый администратор")
        Label(modal, text='Идентификатор').pack()
        id = Entry(modal)
        id.pack(fill=BOTH)
        Label(modal, text='Логин').pack()
        login = Entry(modal)
        login.pack(fill=BOTH)

        Button(modal, text="Добавить", command=lambda: self._add(id.get(), login.get())).pack()
        modal.run()

    def _add(self, id, login):
        admin = Admin(id, login)
        try:
            admin.validate(self.database)
            self.database.admins.append(admin)
            self.database.save()
            self.destroy()
            self.__init__(self.database, self.user, self.prev)
        except AttributeError as ex:
            messagebox.showerror("Ошибка", str(ex))

    def open(self, i):
        modal = Modal(self)
        modal.title("Администратор " + self.database.admins[i].id)
        Label(modal, text='Идентификатор:' + self.database.admins[i].id).pack()
        Label(modal, text='Логин:' + self.database.admins[i].login).pack()
        modal.run()

    def upd(self, i):
        modal = Modal(self)
        modal.title("Администратор " + self.database.admins[i].id)
        Label(modal, text='Идентификатор:' + self.database.admins[i].id).pack()
        Label(modal, text='Логин').pack()
        login = Entry(modal)
        login.insert(END, self.database.admins[i].login)
        login.pack(fill=BOTH)
        Button(modal, text="Изменить", command=lambda: self._upd(i, login.get())).pack()
        modal.run()

    def _upd(self, i, login):
        admin_temp = Admin(self.database.admins[i].id, self.database.admins[i].login)
        self.database.admins.pop(i)
        admin = Admin(admin_temp.id, login)
        try:
            admin.validate(self.database)
            self.database.admins.append(admin)
            self.database.save()
            self.destroy()
            self.__init__(self.database, self.user, self.prev)
        except AttributeError as ex:
            self.database.admins.append(admin_temp)
            messagebox.showerror("Ошибка", str(ex))

    def delete(self, i):
        self.database.admins.pop(i)
        self.destroy()
        self.database.save()
        self.__init__(self.database, self.user, self.prev)
