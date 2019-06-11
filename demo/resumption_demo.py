# -*- coding: utf-8 -*-

"""
A simple demo on session resumption.
"""

import ssl
from pyssldemo.server import Server, ServerThread
from pyssldemo.client import Client


if __name__ == '__main__':
    print(ssl.OPENSSL_VERSION)

    with ServerThread(Server()) as _s_thread:
        _s_thread.start()

        _port = _s_thread.server.get_port()

        with Client() as _client1:
            _client1.connect(port=_port)
            _session = _client1.get_session()

        with Client(context=_client1.context, session=_session) as _client2:
            _client2.connect(port=_port)

            if not _client2.is_session_resumed():
                raise RuntimeWarning('Session is not resumed')
            else:
                print('Session was resumed')

        Client.signal_close_server(context=_client1.context, port=_port)
