"""
Super simple representation of a raw material (or part)
of the thing we are producing.
"""


class RawMaterial(object):

    @staticmethod
    def create(name, lead_time, stock, due):
        r = RawMaterial()
        r.set(name, lead_time, stock)
        return r

    def __init__(self):
        self.name = None
        self.lead_time = None
        self.stock = None
        self.due = None

    def set(self, name, lead_time, stock, due):
        self.name = name
        self.lead_time = lead_time
        self.stock = stock
        self.due = due

    def __repr__(self):
        return "Name: {}, Lead time: {},"
        "Stock: {}, Due: {}".format(self.name, self.lead_time, self.stock,
                                    self.due)
