from datetime import datetime
from tkinter import Label, Entry, BOTH, Listbox, END, StringVar, Button, Scale, messagebox

from tkcalendar import DateEntry

from db.entity.order import Order
from interface.window import Window
from logic.MasterController import MasterController


class ClientOrderWindow(Window):
    def __init__(self, database, prev=None, screenName=None, baseName=None, className='Tk', useTk=1, sync=0, use=None):
        super().__init__(database, prev, screenName, baseName, className, useTk, sync, use)
        self.geometry('500x600+600+400')
        self.master_controller = MasterController(database)

        Label(self, text='Запрос').pack()
        competencies = Listbox(self, height=0)
        self.sims = list()
        for competence in self.database.competencies:
            for similar in competence.similar:
                self.sims.append(similar)
        sv = StringVar()
        sv.trace("w", lambda name_, index, mode, listbox=competencies, sv=sv: self.upd(competencies, sv))

        text = Entry(self, textvariable=sv)
        text.pack(fill=BOTH)
        competencies.pack(fill=BOTH)

        Label(self, text='Ваше имя').pack()
        name = Entry(self)
        name.pack(fill=BOTH)
        Label(self, text='Ваш телефон').pack()
        phone = Entry(self)
        phone.pack(fill=BOTH)
        Label(self, text='Ваш адрес').pack()
        address = Entry(self)
        address.pack(fill=BOTH)
        Label(self, text='Когда должен прибыть мастер?').pack()
        date = DateEntry(self)
        date.pack()
        time = Scale(self, from_=0, to=24, orient='horizontal')
        time.pack()
        Button(self, text="Совершить заказ", command=lambda: self.add(text.get(), date.get_date(), time.get(),
                                                                      competencies,
                                                                      name.get(), phone.get(), address.get())) \
            .pack(fill=BOTH)

    def upd(self, competencies, sv):
        competencies.delete(0, END)
        for sim in self.sims:
            if sv.get() in sim:
                competencies.insert(END, sim)

    def add(self, text, date, time, similar, name, phone, address):
        if len(similar.curselection()) == 0:
            messagebox.showerror("Ошибка", "Выбирете услугу")
            return
        similar = similar.get(similar.curselection())
        dt = datetime(date.year, date.month, date.day, time, 0, 0, 0)
        for competence_ in self.database.competencies:
            for sim in competence_.similar:
                if sim == similar:
                    competence = competence_
        allowed_masters = self.master_controller.findAllowedMasters(dt, competence.id)
        if len(allowed_masters) == 0:
            messagebox.showerror("Ошибка", "Нет свободных мастеров")
            return
        id = 1
        orders_id = list(map(lambda x: int(x.id), self.database.orders))
        while id in orders_id:
            id += 1

        order = Order(id, text, str(dt.isoformat()), allowed_masters[0].id, competence.id, name, phone, address)
        try:
            order.validate(self.database)
            self.database.orders.append(order)
            self.database.save()
            self.destroy()
            self.__init__(self.database, self.prev)
        except AttributeError as ex:
            messagebox.showerror("Ошибка", str(ex))
