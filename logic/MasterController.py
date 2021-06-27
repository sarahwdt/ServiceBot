from datetime import datetime, timedelta


class MasterController:
    def __init__(self, database):
        super().__init__()
        self.database = database

    def findAllowedMasters(self, dt: datetime, competence_id):
        allowed_masters = list()
        for master in self.database.masters:
            if str(competence_id) in master.competencies:
                allowed_masters.append(master)

        time_spend = 0
        for competence in self.database.competencies:
            if competence.id == competence_id:
                time_spend = competence.time
        # time_spend += 1 #время на дорогу

        for order in self.database.orders:
            order_dt = datetime.fromisoformat(order.datetime)
            for master in allowed_masters:
                if master.id == order.master and \
                        (order_dt + timedelta(0, 0, 0, 0, 0, int(time_spend), 0))\
                        > dt\
                        > (order_dt - timedelta(0, 0, 0, 0, 0, int(time_spend), 0)):
                    allowed_masters.remove(master)

        return allowed_masters
