# -*- coding: utf-8 -*-

"""
A simple ssl demo
"""

import time
import ssl
from server import Server, ServerThread
from client import Client
import utils

if __name__ == '__main__':
    print(ssl.OPENSSL_VERSION)

    with ServerThread(Server()) as _s_thread:
        _s_thread.start()

        time.sleep(1) # Wait for server accepting (?)

        _host = 'localhost'
        _port = _s_thread.server.get_port()

        _client = Client()
        _client.connect(_host, _port, b'Client #1')
        _client.connect(_host, _port, b'Client #2')
        _client.connect(_host, _port, utils.SERVER_EXIT_FLAG)
