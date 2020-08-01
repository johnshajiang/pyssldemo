# -*- coding: utf-8 -*-

"""TLS server
"""

import os
import socket
import ssl
import time
from threading import Thread

from pyssldemo.peer import Peer


class Server(Peer):

    def __init__(self, context=None, port=0):
        super(Server, self).__init__(context)
        self.context.sni_callback = self.sni_callback
        self.port = port

        self.s_socket = None  # Server-side SSL socket
        self.c_socket = None  # Accepted SSL socket
        self.server_name = None  # Selected SNI server name

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def sni_callback(self, socket, server_name, context):
        """
        It just records the indicated server name,
        but DOESN'T verify the certificate chain on this server name.
        """

        self.log(f'Indicated server name: {server_name}')
        self.server_name = server_name

    def get_session(self):
        return self.s_socket.session

    def is_session_resumed(self):
        return self.s_socket.session_reused

    def get_app_protocol(self):
        return self.s_socket.selected_alpn_protocol()

    def start(self):
        self.s_socket = self.context.wrap_socket(
            socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM),
            server_side=True)
        self.s_socket.bind(('127.0.0.1', self.port))
        self.s_socket.listen()

        real_port = self.s_socket.getsockname()[1]
        self.log(f'Listening {real_port}')

        _port_log = self.get_port_log_path()
        with open(_port_log, 'w') as f:
            f.write(f'{real_port}')
            self.log(f'Generated port log: {os.path.abspath(_port_log)}')

    def accept(self):
        self.log('Accepting connection ...')
        while True:
            try:
                self.c_socket, _addr = self.s_socket.accept()
                self.log(f'Client address: {_addr}')
                Thread(target=self.connect(self.c_socket)).start()
            except Exception:
                self.log('Server was stopped')
                break

    def connect(self, c_socket):
        self.log(f'Negotiated protocol: {c_socket.version()}')
        self.log(f'Negotiated cipher suite: {c_socket.cipher()}')

        with c_socket:
            request = c_socket.recv(1024)
            self.log(f'Request: {request}')
            c_socket.sendall(b'Client said: ' + request)
            self.log('Send response')

    def close(self):
        self.s_socket.close()

        _port_log = self.get_port_log_path()
        if os.path.isfile(_port_log):
            os.remove(_port_log)
            self.log(f'Removed port log: {os.path.abspath(_port_log)}')

        self.log('Closed')

    def get_log_path(self):
        return 'server.log'

    def get_port_log_path(self):
        return 'port.log'

    def get_port(self):
        """
        Read port from the local port log file.
        If the file is unavailable, the caller would be blocked.
        """

        _port_log = self.get_port_log_path()

        # Wait for port is ready
        while not os.path.isfile(_port_log):
            self.log('Waiting for port ...')
            time.sleep(1)

        with open(_port_log, 'r') as f:
            return int(f.readline())


class ServerThread(Thread):
    def __init__(self, server):
        Thread.__init__(self)
        self.server = server

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server.close()

    def run(self):
        self.server.start()
        self.server.accept()


if __name__ == '__main__':
    print(ssl.OPENSSL_VERSION)

    try:
        with Server(port=65443) as _server:
            _server.start()
            _server.accept()
    except KeyboardInterrupt:
        print('Server exited')
