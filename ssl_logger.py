# -*- coding: utf-8 -*-

"""
A simple logger just recording specified debug logs.
"""

import logging


class SSLLogger(object):

    def __init__(self, name):
        if name not in logging.Logger.manager.loggerDict:
            SSLLogger.init_logger(name)

        self.logger = logger = logging.getLogger(name)

    @staticmethod
    def init_logger(name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s %(message)s')

        fh = logging.FileHandler(name + '.log')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        logger.addHandler(sh)

    def log(self, msg):
        self.logger.debug(msg)
