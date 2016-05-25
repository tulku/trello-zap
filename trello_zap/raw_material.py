"""
Super simple representation of a raw material (or part)
of the thing we are producing.
"""
import arrow
from .config import Configuration


class RawMaterial(object):

    def __init__(self):
        self.backend_object = None
        self.available_by = None
        self.name = None
        self.lead_time = None
        self.needed = None
        self.to_order = None
        self.orders = {}

    def set(self, name, lead_time, needed, obj):
        self.backend_object = obj
        self.name = name
        self.lead_time = lead_time
        self.needed = needed

    def add_order(self, amount, due):
        due_date = arrow.get(due, 'YYYY-MM-DD')
        self.orders[due_date] = amount

    def create_timeline(self):
        dates = sorted(self.orders)
        self.available_by = {}
        total = 0
        for date in dates:
            total += self.orders[date]
            self.available_by[date] = total

        return max(self.available_by.keys())

    def get_required_amount(self, amount):
        return self.needed * amount

    def compare_stock(self, amount):
        dates = sorted(self.available_by)
        return (self.available_by[dates[-1]] - amount)

    def use(self, amount):
        dates = sorted(self.available_by)
        for date in dates:
            if self.available_by[date] >= amount:
                break
        else:
            # never found enough materials
            print('{}, not enough material for {}'.format(self.name, amount))

        available_date = date
        # discount amount from all dates
        for date in dates:
            if date >= available_date:
                self.available_by[date] -= amount

        return available_date

    def __repr__(self):
        return "Name: {}, Orders: {}".format(self.name, self.orders)


class RawMaterials(object):

    def __init__(self):
        conf = Configuration()
        self.order_time = conf.get_time('ordering')
        self.raw_materials = []
        self.required_orders = None
        self.max_sim_date = None

    def append(self, name, lead_time, needed, stock, date, obj):
        rm = RawMaterial()
        rm.set(name, lead_time, needed, obj)
        rm.add_order(stock, date)
        self.raw_materials.append(rm)

    def get_materials(self):
        for rm in self.raw_materials:
            yield rm

    def create_timeline(self):
        dates = []
        for material in self.raw_materials:
            dates.append(material.create_timeline())
        self.max_sim_date = max(dates)

    def create_orders(self, amounts):
        self.required_orders = []
        for name, amount in amounts.items():
            for mat in self.raw_materials:
                if name == mat.name:
                    self._clone_to_order(mat, amount)

    def _clone_to_order(self, mat, amount):
        now = arrow.now()
        o = RawMaterial()
        o.set(mat.name, mat.lead_time, mat.needed, mat.backend_object)
        o.to_order = amount
        shift = int(o.lead_time) + int(self.order_time)
        o.order_due = now.replace(days=+shift)
        self.required_orders.append(o)

    def get_required_materials(self, pieces):
        required = {}
        for m in self.raw_materials:
            n = m.get_required_amount(pieces)
            required[m.name] = n
        return required

    def get_required_orders(self):
        return self.required_orders

    def use(self, required):
        dates = []
        for material, amount in required.items():
            for mat in self.raw_materials:
                if material == mat.name:
                    dates.append(mat.use(amount))
        return max(dates)

    def have_enough(self, required):
        need_more = {}
        for m in self.raw_materials:
            need = m.compare_stock(required[m.name])
            if (need < 0):
                need_more[m.name] = -need
        return need_more
