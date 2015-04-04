
class Request(object):
    """ Represents a request of a product. """

    @staticmethod
    def create(name, amount):
        r = Request()
        r.set(name, amount)
        return r

    def __init__(self):
        self.amount = None
        self.name = None
        self.due = None

    def set(self, name, amount):
        self.name = name
        self.amount = amount

    def mark_impossible(self):
        print 'Request {} for {} impossible'.format(self.amount, self.name)

    def __str__(self):
        return " Resquest for {} of {}".format(self.name, self.amount)


class Requests(object):

    def __init__(self):
        self.requests = []
        self.total = 0

    def append(self, name, amount):
        self.total += amount
        r = Request.create(name, amount)
        self.requests.append(r)

    def get_total(self):
        return self.total

    def get_requests(self):
        for r in self.requests:
            yield r

    def __str__(self):
        s = "["
        for r in self.requests:
            s += str(r) + ", "
        return (s + "]")
