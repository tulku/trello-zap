"""
Super simple representation of a raw material (or part)
of the thing we are producing.
"""


class RawMaterial(object):

    @staticmethod
    def create(name, lead_time, stock):
        r = RawMaterial()
        r.set(name, lead_time, stock)
        return r

    def __init__(self):
        self.name = None
        self.lead_time = None
        self.stock = None

    def set(self, name, lead_time, stock):
        self.name = name
        self.lead_time = lead_time
        self.stock = stock

    def __repr__(self):
        return "Name: {}, Lead time: {}, Stock: {}".format(self.name,
                                                           self.lead_time,
                                                           self.stock)
