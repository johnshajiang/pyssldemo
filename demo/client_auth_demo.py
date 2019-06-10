# -*- coding: utf-8 -*-

"""
A simple demo on client authentication.
"""

import time
import ssl
from pyssldemo.server import Server, ServerThread
from pyssldemo.client import Client


if __name__ == '__main__':
    print(ssl.OPENSSL_VERSION)

    _server = Server()
    _server.set_peer_auth(True)

    with ServerThread(_server) as _s_thread:
        _s_thread.start()

        time.sleep(1)  # Wait for server accepting (?)

        _port = _server.get_port()

        _client = Client()
        _client.connect(port=_port)

        Client.signal_close_server(context=_client.context, port=_port)
