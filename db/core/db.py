from db.entity.admin import Admin
from db.entity.master import Master
from db.entity.order import Order
from db.entity.сompetence import Competence


class DB:
    def __init__(self, txt):
        self.txt = txt
        self.masters = []
        self.admins = []
        self.orders = []
        self.competencies = []
        self.load()

    def load(self):
        db_file = open(self.txt, "rt")
        lines = db_file.readlines()
        lines.sort()
        for line in lines:
            name = line.split(';')[0]
            if name == 'master':
                m = Master.parse(line)
                try:
                    m.validate(self)
                    self.masters.append(Master.parse(line))
                except AttributeError as ex:
                    print(str(ex))
            if name == 'admin':
                a = Admin.parse(line)
                try:
                    a.validate(self)
                    self.admins.append(a)
                except AttributeError as ex:
                    print(str(ex))
            if name == 'order':
                o = Order.parse(line)
                try:
                    o.validate(self)
                    self.orders.append(o)
                except AttributeError as ex:
                    print(str(ex))
            if name == 'competence':
                c = Competence.parse(line)
                try:
                    c.validate(self)
                    self.competencies.append(c)
                except AttributeError as ex:
                    print(str(ex))
        db_file.close()

    def save(self):
        db_file = open(self.txt, "wt")
        for item in self.admins:
            db_file.write(item.save())
            db_file.write("\n")
        for item in self.competencies:
            db_file.write(item.save())
            db_file.write("\n")
        for item in self.masters:
            db_file.write(item.save())
            db_file.write("\n")
        for item in self.orders:
            db_file.write(item.save())
            db_file.write("\n")
        db_file.close()
