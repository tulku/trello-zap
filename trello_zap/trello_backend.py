"""
Gets the production information and outputs the
time estimates from and to a specially crafted Trello board.
"""
import os
from config import Configuration
from trello import TrelloClient
from raw_material import RawMaterials
from requests import Requests


class TrelloBackend(object):

    def __init__(self):
        self._trello = TrelloClient(api_key=os.environ['TRELLO_API_KEY'],
                                    api_secret=os.environ['TRELLO_API_SECRET'],
                                    token=os.environ['OAUTH_TOKEN'],
                                    token_secret=os.environ['OAUTH_SECRET'])

        config = Configuration()
        self._board_name = config.get_board_name()
        self._raw_materials_list = config.get_list('raw')
        self._orders_list = config.get_list('orders')
        self._requests_list = config.get_list('requests')
        self._to_order_list = config.get_list('to_order')

    def load_data(self):
        """ Reads all needed information from the backend. """
        board = self._get_production_board()
        self.lists = board.all_lists()

        raw_list = self._get_list(self._raw_materials_list)
        orders_list = self._get_list(self._orders_list)
        requests_list = self._get_list(self._requests_list)

        raw_materials = self._get_raw_materials(raw_list)
        self._get_orders(orders_list, raw_materials)

        requests = self._get_requests(requests_list)
        return raw_materials, requests

    def inform_required_orders(self, required_orders):
        """
        Shows to the user the orders that he needs to produce. The orders have
        the required amount in the description and an estimated due date based
        on the lead_time and the time it takes for the users to place the
        order.
        """
        to_order_list = self._get_list(self._to_order_list)
        for card in to_order_list.list_cards():
            card.delete()
        if required_orders is None:
            return

        for order in required_orders:
            order_desc = 'Amount: {}\n'.format(order.to_order)
            card = to_order_list.add_card(order.name, order_desc)
            card.set_due(order.order_due)

    def update_requests(self, requests):
        """
        Updates the requests cards on trello with the due date or marked as
        impossible with current stock.
        """
        for request in requests.get_requests():
            if request.impossible:
                request.backend_object.set_labels("red")
                request.backend_object.set_due(None)
                print 'Request {} is impossible.'.format(request.name)
            else:
                request.backend_object.set_due(request.due)
                request.backend_object.set_labels("")
                print 'Request {} due to {}.'.format(request.name, request.due)
        pass

    def _filter_by_name(self, items, name):
        for i in items:
            if i.name == name:
                i.fetch()
                return i

    def _parse_card_description(self, card):
        desc = card.description
        desc = desc.lower()
        lt_mark = 'lead time: '
        s_mark = 'stock: '
        n_mark = 'needed: '
        lt = int(desc.split(lt_mark)[1].split(' ')[0])
        sc = int(desc.split(s_mark)[1].split('\n')[0])
        n = float(desc.split(n_mark)[1].split('\n')[0])
        return lt, sc, n

    def _parse_order_card_description(self, card):
        desc = card.description
        desc = desc.lower()
        a_mark = 'amount: '
        a = int(desc.split(a_mark)[1].split('\n')[0])
        return a

    def _get_production_board(self):
        boards = self._trello.list_boards()
        return self._filter_by_name(boards, self._board_name)

    def _get_list(self, list_name):
        return self._filter_by_name(self.lists, list_name)

    def _get_raw_materials(self, raw_list):
        raw_materials = RawMaterials()
        for card in raw_list.list_cards():
            card.fetch()
            lt, sc, n = self._parse_card_description(card)
            raw_materials.append(card.name, lt, n, sc, card.due, card)
        return raw_materials

    def _get_orders(self, orders_list, raw_materials):
        for card in orders_list.list_cards():
            card.fetch()
            a = self._parse_order_card_description(card)
            try:
                due = card.due
            except AttributeError:
                due = None
            for m in raw_materials.get_materials():
                if m.name == card.name:
                    m.add_order(a, due)

    def _get_requests(self, requests_list):
        r = Requests()
        for card in requests_list.list_cards():
            card.fetch()
            a = self._parse_order_card_description(card)
            r.append(card.name, a, card)

        return r
