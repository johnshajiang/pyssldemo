#! /bin/bash

# Generate RSA CA, server and client end entity certificates
openssl genpkey -algorithm rsa -pkeyopt rsa_keygen_bits:2048 -pkeyopt rsa_keygen_pubexp:65537 -out CA_RSA.key
openssl req -x509 -new -key CA_RSA.key -days 3650 -subj "/CN=CA-RSA" -sha256 -out CA_RSA.cer

openssl genpkey -algorithm rsa -pkeyopt rsa_keygen_bits:2048 -pkeyopt rsa_keygen_pubexp:65537 -out SERVER_RSA.key
openssl req -new -key SERVER_RSA.key -subj "/CN=SERVER-RSA" -sha256 -out SERVER_RSA.csr
openssl x509 -req -CAcreateserial -days 3650 -in SERVER_RSA.csr -sha256 -CA CA_RSA.cer -CAkey CA_RSA.key -out SERVER_RSA.cer

openssl genpkey -algorithm rsa -pkeyopt rsa_keygen_bits:2048 -pkeyopt rsa_keygen_pubexp:65537 -out CLIENT_RSA.key
openssl req -new -key CLIENT_RSA.key -subj "/CN=CLIENT-RSA" -sha256 -out CLIENT_RSA.csr
openssl x509 -req -CAcreateserial -days 3650 -in CLIENT_RSA.csr -sha256 -CA CA_RSA.cer -CAkey CA_RSA.key -out CLIENT_RSA.cer

rm CA_RSA.srl SERVER_RSA.csr CLIENT_RSA.csr

#Generate ECDSA CA, server and client end entity certificates
openssl genpkey -algorithm ec -pkeyopt ec_paramgen_curve:P-256 -pkeyopt ec_param_enc:named_curve -out CA_ECDSA.key
openssl req -x509 -new -key CA_ECDSA.key -days 3650 -subj "/CN=CA-ECDSA" -sha256 -out CA_ECDSA.cer

openssl genpkey -algorithm ec -pkeyopt ec_paramgen_curve:P-256 -pkeyopt ec_param_enc:named_curve -out SERVER_ECDSA.key
openssl req -new -key SERVER_ECDSA.key -subj "/CN=SERVER-ECDSA" -sha256 -out SERVER_ECDSA.csr
openssl x509 -req -CAcreateserial -days 3650 -in SERVER_ECDSA.csr -sha256 -CA CA_ECDSA.cer -CAkey CA_ECDSA.key -out SERVER_ECDSA.cer

openssl genpkey -algorithm ec -pkeyopt ec_paramgen_curve:P-256 -pkeyopt ec_param_enc:named_curve -out CLIENT_ECDSA.key
openssl req -new -key CLIENT_ECDSA.key -subj "/CN=CLIENT-ECDSA" -sha256 -out CLIENT_ECDSA.csr
openssl x509 -req -CAcreateserial -days 3650 -in CLIENT_ECDSA.csr -sha256 -CA CA_ECDSA.cer -CAkey CA_ECDSA.key -out CLIENT_ECDSA.cer

rm CA_ECDSA.srl SERVER_ECDSA.csr CLIENT_ECDSA.csr
