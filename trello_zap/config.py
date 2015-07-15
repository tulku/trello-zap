import ConfigParser
import os


class Configuration(object):

    def __init__(self, conf_file=None):
        self.config = ConfigParser.ConfigParser()
        if conf_file is None:
            conf_file = os.environ['TRELLO_ZAP_CONFIG']
        self.config.readfp(open(conf_file))

    def get_board_name(self):
        return self.config.get('Board', 'board_name')

    def get_list(self, name):
        return self.config.get('Lists', name)

    def get_time(self, time):
        return int(self.config.get('Days', time))

    def get_offlinefile(self):
        return self.config.get('Offline', 'filename')
