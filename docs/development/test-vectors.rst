Test Vectors
============

Testing the correctness of the primitives implemented in each ``cryptography``
backend requires trusted test vectors. Where possible these vectors are obtained
from official sources such as `NIST`_ or `IETF`_ RFCs. When this is not possible
``cryptography`` has chosen to create a set of custom vectors using an official
vector file as input to verify consistency between implemented backends.

Sources
-------

Asymmetric Ciphers
~~~~~~~~~~~~~~~~~~

* RSA PKCS1 from the RSA FTP site (ftp://ftp.rsasecurity.com/pub/pkcs/pkcs-1/
  and ftp://ftp.rsa.com/pub/rsalabs/tmp/).

Hashes
~~~~~~

* MD5 from :rfc:`1321`.
* RIPEMD160 from the `RIPEMD website`_.
* SHA1 from `NIST CAVP`_.
* SHA2 (224, 256, 384, 512) from `NIST CAVP`_.
* Whirlpool from the `Whirlpool website`_.

HMAC
~~~~

* HMAC-MD5 from :rfc:`2202`.
* HMAC-SHA1 from :rfc:`2202`.
* HMAC-RIPEMD160 from :rfc:`2286`.
* HMAC-SHA2 (224, 256, 384, 512) from :rfc:`4231`.

Key Derivation Functions
~~~~~~~~~~~~~~~~~~~~~~~~

* HKDF (SHA1, SHA256) from :rfc:`5869`.
* PBKDF2 (HMAC-SHA1) from :rfc:`6070`.

Recipes
~~~~~~~

* Fernet from its `specification repository`_.

Symmetric Ciphers
~~~~~~~~~~~~~~~~~

* AES (CBC, CFB, CTR, ECB, GCM, OFB) from `NIST CAVP`_.
* 3DES (CBC, CFB, ECB, OFB) from `NIST CAVP`_.
* ARC4 from :rfc:`6229`.
* Blowfish (CBC, CFB, ECB, OFB) from `Bruce Schneier's vectors`_.
* Camellia (ECB) from NTT's `Camellia page`_ as linked by `CRYPTREC`_.
* Camellia (CBC, CFB, OFB) from `OpenSSL's test vectors`_.
* CAST5 (ECB) from :rfc:`2144`.


.. _`NIST`: http://www.nist.gov/
.. _`IETF`: https://www.ietf.org/
.. _`NIST CAVP`: http://csrc.nist.gov/groups/STM/cavp/
.. _`Bruce Schneier's vectors`: https://www.schneier.com/code/vectors.txt
.. _`Camellia page`: http://info.isl.ntt.co.jp/crypt/eng/camellia/
.. _`CRYPTREC`: http://www.cryptrec.go.jp
.. _`OpenSSL's test vectors`: https://github.com/openssl/openssl/blob/97cf1f6c2854a3a955fd7dd3a1f113deba00c9ef/crypto/evp/evptests.txt#L232
.. _`RIPEMD website`: http://homes.esat.kuleuven.be/~bosselae/ripemd160.html
.. _`Whirlpool website`: http://www.larc.usp.br/~pbarreto/WhirlpoolPage.html
.. _`Specification repository`: https://github.com/fernet/spec
