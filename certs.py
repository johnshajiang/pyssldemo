# -*- coding: utf-8 -*-

"""
Certificates and the associated private keys
"""

from enum import Enum, unique
from pyssldemo.params import KeyAlgos, SigAlgos, HashAlgos


class Cert(object):
    def __init__(
            self,
            key_algo,
            sig_algo,
            hash_algo,
            cert_file,
            priv_key_file):
        self.key_algo = key_algo
        self.sig_algo = sig_algo
        self.hash_algo = hash_algo
        self.cert_file = cert_file
        self.priv_key_file = priv_key_file

    def __eq__(self, other):
        return self.cert_file == other.cert_file

    def __repr__(self):
        return 'KeyAlgo: %s, SigAlgo: %s, HashAlgo: %s\nCert: %s\nPrivateKey: %s' % (
            self.key_algo, self.sig_algo, self.hash_algo, self.cert_file, self.priv_key_file)

    def __str__(self):
        return 'KeyAlgo: %s, SigAlgo: %s, HashAlgo: %s' % (
            self.key_algo, self.sig_algo, self.hash_algo)


@unique
class Certs(Enum):
    CA_ECDSA = Cert(KeyAlgos.EC,
                    SigAlgos.ECDSA,
                    HashAlgos.SHA256,
                    'CA_ECDSA.cer',
                    'CA_ECDSA.key')
    CA_RSA = Cert(KeyAlgos.RSA,
                  SigAlgos.RSA,
                  HashAlgos.SHA256,
                  'CA_RSA.cer',
                  'CA_RSA.key')

    SERVER_ECDSA = Cert(KeyAlgos.EC,
                        SigAlgos.ECDSA,
                        HashAlgos.SHA256,
                        'SERVER_ECDSA.cer',
                        'SERVER_ECDSA.key')
    SERVER_RSA = Cert(KeyAlgos.RSA,
                      SigAlgos.RSA,
                      HashAlgos.SHA256,
                      'SERVER_RSA.cer',
                      'SERVER_RSA.key')

    CLIENT_ECDSA = Cert(KeyAlgos.EC,
                        SigAlgos.ECDSA,
                        HashAlgos.SHA256,
                        'CLIENT_ECDSA.cer',
                        'CLIENT_ECDSA.key')
    CLIENT_RSA = Cert(KeyAlgos.RSA,
                      SigAlgos.RSA,
                      HashAlgos.SHA256,
                      'CLIENT_RSA.cer',
                      'CLIENT_RSA.key')


class CertGroup(object):
    def __init__(self, ca, server_cert, client_cert):
        self.ca = ca
        self.server_cert = server_cert
        self.client_cert = client_cert

    def __str__(self):
        return f'CA: {self.ca}\nServer cert: {self.server_cert}\nClient cert:{self.client_cert}'


class CertGroups(Enum):
    RSA_GROUP = CertGroup(Certs.CA_RSA, Certs.SERVER_RSA, Certs.CLIENT_RSA)
    ECDSA_GROUP = CertGroup(Certs.CA_ECDSA, Certs.SERVER_ECDSA, Certs.CLIENT_ECDSA)
