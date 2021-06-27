from datetime import datetime


class Order:

    def __init__(self, id, text, datetime, master, competence, name, phone, address):
        self.id = id
        self.text = text
        self.datetime = datetime
        self.master = master
        self.competence = competence
        self.name = name
        self.phone = phone
        self.address = address

    @staticmethod
    def parse(string):
        string = string.replace('\n', '')
        attr = string.split(';')
        return Order(attr[1] if len(attr) > 1 else '',
                     attr[2] if len(attr) > 2 else '',
                     attr[3] if len(attr) > 3 else '',
                     attr[4] if len(attr) > 4 else '',
                     attr[5] if len(attr) > 5 else '',
                     attr[6] if len(attr) > 6 else '',
                     attr[7] if len(attr) > 7 else '',
                     attr[8] if len(attr) > 8 else '')

    def save(self):
        return "order;" + str(self.id) + ";" + self.text + ";" + self.datetime + ";" + str(self.master) + ";" \
               + str(self.competence) + ";" + self.name + ";" + self.phone + ";" + self.address

    def validate(self, db):
        self.check_id_unique(db)
        self.check_id_not_null()
        self.check_text_not_null()
        self.check_datetime_not_null()
        self.check_master_not_null()
        self.check_competence_not_null()
        self.check_name_not_null()
        self.check_phone_not_null()
        self.check_address_not_null()
        self.check_id_format()
        self.check_master_format()
        self.check_competence_format()
        self.check_datetime_format()
        self.check_master_exist(db)
        self.check_competence_exist(db)

    def check_id_unique(self, db):
        for order in db.orders:
            if self != order and self.id == order.id:
                raise AttributeError('Заказ с id ' + self.id + ' уже существует')

    def check_id_not_null(self):
        if len(str(self.id)) == 0:
            raise AttributeError('Id не может быть пустым')

    def check_text_not_null(self):
        if len(self.text) == 0:
            raise AttributeError('Текст заказа не может быть пустым')

    def check_datetime_not_null(self):
        if len(self.datetime) == 0:
            raise AttributeError('Время создания не может быть пустым')

    def check_master_not_null(self):
        if len(self.master) == 0:
            raise AttributeError('Id мастера не может быть пустым')

    def check_competence_not_null(self):
        if len(self.competence) == 0:
            raise AttributeError('Id компетенции не может быть пустым')

    def check_name_not_null(self):
        if len(self.name) == 0:
            raise AttributeError('Имя не может быть пустым')

    def check_phone_not_null(self):
        if len(self.phone) == 0:
            raise AttributeError('Телефон не может быть пустым')

    def check_address_not_null(self):
        if len(self.address) == 0:
            raise AttributeError('Адрес не может быть пустым')

    def check_id_format(self):
        try:
            int(self.id)
        except Exception:
            raise AttributeError('Id может быть целым числом ' + self.id)

    def check_master_format(self):
        try:
            int(self.master)
        except Exception:
            raise AttributeError('Id мастера может быть целым числом ' + self.master)

    def check_competence_format(self):
        try:
            int(self.competence)
        except Exception:
            raise AttributeError('Id компетенции может быть целым числом ' + self.competence)

    def check_datetime_format(self):
        try:
            datetime.fromisoformat(self.datetime)
        except Exception:
            raise AttributeError('Ошибка формата даты и времени ' + self.datetime)

    def check_master_exist(self, db):
        exist = False
        for master in db.masters:
            if self.master == master.id:
                exist = True
        if not exist:
            raise AttributeError('Не найден мастер с id ' + self.master)

    def check_competence_exist(self, db):
        exist = False
        for competence in db.competencies:
            if self.competence == competence.id:
                exist = True
        if not exist:
            raise AttributeError('Не найдена компетенция с id ' + self.master)
