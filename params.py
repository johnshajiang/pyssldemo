# -*- coding: utf-8 -*-

"""
Parameters on TLS connection
"""

from enum import Enum, unique


class Protocol(object):
    def __init__(self, identity, name):
        self.identity = identity
        self.name = name

    def __repr__(self):
        return 'Protocol(%d, %s)' % (self.identity, self.name)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.identity == other.identity

    def __hash__(self):
        return self.identity


@unique
class Protocols(Enum):
    TLSV1_0 = Protocol(0x0301, 'TLSv1.0')
    TLSV1_1 = Protocol(0x0302, 'TLSv1.1')
    TLSV1_2 = Protocol(0x0303, 'TLSv1.2')
    TLSV1_3 = Protocol(0x0304, 'TLSv1.3')


@unique
class KeyAlgos(Enum):
    RSA = 'RSA'
    DSA = 'DSA'
    EC = 'EC'
    RSASSAPSS = 'RSASSA-PSS'


@unique
class SigAlgos(Enum):
    RSA = 'RSA'
    DSA = 'DSA'
    ECDSA = 'ECDSA'
    RSASSAPSS = 'RSASSA-PSS'


class KeyExAlgo(object):
    def __init__(self, name, key_algo, sig_algo):
        self.name = name
        self.key_algo = key_algo
        self.sig_algo = sig_algo

    def __repr__(self):
        return 'KeyExAlgo(%d, %s)' % (self.name, self.key_algo, self.sig_algo)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return self.name


@unique
class KeyExAlgos(Enum):
    DHE_RSA = KeyExAlgo('DHE_RSA', KeyAlgos.RSA, SigAlgos.RSA)
    ECDHE_ECDSA = KeyExAlgo('ECDHE_ECDSA', KeyAlgos.EC, SigAlgos.ECDSA)
    ECDHE_RSA = KeyExAlgo('ECDHE_RSA', KeyAlgos.EC, SigAlgos.RSA)
    RSA = KeyExAlgo('RSA', KeyAlgos.RSA, SigAlgos.RSA)


@unique
class HashAlgos(Enum):
    SHA1 = 'SHA-1'
    SHA256 = 'SHA-256'
    SHA384 = 'SHA-384'
    SHA512 = 'SHA-512'


class CipherSuite(object):
    def __init__(self, identity, name, key_ex_algo, *protocols):
        self.identity = identity
        self.name = name
        self.key_ex_algo = key_ex_algo
        self.protocols = protocols

    def __repr__(self):
        return 'CipherSuite(%d, %s)' % (self.identity, self.name)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.identity == other.identity

    def __hash__(self):
        return self.identity


@unique
class CipherSuites(Enum):
    TLS_AES_256_GCM_SHA384 = CipherSuite(
        0x1301,
        'TLS_AES_256_GCM_SHA384',
        None,
        Protocols.TLSV1_3)

    TLS_AES_128_GCM_SHA256 = CipherSuite(
        0x1302,
        'TLS_AES_128_GCM_SHA256',
        None,
        Protocols.TLSV1_3)

    TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA = CipherSuite(
        0xC014,
        'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
        KeyExAlgos.ECDHE_RSA,
        Protocols.TLSV1_0, Protocols.TLSV1_1, Protocols.TLSV1_2)

    TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA = CipherSuite(
        0xC024,
        'TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA',
        KeyExAlgos.ECDHE_ECDSA,
        Protocols.TLSV1_0, Protocols.TLSV1_1, Protocols.TLSV1_2)

    TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384 = CipherSuite(
        0xC02C,
        'TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384',
        KeyExAlgos.ECDHE_ECDSA,
        Protocols.TLSV1_2)

    TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 = CipherSuite(
        0xC030,
        'TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384',
        KeyExAlgos.ECDHE_RSA,
        Protocols.TLSV1_2)
