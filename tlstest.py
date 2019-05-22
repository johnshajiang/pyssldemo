# -*- coding: utf-8 -*-

"""
TLS test
"""

from params import Protocols, CipherSuites
import utils

protocols = (Protocols.TLSV1_0, Protocols.TLSV1_1, Protocols.TLSV1_2)
cipher_suites = (CipherSuites.TLS_AES_128_GCM_SHA256,
                 CipherSuites.TLS_AES_256_GCM_SHA384,
                 CipherSuites.TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA,
                 CipherSuites.TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,
                 CipherSuites.TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA,
                 CipherSuites.TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384)


def run():
    for protocol in protocols:
        for cipher_suite in cipher_suites:
            if protocol in cipher_suite.value.protocols:
                run_case(protocol, cipher_suite)
            else:
                print('%s does NOT support %s' % (protocol.name, cipher_suite.name))


def run_case(protocol, cipher_suite):
    pass


if __name__ == '__main__':
    pass
