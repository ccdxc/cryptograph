# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import binascii
import os
import struct
import time

import cffi

import six

from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.hmac import HMAC
from cryptography.hazmat.primitives.block import BlockCipher, ciphers, modes


class InvalidToken(Exception):
    pass


ffi = cffi.FFI()
ffi.cdef("""
bool constant_time_compare(uint8_t *, size_t, uint8_t *, size_t);
""")
lib = ffi.verify("""
#include <stdbool.h>

bool constant_time_compare(uint8_t *a, size_t len_a, uint8_t *b,
                           size_t len_b) {
    size_t i = 0;
    int result = 0;
    if (len_a != len_b) {
        return false;
    }
    for (i = 0; i < len_a; i++) {
        result |= a[i] ^ b[i];
    }
    return result == 0;
}
""")


class Fernet(object):
    def __init__(self, key, backend=None):
        super(Fernet, self).__init__()
        assert len(key) == 32
        self.signing_key = key[:16]
        self.encryption_key = key[16:]
        self.backend = backend

    def encrypt(self, data):
        current_time = int(time.time())
        iv = os.urandom(16)
        return self._encrypt_from_parts(data, current_time, iv)

    def _encrypt_from_parts(self, data, current_time, iv):
        if isinstance(data, six.text_type):
            raise TypeError(
                "Unicode-objects must be encoded before encryption"
            )

        padder = padding.PKCS7(ciphers.AES.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()
        encryptor = BlockCipher(
            ciphers.AES(self.encryption_key), modes.CBC(iv), self.backend
        ).encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        h = HMAC(self.signing_key, hashes.SHA256(), self.backend)
        h.update(b"\x80")
        h.update(struct.pack(">Q", current_time))
        h.update(iv)
        h.update(ciphertext)
        hmac = h.finalize()
        return base64.urlsafe_b64encode(
            b"\x80" + struct.pack(">Q", current_time) + iv + ciphertext + hmac
        )

    def decrypt(self, data, ttl=None, current_time=None):
        if isinstance(data, six.text_type):
            raise TypeError(
                "Unicode-objects must be encoded before decryption"
            )

        if current_time is None:
            current_time = int(time.time())

        try:
            data = base64.urlsafe_b64decode(data)
        except (TypeError, binascii.Error):
            raise InvalidToken

        assert six.indexbytes(data, 0) == 0x80
        timestamp = data[1:9]
        iv = data[9:25]
        ciphertext = data[25:-32]
        if ttl is not None:
            if struct.unpack(">Q", timestamp)[0] + ttl < current_time:
                raise InvalidToken
        h = HMAC(self.signing_key, hashes.SHA256(), self.backend)
        h.update(data[:-32])
        hmac = h.finalize()

        if not lib.constant_time_compare(hmac, len(hmac), data[-32:], 32):
            raise InvalidToken

        decryptor = BlockCipher(
            ciphers.AES(self.encryption_key), modes.CBC(iv), self.backend
        ).decryptor()
        plaintext_padded = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = padding.PKCS7(ciphers.AES.block_size).unpadder()

        unpadded = unpadder.update(plaintext_padded)
        try:
            unpadded += unpadder.finalize()
        except ValueError:
            raise InvalidToken
        return unpadded
