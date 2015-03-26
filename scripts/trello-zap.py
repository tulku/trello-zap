import os
from trello import TrelloClient


class TrelloZap(object):

    def __init__(self):
        self._trello = TrelloClient(api_key=os.environ['TRELLO_API_KEY'],
                                    api_secret=os.environ['TRELLO_API_SECRET'],
                                    token=os.environ['OAUTH_TOKEN'],
                                    token_secret=os.environ['OAUTH_SECRET'])
        board = self.get_production_board()
        print self.get_raw_materials(board)

    def get_production_board(self):
        boards = self._trello.list_boards()
        for b in boards:
            if b.name == 'Lanza - Production':
                b.fetch()
                return b

    def get_raw_materials(self, board):
        lists = board.all_lists()
        for l in lists:
            if l.name == 'Parts':
                l.fetch()
                return l


if __name__ == '__main__':
    tz = TrelloZap()
