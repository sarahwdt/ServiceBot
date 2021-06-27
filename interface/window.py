from tkinter import Tk


class Window(Tk):
    def __init__(self, database, prev=None, screenName=None, baseName=None, className='Tk', useTk=1, sync=0, use=None):
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.database = database
        self.prev = prev
        self.geometry('500x300+600+400')
        self.title("Сервис центр")
        self.protocol("WM_DELETE_WINDOW", self.back)

    def back(self):
        if self.prev is not None:
            self.prev.deiconify()
        self.destroy()

    def next(self, next_window, title_append):
        next_window.title(title_append + "." + next_window.title())
        self.withdraw()
        next_window.mainloop()
