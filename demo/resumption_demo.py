# -*- coding: utf-8 -*-

"""
A simple demo on session resumption over TLS 1.2 and 1.3.
"""

import ssl
from pyssldemo.server import Server, ServerThread
from pyssldemo.client import Client
from pyssldemo.params import Protocols
from pyssldemo import utils


@utils.func_separator()
def run_case(context, port):
    print(f'Protocol: {utils.tls_protocol(context.minimum_version).value.name}')

    with Client(context) as _client1:
        _client1.connect(port=port)
        _session = _client1.get_session()
    with Client(context=_client1.context, session=_session) as _client2:
        _client2.connect(port=port)

        if not _client2.is_session_resumed():
            raise RuntimeWarning('Session is not resumed')
        else:
            print('Session was resumed')


if __name__ == '__main__':
    print(ssl.OPENSSL_VERSION)

    with ServerThread(Server()) as _s_thread:
        _s_thread.start()

        _port = _s_thread.server.get_port()

        for _protocol in (Protocols.TLSV1_2, Protocols.TLSV1_3):
            _context = utils.create_context(min_protocol=_protocol, max_protocol=_protocol)
            run_case(_context, _port)

        Client.signal_close_server(context=_context, port=_port)
