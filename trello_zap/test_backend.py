"""
Implements a testing backend. This should allow simpler unittesting
and faster development (no need to download trello information)
"""
import os
import cPickle as pickle


class TestBackend(object):

    def __init__(self):
        self.filename = os.environ['OFFLINE_FILE']

    def load_data(self):
        data = open(self.filename, 'rb')
        (materials, requests) = pickle.load(data)
        return materials, requests

    def save_data(self, materials, requests):
        "Creates off line files with the information passed as parameters."
        data = open(self.filename, 'wb')
        pickle.dump((materials, requests), data, -1)
