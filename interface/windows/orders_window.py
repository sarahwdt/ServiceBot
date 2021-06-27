from datetime import datetime
from tkinter import Button, LabelFrame, Label, E, W, BOTH, EW, messagebox, END, Listbox

from db.entity.order import Order
from interface.modal import Modal
from interface.private_window import PrivateWindow
from logic.MasterController import MasterController


class Orders(PrivateWindow):
    def __init__(self, database, user, prev=None, screenName=None, baseName=None, className='Tk', useTk=1, sync=0,
                 use=None):
        super().__init__(database, user, prev, screenName, baseName, className, useTk, sync, use)
        self.master_controller = MasterController(database)
        label_frame = LabelFrame(self, text="Заказы")
        Label(master=label_frame, text="id", borderwidth=1, relief="solid").grid(row=0, column=0, sticky=W)
        Label(master=label_frame, text="Компетенция", borderwidth=1, relief="solid").grid(row=0, column=1,
                                                                                            sticky=E + W)
        Label(master=label_frame, text="Время запроса", borderwidth=1, relief="solid").grid(row=0, column=2,
                                                                                            sticky=E + W)
        Label(master=label_frame, text="Опции", borderwidth=1, relief="solid").grid(row=0, column=3, columnspan=3,
                                                                                    sticky=E + W)
        for i in range(len(self.database.orders)):
            Label(master=label_frame, text=self.database.orders[i].id).grid(row=i + 1, column=0, sticky=W)
            for competence in self.database.competencies:
                if competence.id == self.database.orders[i].competence:
                    Label(master=label_frame, text=competence.name).grid(row=i + 1, column=1, sticky=EW)
            Label(master=label_frame, text=self.database.orders[i].datetime).grid(row=i + 1, column=2, sticky=EW)

            Button(master=label_frame, text="Открыть", command=lambda index=i: self.open(index)) \
                .grid(row=i + 1, column=3, sticky=E + W)
            Button(master=label_frame, text="Изменить", command=lambda index=i: self.upd(index)) \
                .grid(row=i + 1, column=4, sticky=E + W)
            Button(master=label_frame, text="Удалить", command=lambda index=i: self.delete(index)) \
                .grid(row=i + 1, column=5, sticky=E + W)

        label_frame.grid_columnconfigure(1, weight=1)
        label_frame.pack(expand=1, fill=BOTH)

    # def add(self):
    #     modal = Modal(self)
    #     modal.title("Новый мастер")
    #     Label(modal, text='Идентификатор').pack()
    #     id = Entry(modal)
    #     id.pack()
    #     Label(modal, text='Имя мастера').pack()
    #     name = Entry(modal)
    #     name.pack()
    #     Label(modal, text='Компетенции').pack()
    #     competencies = Listbox(modal, selectmode="multiple")
    #     for item in self.database.competencies:
    #         competencies.insert(END, item.name)
    #     competencies.pack()
    #
    #     Button(modal, text="Добавить", command=lambda: self._add(id.get(), name.get(),
    #                                                              list(map(lambda x: self.database.competencies[x].id,
    #                                                                       competencies.curselection())))).pack()
    #     modal.run()
    #
    # def _add(self, id, name, competencies):
    #     master = Master(id, name, competencies)
    #     try:
    #         master.validate(self.database)
    #         self.database.masters.append(master)
    #         self.database.save()
    #         self.destroy()
    #         self.__init__(self.database, self.user, self.prev)
    #     except AttributeError as ex:
    #         messagebox.showerror("Ошибка", str(ex))

    def open(self, i):
        modal = Modal(self)
        modal.title("Заказ " + self.database.orders[i].id)
        Label(modal, text='Идентификатор:' + self.database.orders[i].id).pack()
        Label(modal, text='Текст запроса:' + self.database.orders[i].text).pack()
        Label(modal, text='Время начала заказа:' + self.database.orders[i].datetime).pack()
        for master in self.database.masters:
            if master.id == self.database.orders[i].master:
                Label(modal, text='Имя мастера:' + self.database.masters[i].name).pack()
        for competence in self.database.competencies:
            if competence.id == self.database.orders[i].competence:
                Label(modal, text='Название компетенции:' + competence.name).pack()

        Label(modal, text='Имя заказчика:' + self.database.orders[i].name).pack()
        Label(modal, text='Телефон заказчика:' + self.database.orders[i].phone).pack()
        Label(modal, text='Адрес заказчика:' + self.database.orders[i].address).pack()

        modal.run()

    def upd(self, i):
        modal = Modal(self)
        modal.geometry('300x500+600+400')

        modal.title("Заказ " + self.database.orders[i].id)

        Label(modal, text='Идентификатор:' + self.database.orders[i].id).pack()
        Label(modal, text='Текст запроса:' + self.database.orders[i].text).pack()
        Label(modal, text='Время начала заказа:' + self.database.orders[i].datetime).pack()
        for competence in self.database.competencies:
            if competence.id == self.database.orders[i].competence:
                Label(modal, text='Название компетенции:' + competence.name).pack()

        for master in self.database.masters:
            if master.id == self.database.orders[i].master:
                Label(modal, text='Имя мастера:' + master.name).pack()

        Label(modal, text='Имя заказчика:' + self.database.orders[i].name).pack()
        Label(modal, text='Телефон заказчика:' + self.database.orders[i].phone).pack()
        Label(modal, text='Адрес заказчика:' + self.database.orders[i].address).pack()
        Label(modal, text='Свободные мастера:').pack()

        masters = Listbox(modal)
        allowed_masters = self.master_controller.findAllowedMasters(
            datetime.fromisoformat(self.database.orders[i].datetime),
            self.database.orders[i].competence)
        for index in range(len(allowed_masters)):
            masters.insert(END, allowed_masters[index].name)
            if allowed_masters[index].id == self.database.orders[i].master:
                masters.select_set(index)

        masters.pack(fill=BOTH)

        Button(modal, text="Изменить", command=lambda i=i, masters=masters:
        self._upd(i, masters, allowed_masters)).pack()
        modal.run()

    def _upd(self, i, masters, allowed_masters):
        master_id = allowed_masters[masters.curselection()[0]].id
        order = Order(self.database.orders[i].id,
                      self.database.orders[i].text,
                      self.database.orders[i].datetime,
                      master_id,
                      self.database.orders[i].competence,
                      self.database.orders[i].name,
                      self.database.orders[i].phone,
                      self.database.orders[i].address)
        order_temp = self.database.orders.pop(i)
        try:
            order.validate(self.database)
            self.database.orders.append(order)
            self.database.save()
            self.destroy()
            self.__init__(self.database, self.user, self.prev)
        except AttributeError as ex:
            self.database.orders.append(order_temp)
            messagebox.showerror("Ошибка", str(ex))

    def delete(self, i):
        self.database.orders.pop(i)
        self.destroy()
        self.database.save()
        self.__init__(self.database, self.user, self.prev)
