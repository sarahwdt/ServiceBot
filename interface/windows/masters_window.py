from tkinter import Button, LabelFrame, Label, E, W, BOTH, EW, S, Entry, messagebox, END, Listbox

from db.entity.master import Master
from interface.modal import Modal
from interface.private_window import PrivateWindow


class Masters(PrivateWindow):
    def __init__(self, database, user, prev=None, screenName=None, baseName=None, className='Tk', useTk=1, sync=0,
                 use=None):
        super().__init__(database, user, prev, screenName, baseName, className, useTk, sync, use)
        label_frame = LabelFrame(self, text="Мастера")
        Label(master=label_frame, text="id", borderwidth=1, relief="solid").grid(row=0, column=0, sticky=W)
        Label(master=label_frame, text="Имя мастера", borderwidth=1, relief="solid").grid(row=0, column=1,
                                                                                          sticky=E + W)
        Label(master=label_frame, text="Опции", borderwidth=1, relief="solid").grid(row=0, column=2, columnspan=3,
                                                                                    sticky=E + W)
        for i in range(len(self.database.masters)):
            Label(master=label_frame, text=self.database.masters[i].id).grid(row=i + 1, column=0, sticky=W)
            Label(master=label_frame, text=self.database.masters[i].name).grid(row=i + 1, column=1, sticky=EW)

            Button(master=label_frame, text="Открыть", command=lambda index=i: self.open(index)) \
                .grid(row=i + 1, column=2, sticky=E + W)
            Button(master=label_frame, text="Изменить", command=lambda index=i: self.upd(index)) \
                .grid(row=i + 1, column=3, sticky=E + W)
            Button(master=label_frame, text="Удалить", command=lambda index=i: self.delete(index)) \
                .grid(row=i + 1, column=4, sticky=E + W)

        Button(master=label_frame, text="Добавить", command=self.add) \
            .grid(row=len(self.database.masters) + 2, column=0, columnspan=5, sticky=E + W + S)
        label_frame.grid_columnconfigure(1, weight=1)
        label_frame.grid_rowconfigure(len(self.database.masters) + 2, weight=1)
        label_frame.pack(expand=1, fill=BOTH)

    def add(self):
        modal = Modal(self)
        modal.title("Новый мастер")
        Label(modal, text='Идентификатор').pack()
        id = Entry(modal)
        id.pack(fill=BOTH)
        Label(modal, text='Имя мастера').pack()
        name = Entry(modal)
        name.pack(fill=BOTH)
        Label(modal, text='Компетенции').pack()
        competencies = Listbox(modal, selectmode="multiple")
        for item in self.database.competencies:
            competencies.insert(END, item.name)
        competencies.pack(fill=BOTH)

        Button(modal, text="Добавить", command=lambda: self._add(id.get(), name.get(),
                                                                 list(map(lambda x: self.database.competencies[x].id,
                                                                          competencies.curselection())))).pack()
        modal.run()

    def _add(self, id, name, competencies):
        master = Master(id, name, competencies)
        try:
            master.validate(self.database)
            self.database.masters.append(master)
            self.database.save()
            self.destroy()
            self.__init__(self.database, self.user, self.prev)
        except AttributeError as ex:
            messagebox.showerror("Ошибка", str(ex))

    def open(self, i):
        modal = Modal(self)
        modal.title("Мастер " + self.database.competencies[i].id)
        Label(modal, text='Идентификатор:' + self.database.masters[i].id).pack()
        Label(modal, text='Имя мастера:' + self.database.masters[i].name).pack()
        label_frame = LabelFrame(modal, text="Компетенции")
        for item in self.database.competencies:
            if item.id in self.database.masters[i].competencies:
                Label(label_frame, text=item.name).pack()
        label_frame.pack(fill=BOTH)
        modal.run()

    def upd(self, i):
        modal = Modal(self)
        modal.title("Мастер " + self.database.masters[i].id)
        Label(modal, text='Имя мастера').pack()
        name = Entry(modal)
        name.insert(END, self.database.masters[i].name)
        name.pack(fill=BOTH)
        Label(modal, text='Компетенции').pack()
        competencies = Listbox(modal, selectmode="multiple")
        for item in self.database.competencies:
            competencies.insert(END, item.name)
        for index in range(len(self.database.competencies)):
            if str(self.database.competencies[index].id) in self.database.masters[i].competencies:
                competencies.select_set(index)
        competencies.pack(fill=BOTH)
        Button(modal, text="Изменить", command=lambda: self._upd(i, name.get(),
                                                                 list(map(lambda x: self.database.competencies[x].id,
                                                                          competencies.curselection())))).pack()
        modal.run()

    def _upd(self, i, name, competencies):
        master_temp = Master(self.database.masters[i].id, self.database.masters[i].name,
                             self.database.masters[i].competencies)
        self.database.masters.pop(i)
        master = Master(master_temp.id, name, competencies)
        try:
            master.validate(self.database)
            self.database.masters.append(master)
            self.database.save()
            self.destroy()
            self.__init__(self.database, self.user, self.prev)
        except AttributeError as ex:
            self.database.masters.append(master_temp)
            messagebox.showerror("Ошибка", str(ex))

    def delete(self, i):
        self.database.masters.pop(i)
        self.destroy()
        self.database.save()
        self.__init__(self.database, self.user, self.prev)
