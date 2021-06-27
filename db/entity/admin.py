class Admin:

    def __init__(self, id, login):
        self.id = id
        self.login = login

    @staticmethod
    def parse(string):
        string = string.replace('\n', '')
        attr = string.split(';')
        return Admin(attr[1] if len(attr) > 1 else '',
                     attr[2] if len(attr) > 2 else '')

    def save(self):
        return "admin;" + self.id + ";" + self.login

    def validate(self, db):
        self.check_id_not_null()
        self.check_login_not_null()
        self.check_id_format()
        self.check_id_unique(db)
        self.check_login_unique(db)

    def check_id_not_null(self):
        if len(self.id) == 0:
            raise AttributeError('Id не может быть пустым')

    def check_login_not_null(self):
        if len(self.login) == 0:
            raise AttributeError('Логин не может быть пустым')

    def check_id_format(self):
        try:
            int(self.id)
        except Exception:
            raise AttributeError('Id может быть целым числом ' + self.id)

    def check_id_unique(self, db):
        for admin in db.admins:
            if self != admin and self.id == admin.id:
                raise AttributeError('Администратор с id ' + self.id + ' уже существует')

    def check_login_unique(self, db):
        for admin in db.admins:
            if self != admin and self.login == admin.login:
                raise AttributeError('Администратор с логином ' + self.login + ' уже существует')
