class Competence:

    def __init__(self, id, name, time, similar):
        self.id = id
        self.name = name
        self.time = time
        self.similar = similar

    @staticmethod
    def parse(string):
        string = string.replace('\n', '')
        attr = string.split(';')
        return Competence(attr[1] if len(attr) > 1 else '',
                          attr[2] if len(attr) > 2 else '',
                          attr[3] if len(attr) > 3 else '',
                          set(attr[4].split(',')) if len(attr) > 4 else '')

    def save(self):
        if isinstance(self.similar, set) or isinstance(self.similar, list):
            return "competence;" + self.id + ";" + self.name + ";" + self.time + ";" + ",".join(self.similar)
        else:
            return "competence;" + self.id + ";" + self.name + ";" + self.time + ";" + str(self.similar)

    def validate(self, db):
        self.check_id_not_null()
        self.check_name_not_null()
        self.check_time_not_null()
        self.check_similar_not_null()
        self.check_id_format()
        self.check_time_format()
        self.check_id_unique(db)
        self.check_similar_unique(db)

    def check_id_not_null(self):
        if len(self.id) == 0:
            raise AttributeError('Id не может быть пустым')

    def check_name_not_null(self):
        if len(self.name) == 0:
            raise AttributeError('Имя не может быть пустым')

    def check_time_not_null(self):
        if len(self.time) == 0:
            raise AttributeError('Время не может быть пустым')

    def check_similar_not_null(self):
        if len(self.similar) == 0:
            raise AttributeError('Должны присутствовать варианты запроса для копетенции')
        for sim in self.similar:
            if len(sim) < 3:
                raise AttributeError('Длинна варианта запроса не может быть меньше 3 символов')

    def check_id_format(self):
        try:
            int(self.id)
        except Exception:
            raise AttributeError('Id может быть целым числом ' + self.id)

    def check_time_format(self):
        try:
            int(self.time)
        except Exception:
            raise AttributeError('Ошибочный формат времени ' + self.time + '. Время указыватся в количестве часов.')

    def check_id_unique(self, db):
        for competence in db.competencies:
            if self != competence and self.id == competence.id:
                raise AttributeError('Компетенция с id ' + self.id + ' уже существует')

    def check_similar_unique(self, db):
        for competence in db.competencies:
            if self != competence:
                for sim in competence.similar:
                    if sim in self.similar:
                        raise AttributeError('Компетенция содержит паттерн, который уже существует базе данных: ' + sim)
