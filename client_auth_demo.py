# -*- coding: utf-8 -*-

"""
A simple demo on checking client authentication.
"""

import time
import ssl
from server import Server, ServerThread
from client import Client
import utils


if __name__ == '__main__':
    print(ssl.OPENSSL_VERSION)

    _server = Server()
    _server.set_client_auth(True)

    with ServerThread(_server) as _s_thread:
        _s_thread.start()

        time.sleep(1)  # Wait for server accepting (?)

        _port = _server.get_port()

        _client = Client()
        _client.connect(port=_port)
        _client.connect(port=_port, msg=utils.SERVER_EXIT_FLAG)
