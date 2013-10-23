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

from __future__ import absolute_import, division, print_function

from cryptography.primitives import interfaces


class BlockCipher(object):
    def __init__(self, cipher, mode, backend=None):
        super(BlockCipher, self).__init__()

        if backend is None:
            from cryptography.bindings import _default_backend as backend

        self.cipher = cipher
        self.mode = mode
        self._backend = backend

    def encryptor(self):
        return _CipherEncryptionContext(self.cipher, self.mode, self._backend)

    def decryptor(self):
        return _CipherDecryptionContext(self.cipher, self.mode, self._backend)


@interfaces.register(interfaces.CipherContext)
class _CipherEncryptionContext(object):
    def __init__(self, cipher, mode, backend):
        super(_CipherEncryptionContext, self).__init__()
        self._backend = backend
        self._ctx = self._backend.ciphers.create_encrypt_ctx(cipher, mode)

    def update(self, data):
        if self._ctx is None:
            raise ValueError("Context was already finalized")
        return self._backend.ciphers.update_encrypt_ctx(self._ctx, data)

    def finalize(self):
        if self._ctx is None:
            raise ValueError("Context was already finalized")
        data = self._backend.ciphers.finalize_encrypt_ctx(self._ctx)
        self._ctx = None
        return data


@interfaces.register(interfaces.CipherContext)
class _CipherDecryptionContext(object):
    def __init__(self, cipher, mode, backend):
        super(_CipherDecryptionContext, self).__init__()
        self._backend = backend
        self._ctx = self._backend.ciphers.create_decrypt_ctx(cipher, mode)

    def update(self, data):
        if self._ctx is None:
            raise ValueError("Context was already finalized")
        return self._backend.ciphers.update_decrypt_ctx(self._ctx, data)

    def finalize(self):
        if self._ctx is None:
            raise ValueError("Context was already finalized")
        data = self._backend.ciphers.finalize_decrypt_ctx(self._ctx)
        self._ctx = None
        return data
