#! /bin/bash

# Generate X.509 version 3 extensions for CA
cat > ca.ext << EOF
basicConstraints=critical,CA:TRUE
subjectKeyIdentifier=hash
authorityKeyIdentifier=keyid,issuer
keyUsage=critical,keyCertSign,cRLSign,digitalSignature
EOF

# Generate X.509 version 3 extension file for EE
cat > ee.ext << EOF
basicConstraints=critical,CA:FALSE
subjectKeyIdentifier=hash
authorityKeyIdentifier=keyid,issuer
EOF

# Generate RSA CA, server and client end entity certificates
openssl genpkey -algorithm rsa -pkeyopt rsa_keygen_bits:2048 -pkeyopt rsa_keygen_pubexp:65537 -out CA_RSA.key
openssl req -new -key CA_RSA.key -subj "/CN=CA-RSA" -sha256 -out CA_RSA.csr
openssl x509 -extfile ca.ext -req -CAcreateserial -days 3650 -in CA_RSA.csr -sha256 -signkey CA_RSA.key -out CA_RSA.cer.tmp
openssl x509 -text -in CA_RSA.cer.tmp > CA_RSA.cer

openssl genpkey -algorithm rsa -pkeyopt rsa_keygen_bits:2048 -pkeyopt rsa_keygen_pubexp:65537 -out SERVER_RSA.key
openssl req -new -key SERVER_RSA.key -subj "/CN=SERVER-RSA" -sha256 -out SERVER_RSA.csr
openssl x509 -extfile ee.ext -req -CAcreateserial -days 3650 -in SERVER_RSA.csr -sha256 -CA CA_RSA.cer -CAkey CA_RSA.key -out SERVER_RSA.cer.tmp
openssl x509 -text -in SERVER_RSA.cer.tmp > SERVER_RSA.cer

openssl genpkey -algorithm rsa -pkeyopt rsa_keygen_bits:2048 -pkeyopt rsa_keygen_pubexp:65537 -out CLIENT_RSA.key
openssl req -new -key CLIENT_RSA.key -subj "/CN=CLIENT-RSA" -sha256 -out CLIENT_RSA.csr
openssl x509 -extfile ee.ext -req -CAcreateserial -days 3650 -in CLIENT_RSA.csr -sha256 -CA CA_RSA.cer -CAkey CA_RSA.key -out CLIENT_RSA.cer.tmp
openssl x509 -text -in CLIENT_RSA.cer.tmp > CLIENT_RSA.cer

# Generate ECDSA CA, server and client end entity certificates with curve secp256r1
openssl genpkey -algorithm ec -pkeyopt ec_paramgen_curve:P-256 -pkeyopt ec_param_enc:named_curve -out CA_ECDSA_SECP256R1.key
openssl req -new -key CA_ECDSA_SECP256R1.key -subj "/CN=CA-ECDSA-SECP256R1" -sha256 -out CA_ECDSA_SECP256R1.csr
openssl x509 -extfile ca.ext -req -CAcreateserial -days 3650 -in CA_ECDSA_SECP256R1.csr -sha256 -signkey CA_ECDSA_SECP256R1.key -out CA_ECDSA_SECP256R1.cer.tmp
openssl x509 -text -in CA_ECDSA_SECP256R1.cer.tmp > CA_ECDSA_SECP256R1.cer

openssl genpkey -algorithm ec -pkeyopt ec_paramgen_curve:P-256 -pkeyopt ec_param_enc:named_curve -out SERVER_ECDSA_SECP256R1.key
openssl req -new -key SERVER_ECDSA_SECP256R1.key -subj "/CN=SERVER-ECDSA-SECP256R1" -sha256 -out SERVER_ECDSA_SECP256R1.csr
openssl x509 -extfile ee.ext -req -CAcreateserial -days 3650 -in SERVER_ECDSA_SECP256R1.csr -sha256 -CA CA_ECDSA_SECP256R1.cer -CAkey CA_ECDSA_SECP256R1.key -out SERVER_ECDSA_SECP256R1.cer.tmp
openssl x509 -text -in SERVER_ECDSA_SECP256R1.cer.tmp > SERVER_ECDSA_SECP256R1.cer

openssl genpkey -algorithm ec -pkeyopt ec_paramgen_curve:P-256 -pkeyopt ec_param_enc:named_curve -out CLIENT_ECDSA_SECP256R1.key
openssl req -new -key CLIENT_ECDSA_SECP256R1.key -subj "/CN=CLIENT-ECDSA-SECP256R1" -sha256 -out CLIENT_ECDSA_SECP256R1.csr
openssl x509 -extfile ee.ext -req -CAcreateserial -days 3650 -in CLIENT_ECDSA_SECP256R1.csr -sha256 -CA CA_ECDSA_SECP256R1.cer -CAkey CA_ECDSA_SECP256R1.key -out CLIENT_ECDSA_SECP256R1.cer.tmp
openssl x509 -text -in CLIENT_ECDSA_SECP256R1.cer.tmp > CLIENT_ECDSA_SECP256R1.cer

# Generate ECDSA CA, server and client end entity certificates with curve secp384r1
openssl genpkey -algorithm ec -pkeyopt ec_paramgen_curve:P-384 -pkeyopt ec_param_enc:named_curve -out CA_ECDSA_SECP384R1.key
openssl req -new -key CA_ECDSA_SECP384R1.key -subj "/CN=CA-ECDSA-SECP384R1" -sha384 -out CA_ECDSA_SECP384R1.csr
openssl x509 -extfile ca.ext -req -CAcreateserial -days 3650 -in CA_ECDSA_SECP384R1.csr -sha384 -signkey CA_ECDSA_SECP384R1.key -out CA_ECDSA_SECP384R1.cer.tmp
openssl x509 -text -in CA_ECDSA_SECP384R1.cer.tmp > CA_ECDSA_SECP384R1.cer

openssl genpkey -algorithm ec -pkeyopt ec_paramgen_curve:P-384 -pkeyopt ec_param_enc:named_curve -out SERVER_ECDSA_SECP384R1.key
openssl req -new -key SERVER_ECDSA_SECP384R1.key -subj "/CN=SERVER-ECDSA-SECP384R1" -sha384 -out SERVER_ECDSA_SECP384R1.csr
openssl x509 -extfile ee.ext -req -CAcreateserial -days 3650 -in SERVER_ECDSA_SECP384R1.csr -sha384 -CA CA_ECDSA_SECP384R1.cer -CAkey CA_ECDSA_SECP384R1.key -out SERVER_ECDSA_SECP384R1.cer.tmp
openssl x509 -text -in SERVER_ECDSA_SECP384R1.cer.tmp > SERVER_ECDSA_SECP384R1.cer

openssl genpkey -algorithm ec -pkeyopt ec_paramgen_curve:P-384 -pkeyopt ec_param_enc:named_curve -out CLIENT_ECDSA_SECP384R1.key
openssl req -new -key CLIENT_ECDSA_SECP384R1.key -subj "/CN=CLIENT-ECDSA-SECP384R1" -sha384 -out CLIENT_ECDSA_SECP384R1.csr
openssl x509 -extfile ee.ext -req -CAcreateserial -days 3650 -in CLIENT_ECDSA_SECP384R1.csr -sha384 -CA CA_ECDSA_SECP384R1.cer -CAkey CA_ECDSA_SECP384R1.key -out CLIENT_ECDSA_SECP384R1.cer.tmp
openssl x509 -text -in CLIENT_ECDSA_SECP384R1.cer.tmp > CLIENT_ECDSA_SECP384R1.cer

# Generate ECDSA CA, server and client end entity certificates with curve secp521r1
openssl genpkey -algorithm ec -pkeyopt ec_paramgen_curve:P-521 -pkeyopt ec_param_enc:named_curve -out CA_ECDSA_SECP521R1.key
openssl req -new -key CA_ECDSA_SECP521R1.key -subj "/CN=CA-ECDSA-SECP521R1" -sha512 -out CA_ECDSA_SECP521R1.csr
openssl x509 -extfile ca.ext -req -CAcreateserial -days 3650 -in CA_ECDSA_SECP521R1.csr -sha512 -signkey CA_ECDSA_SECP521R1.key -out CA_ECDSA_SECP521R1.cer.tmp
openssl x509 -text -in CA_ECDSA_SECP521R1.cer.tmp > CA_ECDSA_SECP521R1.cer

openssl genpkey -algorithm ec -pkeyopt ec_paramgen_curve:P-521 -pkeyopt ec_param_enc:named_curve -out SERVER_ECDSA_SECP521R1.key
openssl req -new -key SERVER_ECDSA_SECP521R1.key -subj "/CN=SERVER-ECDSA-SECP521R1" -sha512 -out SERVER_ECDSA_SECP521R1.csr
openssl x509 -extfile ee.ext -req -CAcreateserial -days 3650 -in SERVER_ECDSA_SECP521R1.csr -sha512 -CA CA_ECDSA_SECP521R1.cer -CAkey CA_ECDSA_SECP521R1.key -out SERVER_ECDSA_SECP521R1.cer.tmp
openssl x509 -text -in SERVER_ECDSA_SECP521R1.cer.tmp > SERVER_ECDSA_SECP521R1.cer

openssl genpkey -algorithm ec -pkeyopt ec_paramgen_curve:P-521 -pkeyopt ec_param_enc:named_curve -out CLIENT_ECDSA_SECP521R1.key
openssl req -new -key CLIENT_ECDSA_SECP521R1.key -subj "/CN=CLIENT-ECDSA-SECP521R1" -sha512 -out CLIENT_ECDSA_SECP521R1.csr
openssl x509 -extfile ee.ext -req -CAcreateserial -days 3650 -in CLIENT_ECDSA_SECP521R1.csr -sha512 -CA CA_ECDSA_SECP521R1.cer -CAkey CA_ECDSA_SECP521R1.key -out CLIENT_ECDSA_SECP521R1.cer.tmp
openssl x509 -text -in CLIENT_ECDSA_SECP521R1.cer.tmp > CLIENT_ECDSA_SECP521R1.cer

# Generate RSASSA-PSS CA, server and client end entity certificates
openssl genpkey -algorithm rsa -pkeyopt rsa_keygen_bits:2048 -pkeyopt rsa_keygen_pubexp:65537 -out CA_PSS.key
openssl req -new -key CA_PSS.key -subj "/CN=CA-PSS" -sha256 -out CA_PSS.csr
openssl x509 -extfile ca.ext -req -CAcreateserial -days 3650 -in CA_PSS.csr -sha256 -signkey CA_PSS.key -out CA_PSS.cer.tmp
openssl x509 -text -in CA_PSS.cer.tmp > CA_PSS.cer

openssl genpkey -algorithm rsa -pkeyopt rsa_keygen_bits:2048 -pkeyopt rsa_keygen_pubexp:65537 -out SERVER_PSS.key
openssl req -new -key SERVER_PSS.key -subj "/CN=SERVER-PSS" -sha256 -out SERVER_PSS.csr
openssl x509 -extfile ee.ext -req -CAcreateserial -days 3650 -in SERVER_PSS.csr -sha256 -CA CA_PSS.cer -CAkey CA_PSS.key -out SERVER_PSS.cer.tmp
openssl x509 -text -in SERVER_PSS.cer.tmp > SERVER_PSS.cer

openssl genpkey -algorithm rsa -pkeyopt rsa_keygen_bits:2048 -pkeyopt rsa_keygen_pubexp:65537 -out CLIENT_PSS.key
openssl req -new -key CLIENT_PSS.key -subj "/CN=CLIENT-PSS" -sha256 -out CLIENT_PSS.csr
openssl x509 -extfile ee.ext -req -CAcreateserial -days 3650 -in CLIENT_PSS.csr -sha256 -CA CA_PSS.cer -CAkey CA_PSS.key -out CLIENT_PSS.cer.tmp
openssl x509 -text -in CLIENT_PSS.cer.tmp > CLIENT_PSS.cer

rm *.ext *.srl *.csr *.tmp
