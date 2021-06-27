from tkinter import Button, LabelFrame, Label, E, W, BOTH, EW, S, Entry, messagebox, Text, END, DISABLED

from db.entity.сompetence import Competence
from interface.modal import Modal
from interface.private_window import PrivateWindow


class Competencies(PrivateWindow):
    def __init__(self, database, user, prev=None, screenName=None, baseName=None, className='Tk', useTk=1, sync=0,
                 use=None):
        super().__init__(database, user, prev, screenName, baseName, className, useTk, sync, use)
        label_frame = LabelFrame(self, text="Компетенции")
        Label(master=label_frame, text="id", borderwidth=1, relief="solid").grid(row=0, column=0, sticky=W)
        Label(master=label_frame, text="Название компетенции", borderwidth=1, relief="solid").grid(row=0, column=1,
                                                                                                   sticky=E + W)
        Label(master=label_frame, text="Время", borderwidth=1, relief="solid").grid(row=0, column=2, sticky=E + W)
        Label(master=label_frame, text="Опции", borderwidth=1, relief="solid").grid(row=0, column=3, columnspan=3,
                                                                                    sticky=E + W)
        for i in range(len(self.database.competencies)):
            Label(master=label_frame, text=self.database.competencies[i].id).grid(row=i + 1, column=0, sticky=W)
            Label(master=label_frame, text=self.database.competencies[i].name).grid(row=i + 1, column=1, sticky=EW)
            Label(master=label_frame, text=self.database.competencies[i].time).grid(row=i + 1, column=2, sticky=EW)

            Button(master=label_frame, text="Открыть", command=lambda index=i: self.open(index)) \
                .grid(row=i + 1, column=3, sticky=E + W)
            Button(master=label_frame, text="Изменить", command=lambda index=i: self.upd(index)) \
                .grid(row=i + 1, column=4, sticky=E + W)
            Button(master=label_frame, text="Удалить", command=lambda index=i: self.delete(index)) \
                .grid(row=i + 1, column=5, sticky=E + W)

        Button(master=label_frame, text="Добавить", command=self.add) \
            .grid(row=len(self.database.competencies) + 2, column=0, columnspan=6, sticky=E + W + S)
        label_frame.grid_columnconfigure(1, weight=1)
        label_frame.grid_rowconfigure(len(self.database.competencies) + 2, weight=1)
        label_frame.pack(expand=1, fill=BOTH)

    def add(self):
        modal = Modal(self)
        modal.title("Новая компетенция")
        Label(modal, text='Идентификатор').pack()
        id = Entry(modal)
        id.pack(fill=BOTH)
        Label(modal, text='Название компетенции').pack()
        name = Entry(modal)
        name.pack(fill=BOTH)
        Label(modal, text='Время, затрачиваемое на услугу').pack()
        time = Entry(modal)
        time.pack(fill=BOTH)
        Label(modal, text='Варианты запросов для компетенции').pack()
        similar = Text(modal, height=4)
        similar.pack(fill=BOTH)

        Button(modal, text="Добавить", command=lambda: self._add(id.get(), name.get(), time.get(),
                                                                 similar.get(1.0, END).split('\n'))).pack()
        modal.run()

    def _add(self, id, name, time, similar):
        similar.pop(len(similar) - 1)
        competence = Competence(id, name, time, similar)
        try:
            competence.validate(self.database)
            self.database.competencies.append(competence)
            self.database.save()
            self.destroy()
            self.__init__(self.database, self.user, self.prev)
        except AttributeError as ex:
            messagebox.showerror("Ошибка", str(ex))

    def open(self, i):
        modal = Modal(self)
        modal.title("Компетенция " + self.database.competencies[i].id)
        Label(modal, text='Идентификатор:' + self.database.competencies[i].id).pack()
        Label(modal, text='Название компетенции:' + self.database.competencies[i].name).pack()
        Label(modal, text='Затрачиваемое время:' + self.database.competencies[i].time).pack()
        Label(modal, text='Варианты запросов для компетенции').pack()
        text = Text(modal)
        text.insert(END, '\n'.join(self.database.competencies[i].similar))
        text.configure(state=DISABLED)
        text.pack(expand=1, fill=BOTH)
        modal.run()

    def upd(self, i):
        modal = Modal(self)
        modal.title("Компетенция " + self.database.competencies[i].id)
        Label(modal, text='Название компетенции').pack()
        name = Entry(modal)
        name.insert(END, self.database.competencies[i].name)
        name.pack(fill=BOTH)
        Label(modal, text='Время, затрачиваемое на услугу').pack()
        time = Entry(modal)
        time.insert(END, self.database.competencies[i].time)
        time.pack(fill=BOTH)
        Label(modal, text='Варианты запросов для компетенции').pack()
        similar = Text(modal, height=4)
        similar.insert(END, '\n'.join(self.database.competencies[i].similar))
        similar.pack(fill=BOTH)
        Button(modal, text="Изменить", command=lambda: self._upd(i, name.get(), time.get(),
                                                                 similar.get(1.0, END).split('\n'))).pack()
        modal.run()

    def _upd(self, i, name, time, similar):
        similar.pop(len(similar) - 1)
        competence_temp = Competence(self.database.competencies[i].id, self.database.competencies[i].name,
                                     self.database.competencies[i].time, self.database.competencies[i].similar)
        self.database.competencies.pop(i)
        competence = Competence(competence_temp.id, name, time, similar)
        try:
            competence.validate(self.database)
            self.database.competencies.append(competence)
            self.database.save()
            self.destroy()
            self.__init__(self.database, self.user, self.prev)
        except AttributeError as ex:
            self.database.competencies.append(competence_temp)
            messagebox.showerror("Ошибка", str(ex))

    def delete(self, i):
        self.database.competencies.pop(i)
        self.destroy()
        self.database.save()
        self.__init__(self.database, self.user, self.prev)
