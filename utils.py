# -*- coding: utf-8 -*-

"""
Utilities
"""

import os
import os.path
import ssl
from pyssldemo.params import Protocols, CipherSuites
from pyssldemo.certs import CertGroups


def tls_version(protocol):
    """ Convert Protocol to TLS protocol option """

    if protocol == Protocols.TLSV1_0:
        return ssl.TLSVersion.TLSv1
    elif protocol == Protocols.TLSV1_1:
        return ssl.TLSVersion.TLSv1_1
    elif protocol == Protocols.TLSV1_2:
        return ssl.TLSVersion.TLSv1_2
    elif protocol == Protocols.TLSV1_3:
        return ssl.TLSVersion.TLSv1_3
    else:
        return None


def tls_protocol(version):
    """ Convert Protocol to TLS protocol option """

    if version == ssl.TLSVersion.TLSv1:
        return Protocols.TLSV1_0
    elif version == ssl.TLSVersion.TLSv1_1:
        return Protocols.TLSV1_1
    elif version == ssl.TLSVersion.TLSv1_2:
        return Protocols.TLSV1_2
    elif version == ssl.TLSVersion.TLSv1_3:
        return Protocols.TLSV1_3
    else:
        return None


def openssl_cs(cipher_suites):
    """ Convert CipherSuites to OpenSSL cipher suite names """

    _cipher_suites = []
    for _cipher_suite in cipher_suites:
        if _cipher_suite == CipherSuites.TLS_AES_256_GCM_SHA384:
            _cipher_suites.append('TLS_AES_256_GCM_SHA384')
        elif _cipher_suite == CipherSuites.TLS_AES_128_GCM_SHA256:
            _cipher_suites.append('TLS_AES_128_GCM_SHA256')
        elif _cipher_suite == CipherSuites.TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA:
            _cipher_suites.append('ECDHE-RSA-AES256-SHA')
        elif _cipher_suite == CipherSuites.TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA:
            _cipher_suites.append('ECDHE-ECDSA-AES256-SHA')
        elif _cipher_suite == CipherSuites.TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384:
            _cipher_suites.append('ECDHE-ECDSA-AES256-GCM-SHA384')
        elif _cipher_suite == CipherSuites.TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384:
            _cipher_suites.append('ECDHE-RSA-AES256-GCM-SHA384')

    return ':'.join(_cipher_suites)


CERT_DIR = os.getenv('PYSSLDEMO_CERT_DIR')


def get_cert_path(cert_file):
    return os.path.join(CERT_DIR, cert_file)


def create_context(
    min_protocol=Protocols.TLSV1_2,
    max_protocol=Protocols.TLSV1_3,
    cert_group=CertGroups.ECDSA_GROUP,
    cipher_suites=(
        CipherSuites.TLS_AES_128_GCM_SHA256,
        CipherSuites.TLS_AES_256_GCM_SHA384,
        CipherSuites.TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,
        CipherSuites.TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA)):
    """
    Create SSL context with specified protocols, certificate group and cipher suites.
    """

    _context = ssl.SSLContext()
    _context.minimum_version = tls_version(min_protocol)
    _context.maximum_version = tls_version(max_protocol)

    _context.set_ciphers(openssl_cs(cipher_suites))

    _context.load_verify_locations(
        cafile=get_cert_path(cert_group.value.ca.value.cert_file))
    _context.load_cert_chain(
        certfile=get_cert_path(
            cert_group.value.server_cert.value.cert_file), keyfile=get_cert_path(
            cert_group.value.server_cert.value.priv_key_file))

    _context.verify_mode = ssl.CERT_NONE
    _context.check_hostname = False

    return _context


def func_separator(title=None):
    def wrapper(func):
        if title is None:
            _title = func.__name__
        else:
            _title = title

        def func_wrapper(*args, **kwargs):
            print(f'========== {_title} start ==========')
            func(*args, **kwargs)
            print(f'========== {_title} end ==========')
        return func_wrapper
    return wrapper
