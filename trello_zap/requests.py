
class Request(object):
    """ Represents a request of a product. """

    @staticmethod
    def create(name, amount):
        r = Request()
        r.set(name, amount)

    def __init__(self):
        self.amount = None
        self.name = None
        self.due = None

    def set(self, name, amount):
        self.name = name
        self.amount = amount

    def __repr__(self):
        return " Resquest for {} of {}".format(self.name, self.amount)


class Requests(object):

    def __init__(self):
        self.requests = []

    def append(self, name, amount):
        self.requests.append(Request.create(name, amount))
