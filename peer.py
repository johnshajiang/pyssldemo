# -*- coding: utf-8 -*-

"""
TLS peer
"""

import ssl

from params import Protocols, CipherSuites
from certs import CertGroups
import utils


class Peer(object):
    """ TLS peer on specified parameters """

    def __init__(
            self,
            min_protocol=Protocols.TLSV1_0,
            max_protocol=Protocols.TLSV1_2,
            cert_group=CertGroups.RSA_GROUP,
            cipher_suites=(CipherSuites.TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA,),
            check_cert=True):
        self.context = utils.create_context(
            min_protocol,
            max_protocol,
            cert_group,
            cipher_suites)

        if check_cert:
            self.context.verify_mode = ssl.CERT_REQUIRED

    def log(self, msg):
        print(f'[{type(self).__name__}] {msg}')
