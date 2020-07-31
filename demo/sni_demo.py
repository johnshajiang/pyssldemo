# -*- coding: utf-8 -*-

"""
A simple demo on server name indication.
"""

import ssl
import time

from pyssldemo.client import Client
from pyssldemo.server import Server, ServerThread

if __name__ == '__main__':
    print(ssl.OPENSSL_VERSION)

    server_name = 'localhost'

    with ServerThread(Server()) as _s_thread:
        _s_thread.start()

        time.sleep(1)  # Wait for server accepting (?)

        _port = _s_thread.server.get_port()

        with Client() as _client:
            _client.server_name = server_name
            _client.connect(port=_port)
            if server_name != _s_thread.server.server_name:
                raise RuntimeWarning(f'Unexpected server name: {_s_thread.server.server_name}')
