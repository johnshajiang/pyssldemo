# -*- coding: utf-8 -*-

"""
A simple ssl demo
"""

import time
import ssl
from params import Protocols, CipherSuites
from server import Server, ServerThread
from client import Client
import utils

if __name__ == '__main__':
    print(ssl.OPENSSL_VERSION)

    protocol = Protocols.TLSV1_2
    cipher_suite = CipherSuites.TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384

    s_thread = ServerThread(Server(protocol, cipher_suite))
    s_thread.start()
    port = s_thread.server.get_port()

    time.sleep(1) # Wait for server accepting

    client = Client(protocol, cipher_suite)
    client.connect('localhost', port, b'Client #1')
    client.connect('localhost', port, b'Client #2')
    client.connect('localhost', port, utils.SERVER_EXIT_FLAG)
