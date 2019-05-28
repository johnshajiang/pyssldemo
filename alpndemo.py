# -*- coding: utf-8 -*-

"""
A simple demo on checking ALPN.
"""

import time
import ssl
from server import Server, ServerThread
from client import Client
import utils


if __name__ == '__main__':
    print(ssl.OPENSSL_VERSION)

    _server = Server()
    _server.set_app_protocols('http/1.1', 'http/2')

    with ServerThread(_server) as _s_thread:
        _s_thread.start()

        time.sleep(1)  # Wait for server accepting (?)

        _port = _s_thread.server.get_port()

        _client = Client()
        _client.set_app_protocols('http/2')

        _client.connect(port=_port)

        if _client.negotiated_app_protocol != 'http/2':
            raise ValueError(f'Unexpected app protocol: {_client.negotiated_app_protocol}')

        _client.connect(port=_port, msg=utils.SERVER_EXIT_FLAG)
