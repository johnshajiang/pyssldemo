# -*- coding: utf-8 -*-

"""
A simple demo on checking ALPN.
"""

import ssl
from pyssldemo.server import Server, ServerThread
from pyssldemo.client import Client


if __name__ == '__main__':
    print(ssl.OPENSSL_VERSION)

    _server = Server()
    _server.set_app_protocols('http/1.1', 'http/2')

    with ServerThread(_server) as _s_thread:
        _s_thread.start()

        _port = _server.get_port()

        with Client() as _client:
            _client.set_app_protocols('http/2')
            _client.connect(port=_port)
            _negotiated_app_protocol = _client.get_app_protocol()

            if _negotiated_app_protocol != 'http/2':
                raise RuntimeWarning(f'Unexpected app protocol: {_client.get_app_protocol()}')

        Client.signal_close_server(context=_client.context, port=_port)
