# -*- coding: utf-8 -*-

"""
A simple demo on session resumption.
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

        time.sleep(1)  # Wait for server accepting (?)

        _port = _s_thread.server.get_port()

        _client1 = Client()
        _client1.connect(port=_port)

        _client2 = Client(context=_client1.context, session=_client1.session)
        _client2.connect(port=_port)
        if not _client2.session_resumed:
            raise RuntimeError('Session is not reused')
        else:
            print('Session was reused')

        _client2.signal_close_server(port=_port)
