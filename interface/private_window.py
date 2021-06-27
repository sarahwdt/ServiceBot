from interface.window import Window


class PrivateWindow(Window):
    def __init__(self, database, user, prev=None, screenName=None, baseName=None, className='Tk', useTk=1, sync=0,
                 use=None):
        super().__init__(database, prev, screenName, baseName, className, useTk, sync, use)
        self.user = user
