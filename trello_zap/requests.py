
class Request(object):
    """ Represents a request of a product. """

    def __init__(self):
        self.backend_object = None
        self.amount = None
        self.name = None
        self.due = None
        self.impossible = False
        self.due = None

    def set(self, name, amount, obj):
        self.name = name
        self.amount = amount
        self.backend_object = obj

    def mark_impossible(self):
        self.impossible = True
        print 'Request {} for {} impossible'.format(self.amount, self.name)

    def set_due(self, due):
        self.due = due
        print 'Request {} for {} due {}'.format(self.amount, self.name, due)

    def __str__(self):
        return " Resquest for {} of {}".format(self.name, self.amount)


class Requests(object):

    def __init__(self):
        self.requests = []
        self.total = 0

    def append(self, name, amount, obj):
        self.total += amount
        r = Request()
        r.set(name, amount, obj)
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
