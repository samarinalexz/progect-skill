import logging
from random import choice

class SpecialFilter(logging.Filter):
    # """
    # This is a filter which injects contextual information into the log.
    #
    # Rather than use actual contextual information, we just use random
    # data in this demo.
    # """

    USERS = ['jim', 'fred', 'sheila']
    IPS = ['123.231.231.123', '127.0.0.1', '192.168.0.1']

    def filter(self, record):

        record.ip = choice(SpecialFilter.IPS)
        record.user = choice(SpecialFilter.USERS)
        return True