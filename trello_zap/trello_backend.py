"""
Gets the production information and outputs the
time estimates from and to a specially crafted Trello board.
"""
import os
from trello import TrelloClient
from raw_material import RawMaterial


class TrelloBackend(object):

    def __init__(self):
        self._trello = TrelloClient(api_key=os.environ['TRELLO_API_KEY'],
                                    api_secret=os.environ['TRELLO_API_SECRET'],
                                    token=os.environ['OAUTH_TOKEN'],
                                    token_secret=os.environ['OAUTH_SECRET'])

        self._board_name = os.environ['TRELLO_BOARD']
        self._raw_materials_list = os.environ['TRELLO_RAW_LIST']
        self._orders_list = os.environ['TRELLO_ORDERS_LIST']
        self._requests_list = os.environ['TRELLO_REQUESTS_LIST']

    def load_data(self):
        """ Reads all needed information from the backend. """
        board = self._get_production_board()
        raw_list = self._get_list(board, self._raw_materials_list)
        orders_list = self._get_list(board, self._orders_list)
        requests_list = self._get_list(board, self._requests_list)

        print self._get_raw_materials(raw_list)

    def _filter_by_name(self, items, name):
        for i in items:
            if i.name == name:
                i.fetch()
                return i

    def _parse_card_description(self, card):
        desc = card.description
        lt_mark = 'Lead Time: '
        s_mark = 'Stock: '
        lt = int(desc.split(lt_mark)[1].split(' ')[0])
        sc = int(desc.split(s_mark)[1])
        return lt, sc

    def _get_production_board(self):
        boards = self._trello.list_boards()
        return self._filter_by_name(boards, self._board_name)

    def _get_list(self, board, list_name):
        lists = board.all_lists()
        return self._filter_by_name(lists, list_name)

    def _get_raw_materials(self, raw_list):
        raw_materials = []
        for card in raw_list.list_cards():
            lt, sc = self._parse_card_description(card)
            due = card.due
            raw_materials.append(RawMaterial.create(card.name, lt, sc, due))
        return raw_materials
