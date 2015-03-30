"""
Super simple representation of a raw material (or part)
of the thing we are producing.
"""
import arrow


class RawMaterial(object):

    @staticmethod
    def create(name, lead_time, stock, needed):
        r = RawMaterial()
        r.set(name, lead_time, stock, needed)
        return r

    def __init__(self):
        self.available_by = None
        self.name = None
        self.lead_time = None
        self.stock = None
        self.needed = None
        self.orders = {}

    def set(self, name, lead_time, stock, needed):
        self.name = name
        self.lead_time = lead_time
        self.stock = stock
        self.needed = needed

    def add_order(self, amount, due):
        due_date = arrow.get(due, 'YYYY-MM-DD')
        self.orders[due_date] = amount

    def create_timeline(self):
        self.available_by = {}
        self.available_by[arrow.now()] = self.stock
        total = self.stock
        for date, amount in self.orders.iteritems():
            total += amount
            self.available_by[date] = total

        return max(self.available_by.keys())

    def __repr__(self):
        return "Name: {}, Orders: {}".format(self.name, self.orders)
