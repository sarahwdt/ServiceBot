from tkinter import Toplevel


class Modal(Toplevel):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self.geometry('300x300+600+400')

    def run(self):
        self.transient(self.master)
        self.grab_set()
        self.focus_set()
        self.wait_window()
