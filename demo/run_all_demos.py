# -*- coding: utf-8 -*-

"""Run all demos.
"""

import os
import ssl
import subprocess

demo_names = (
    'alpn_demo',
    'basic_conn_demo',
    'client_auth_demo',
    'combo_conn_demo',
    'conc_conn_demo',
    'resumption_demo',
    'sni_demo'
)


def run_demo(demo_name):
    _dir = os.path.dirname(os.path.abspath(__file__))
    _demo_path = os.path.join(_dir, demo_name + '.py')
    print(f'Demo: {_demo_path}')
    return subprocess.run(['python3', _demo_path])


if __name__ == '__main__':
    print(ssl.OPENSSL_VERSION)

    for _demo_name in demo_names:
        cp = run_demo(_demo_name)
        if cp.returncode != 0:
            raise RuntimeError(f'{_demo_name} failed!')
