from datetime import datetime


class ReportController:
    def __init__(self, database) -> None:
        self.database = database

    def buildMainReport(self):
        report = "Отчет по заказам\n" \
                 "==========================\n" \
                 "Количество заказов(всего/выполенено):"
        finished = 0
        for order in self.database.orders:
            if datetime.fromisoformat(order.datetime) < datetime.now():
                finished += 1

        report += str(len(self.database.orders)) + '/' + str(finished) + '\n'

        report += "==========================\n" \
                  "Количество заказов по компетенциям(всего/выполнено):\n"
        for competence in self.database.competencies:
            report += competence.name + ':'
            fin = 0
            _all = 0
            for order in self.database.orders:
                if order.competence == competence.id:
                    _all += 1
                    if datetime.fromisoformat(order.datetime) < datetime.now():
                        fin += 1
            report += str(_all) + '/' + str(fin) + '\n'

        report += "==========================\n" \
                  "Количество заказов по мастерам(всего/выполнено):\n"
        for master in self.database.masters:
            report += master.name + ':'
            fin = 0
            _all = 0
            for order in self.database.orders:
                if order.master == master.id:
                    _all += 1
                    if datetime.fromisoformat(order.datetime) < datetime.now():
                        fin += 1
            report += str(_all) + '/' + str(fin) + '\n'

        report += "==========================\n" \
                  + "Отчет актуален на " + datetime.now().strftime("%d.%m.%Y %H:%M:%S") + "\n"
        return report
