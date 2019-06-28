#! /bin/bash

# Create X.509 v3 extension
echo "subjectKeyIdentifier = hash" > v3.ext
echo "authorityKeyIdentifier = keyid,issuer" >> v3.ext

# Generate RSA CA, server and client end entity certificates
openssl genpkey -algorithm rsa -pkeyopt rsa_keygen_bits:2048 -pkeyopt rsa_keygen_pubexp:65537 -out CA_RSA.key
openssl req -x509 -new -key CA_RSA.key -days 3650 -subj "/CN=CA-RSA" -sha256 -out CA_RSA.cer.tmp
openssl x509 -text -in CA_RSA.cer.tmp > CA_RSA.cer

openssl genpkey -algorithm rsa -pkeyopt rsa_keygen_bits:2048 -pkeyopt rsa_keygen_pubexp:65537 -out SERVER_RSA.key
openssl req -new -key SERVER_RSA.key -subj "/CN=SERVER-RSA" -sha256 -out SERVER_RSA.csr
openssl x509 -extfile v3.ext -req -CAcreateserial -days 3650 -in SERVER_RSA.csr -sha256 -CA CA_RSA.cer -CAkey CA_RSA.key -out SERVER_RSA.cer.tmp
openssl x509 -text -in SERVER_RSA.cer.tmp > SERVER_RSA.cer

openssl genpkey -algorithm rsa -pkeyopt rsa_keygen_bits:2048 -pkeyopt rsa_keygen_pubexp:65537 -out CLIENT_RSA.key
openssl req -new -key CLIENT_RSA.key -subj "/CN=CLIENT-RSA" -sha256 -out CLIENT_RSA.csr
openssl x509 -extfile v3.ext -req -CAcreateserial -days 3650 -in CLIENT_RSA.csr -sha256 -CA CA_RSA.cer -CAkey CA_RSA.key -out CLIENT_RSA.cer.tmp
openssl x509 -text -in CLIENT_RSA.cer.tmp > CLIENT_RSA.cer

# Generate ECDSA CA, server and client end entity certificates with curve secp256r1
openssl genpkey -algorithm ec -pkeyopt ec_paramgen_curve:P-256 -pkeyopt ec_param_enc:named_curve -out CA_ECDSA_SECP256R1.key
openssl req -x509 -new -key CA_ECDSA_SECP256R1.key -days 3650 -subj "/CN=CA-ECDSA-SECP256R1" -sha256 -out CA_ECDSA_SECP256R1.cer.tmp
openssl x509 -text -in CA_ECDSA_SECP256R1.cer.tmp > CA_ECDSA_SECP256R1.cer

openssl genpkey -algorithm ec -pkeyopt ec_paramgen_curve:P-256 -pkeyopt ec_param_enc:named_curve -out SERVER_ECDSA_SECP256R1.key
openssl req -new -key SERVER_ECDSA_SECP256R1.key -subj "/CN=SERVER-ECDSA-SECP256R1" -sha256 -out SERVER_ECDSA_SECP256R1.csr
openssl x509 -extfile v3.ext -req -CAcreateserial -days 3650 -in SERVER_ECDSA_SECP256R1.csr -sha256 -CA CA_ECDSA_SECP256R1.cer -CAkey CA_ECDSA_SECP256R1.key -out SERVER_ECDSA_SECP256R1.cer.tmp
openssl x509 -text -in SERVER_ECDSA_SECP256R1.cer.tmp > SERVER_ECDSA_SECP256R1.cer

openssl genpkey -algorithm ec -pkeyopt ec_paramgen_curve:P-256 -pkeyopt ec_param_enc:named_curve -out CLIENT_ECDSA_SECP256R1.key
openssl req -new -key CLIENT_ECDSA_SECP256R1.key -subj "/CN=CLIENT-ECDSA-SECP256R1" -sha256 -out CLIENT_ECDSA_SECP256R1.csr
openssl x509 -extfile v3.ext -req -CAcreateserial -days 3650 -in CLIENT_ECDSA_SECP256R1.csr -sha256 -CA CA_ECDSA_SECP256R1.cer -CAkey CA_ECDSA_SECP256R1.key -out CLIENT_ECDSA_SECP256R1.cer.tmp
openssl x509 -text -in CLIENT_ECDSA_SECP256R1.cer.tmp > CLIENT_ECDSA_SECP256R1.cer

# Generate ECDSA CA, server and client end entity certificates with curve secp384r1
openssl genpkey -algorithm ec -pkeyopt ec_paramgen_curve:P-384 -pkeyopt ec_param_enc:named_curve -out CA_ECDSA_SECP384R1.key
openssl req -x509 -new -key CA_ECDSA_SECP384R1.key -days 3650 -subj "/CN=CA-ECDSA-SECP384R1" -sha256 -out CA_ECDSA_SECP384R1.cer.tmp
openssl x509 -text -in CA_ECDSA_SECP384R1.cer.tmp > CA_ECDSA_SECP384R1.cer

openssl genpkey -algorithm ec -pkeyopt ec_paramgen_curve:P-384 -pkeyopt ec_param_enc:named_curve -out SERVER_ECDSA_SECP384R1.key
openssl req -new -key SERVER_ECDSA_SECP384R1.key -subj "/CN=SERVER-ECDSA-SECP384R1" -sha256 -out SERVER_ECDSA_SECP384R1.csr
openssl x509 -extfile v3.ext -req -CAcreateserial -days 3650 -in SERVER_ECDSA_SECP384R1.csr -sha256 -CA CA_ECDSA_SECP384R1.cer -CAkey CA_ECDSA_SECP384R1.key -out SERVER_ECDSA_SECP384R1.cer.tmp
openssl x509 -text -in SERVER_ECDSA_SECP384R1.cer.tmp > SERVER_ECDSA_SECP384R1.cer

openssl genpkey -algorithm ec -pkeyopt ec_paramgen_curve:P-384 -pkeyopt ec_param_enc:named_curve -out CLIENT_ECDSA_SECP384R1.key
openssl req -new -key CLIENT_ECDSA_SECP384R1.key -subj "/CN=CLIENT-ECDSA-SECP384R1" -sha256 -out CLIENT_ECDSA_SECP384R1.csr
openssl x509 -extfile v3.ext -req -CAcreateserial -days 3650 -in CLIENT_ECDSA_SECP384R1.csr -sha256 -CA CA_ECDSA_SECP384R1.cer -CAkey CA_ECDSA_SECP384R1.key -out CLIENT_ECDSA_SECP384R1.cer.tmp
openssl x509 -text -in CLIENT_ECDSA_SECP384R1.cer.tmp > CLIENT_ECDSA_SECP384R1.cer

# Generate ECDSA CA, server and client end entity certificates with curve secp521r1
openssl genpkey -algorithm ec -pkeyopt ec_paramgen_curve:P-521 -pkeyopt ec_param_enc:named_curve -out CA_ECDSA_SECP521R1.key
openssl req -x509 -new -key CA_ECDSA_SECP521R1.key -days 3650 -subj "/CN=CA-ECDSA-SECP521R1" -sha256 -out CA_ECDSA_SECP521R1.cer.tmp
openssl x509 -text -in CA_ECDSA_SECP521R1.cer.tmp > CA_ECDSA_SECP521R1.cer

openssl genpkey -algorithm ec -pkeyopt ec_paramgen_curve:P-521 -pkeyopt ec_param_enc:named_curve -out SERVER_ECDSA_SECP521R1.key
openssl req -new -key SERVER_ECDSA_SECP521R1.key -subj "/CN=SERVER-ECDSA-SECP521R1" -sha256 -out SERVER_ECDSA_SECP521R1.csr
openssl x509 -extfile v3.ext -req -CAcreateserial -days 3650 -in SERVER_ECDSA_SECP521R1.csr -sha256 -CA CA_ECDSA_SECP521R1.cer -CAkey CA_ECDSA_SECP521R1.key -out SERVER_ECDSA_SECP521R1.cer.tmp
openssl x509 -text -in SERVER_ECDSA_SECP521R1.cer.tmp > SERVER_ECDSA_SECP521R1.cer

openssl genpkey -algorithm ec -pkeyopt ec_paramgen_curve:P-521 -pkeyopt ec_param_enc:named_curve -out CLIENT_ECDSA_SECP521R1.key
openssl req -new -key CLIENT_ECDSA_SECP521R1.key -subj "/CN=CLIENT-ECDSA-SECP521R1" -sha256 -out CLIENT_ECDSA_SECP521R1.csr
openssl x509 -extfile v3.ext -req -CAcreateserial -days 3650 -in CLIENT_ECDSA_SECP521R1.csr -sha256 -CA CA_ECDSA_SECP521R1.cer -CAkey CA_ECDSA_SECP521R1.key -out CLIENT_ECDSA_SECP521R1.cer.tmp
openssl x509 -text -in CLIENT_ECDSA_SECP521R1.cer.tmp > CLIENT_ECDSA_SECP521R1.cer

rm v3.ext *.srl *.csr *.tmp
