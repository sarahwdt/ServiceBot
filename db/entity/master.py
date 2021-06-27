class Master:

    def __init__(self, id, name, competencies):
        self.id = id
        self.name = name
        self.competencies = competencies

    @staticmethod
    def parse(string):
        string = string.replace('\n', '')
        attr = string.split(';')
        return Master(attr[1] if len(attr) > 1 else '',
                      attr[2] if len(attr) > 2 else '',
                      set(attr[3].split(',')) if len(attr) > 3 else '')

    def save(self):
        if isinstance(self.competencies, list) or isinstance(self.competencies, set):
            return "master;" + self.id + ";" + self.name + ";" + ",".join(self.competencies)
        else:
            return "master;" + self.id + ";" + self.name + ";" + str(self.competencies)

    def validate(self, db):
        self.check_id_not_null()
        self.check_name_not_null()
        self.check_competencies_not_null()
        self.check_id_format()
        self.check_competence_format()
        self.check_id_unique(db)
        self.check_competence_exist(db)

    def check_id_not_null(self):
        if len(self.id) == 0:
            raise AttributeError('Id не может быть пустым')

    def check_name_not_null(self):
        if len(self.name) == 0:
            raise AttributeError('Имя не может быть пустым')

    def check_competencies_not_null(self):
        if len(self.competencies) == 0:
            raise AttributeError('Компетенции не может быть пустыми')

    def check_id_format(self):
        try:
            int(self.id)
        except Exception:
            raise AttributeError('Id может быть целым числом ' + self.id)

    def check_competence_format(self):
        for competence in self.competencies:
            try:
                int(competence)
            except Exception:
                raise AttributeError('Ошибка в формате id компетенции:' + competence)

    def check_id_unique(self, db):
        for master in db.masters:
            if self != master and self.id == master.id:
                raise AttributeError('Мастер с id ' + self.id + ' уже существует')

    def check_competence_exist(self, db):
        for com_id in self.competencies:
            exist = False
            for competence in db.competencies:
                if com_id == competence.id:
                    exist = True
            if not exist:
                raise AttributeError('Не найдено компетенции с id ' + com_id)
