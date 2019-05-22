# -*- coding: utf-8 -*-

"""
Utilities
"""

import os
import os.path
import ssl
from params import Protocols, KeyExAlgos, CipherSuites
from certs import Certs, CertGroup


def get_cert_group(key_ex_algo):
    """ Assemble CertGroup based on the specified key exchange algorithm """

    if key_ex_algo in (
            KeyExAlgos.RSA,
            KeyExAlgos.DHE_RSA,
            KeyExAlgos.ECDHE_RSA):
        return CertGroup(Certs.CA_RSA, Certs.SERVER_RSA, Certs.CLIENT_RSA)
    else:
        return CertGroup(
            Certs.CA_ECDSA,
            Certs.SERVER_ECDSA,
            Certs.CLIENT_ECDSA)


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


def openssl_cs(cipher_suite):
    """ Convert CipherSuite to OpenSSL cipher suite name """

    if cipher_suite == CipherSuites.TLS_AES_256_GCM_SHA384:
        return 'TLS_AES_256_GCM_SHA384'
    elif cipher_suite == CipherSuites.TLS_AES_128_GCM_SHA256:
        return 'TLS_AES_128_GCM_SHA256'
    elif cipher_suite == CipherSuites.TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA:
        return 'ECDHE-RSA-AES256-SHA'
    elif cipher_suite == CipherSuites.TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA:
        return 'ECDHE-ECDSA-AES256-SHA'
    elif cipher_suite == CipherSuites.TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384:
        return 'ECDHE-ECDSA-AES256-GCM-SHA384'
    elif cipher_suite == CipherSuites.TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384:
        return 'ECDHE-RSA-AES256-GCM-SHA384'
    else:
        return None


CERT_DIR = os.getenv('TLSTEST.CERT.DIR')


def get_cert_path(cert_file):
    return os.path.join(CERT_DIR, cert_file)


def create_context(protocol, cipher_suite):
    """
    Create SSL context with specified protocol and cipher suite.
    The CA and end entity certificate are automatically determined by the cipher suite
    """

    _context = ssl.SSLContext()
    _tls_version = tls_version(protocol)
    _context.minimum_version = _tls_version
    _context.maximum_version = _tls_version

    _context.verify_mode = ssl.CERT_REQUIRED
    _context.check_hostname = False

    _context.set_ciphers(openssl_cs(cipher_suite))

    _cert_group = get_cert_group(cipher_suite.value.key_ex_algo)
    _context.load_verify_locations(
        cafile=get_cert_path(_cert_group.ca.value.cert_file))
    _context.load_cert_chain(
        certfile=get_cert_path(_cert_group.server_cert.value.cert_file),
        keyfile=get_cert_path(_cert_group.server_cert.value.priv_key_file))

    return _context
