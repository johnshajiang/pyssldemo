# -*- coding: utf-8 -*-

"""
A simple demo on basic connection with server authentication.
"""

import ssl
from pyssldemo.server import Server, ServerThread
from pyssldemo.client import Client


if __name__ == '__main__':
    print(ssl.OPENSSL_VERSION)

    with ServerThread(Server()) as _s_thread:
        _s_thread.start()

        _port = _s_thread.server.get_port()

        with Client() as _client:
            _client.connect(port=_port)

        Client.signal_close_server(context=_client.context, port=_port)
