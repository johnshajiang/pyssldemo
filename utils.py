# -*- coding: utf-8 -*-

"""
Utilities
"""

import os
import os.path
import ssl
from params import Protocols, KeyExAlgos, CipherSuites


SERVER_EXIT_FLAG = b'EXIT'


def tls_version(protocol):
    """ Convert Protocol to TLS protocol option """

    if protocol == Protocols.TLSV1_0:
        return ssl.TLSVersion.TLSv1
    elif protocol == Protocols.TLSV1_1:
        return ssl.TLSVersion.TLSv1_1
    elif protocol == Protocols.TLSV1_2:
        return ssl.TLSVersion.TLSv1_2
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


CERT_DIR = os.getenv('PYSSLDEMO.CERT.DIR')


def get_cert_path(cert_file):
    return os.path.join(CERT_DIR, cert_file)


def create_context(
        min_protocol,
        max_protocol,
        cert_group,
        cipher_suites):
    """
    Create SSL context with specified protocol and cipher suite.
    The CA and end entity certificate are automatically determined by the cipher suite.
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

    return _context
