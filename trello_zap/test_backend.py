"""
Implements a testing backend. This should allow simpler unittesting
and faster development (no need to download trello information)
"""
from .config import Configuration
import pickle


class TestBackend(object):

    def __init__(self):
        self.filename = Configuration().get_offlinefile()

    def load_data(self):
        data = open(self.filename, 'rb')
        (materials, requests) = pickle.load(data)
        return materials, requests

    def save_data(self, materials, requests):
        "Creates off line files with the information passed as parameters."
        data = open(self.filename, 'wb')
        pickle.dump((materials, requests), data, -1)

    def inform_required_orders(self, orders):
        if orders is not None:
            for o in orders:
                print('Need to order {} {}. Due {}'.format(o.to_order,
                                                           o.name,
                                                           o.order_due))
        else:
            print('There are no new orders required.')

    def update_requests(self, requests):
        for request in requests.get_requests():
            if request.impossible:
                print('Request {} is impossible.'.format(request.name))
            else:
                print('Request {} due to {}.'.format(request.name, request.due))
