from tkinter import Button, filedialog

from interface.private_window import PrivateWindow
from interface.windows.admins_window import Admins
from interface.windows.competenties_window import Competencies
from interface.windows.masters_window import Masters
from interface.windows.orders_window import Orders
from logic.ReportController import ReportController


class Menu(PrivateWindow):
    def __init__(self, database, user, prev=None, screenName=None, baseName=None, className='Tk', useTk=1, sync=0,
                 use=None):
        super().__init__(database, user, prev, screenName, baseName, className, useTk, sync, use)
        Button(master=self, text='Заказы',
               command=lambda: self.next(Orders(self.database, self.user, self), "Заказы")).pack()
        Button(master=self, text='Мастера',
               command=lambda: self.next(Masters(self.database, self.user, self), "Мастера")).pack()
        Button(master=self, text='Компетенции',
               command=lambda: self.next(Competencies(self.database, self.user, self), "Компетенции")).pack()
        Button(master=self, text='Администраторы',
               command=lambda: self.next(Admins(self.database, self.user, self), "Администраторы")).pack()
        Button(master=self, text='Отчет', command=self.write_report).pack()
        self.report_controller = ReportController(self.database)

    def write_report(self):
        self.withdraw()
        dlg = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[("Простой txt файл", '*.txt')], )
        if dlg != '':
            f = open(dlg, "w")
            f.write(self.report_controller.buildMainReport())
            f.close()
        self.deiconify()
