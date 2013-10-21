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

import abc

import six

from cryptography.bindings import _default_api


class BlockCipher(object):
    def __init__(self, cipher, mode, api=None):
        super(BlockCipher, self).__init__()

        if api is None:
            api = _default_api

        self.cipher = cipher
        self.mode = mode
        self._api = api

    def encryptor(self):
        return _BlockCipherEncryptionContext(self.cipher, self.mode, self._api)

    def decryptor(self):
        return _BlockCipherDecryptionContext(self.cipher, self.mode, self._api)


class _BlockCipherContext(six.with_metaclass(abc.ABCMeta)):
    def __init__(self, cipher, mode, api):
        super(_BlockCipherContext, self).__init__()
        self.cipher = cipher
        self.mode = mode
        self._api = api

    def _check_ctx(self):
        if self._ctx is None:
            raise ValueError("Context was already finalized")


class _BlockCipherEncryptionContext(_BlockCipherContext):
    def __init__(self, cipher, mode, api):
        super(_BlockCipherEncryptionContext, self).__init__(cipher, mode, api)
        self._ctx = self._api.create_block_cipher_encrypt_context(cipher, mode)

    def update(self, data):
        self._check_ctx()
        return self._api.update_encrypt_context(self._ctx, data)

    def finalize(self):
        self._check_ctx()
        data = self._api.finalize_encrypt_context(self._ctx)
        self._ctx = None
        return data


class _BlockCipherDecryptionContext(_BlockCipherContext):
    def __init__(self, cipher, mode, api):
        super(_BlockCipherDecryptionContext, self).__init__(cipher, mode, api)
        self._ctx = self._api.create_block_cipher_decrypt_context(cipher, mode)

    def update(self, data):
        self._check_ctx()
        return self._api.update_decrypt_context(self._ctx, data)

    def finalize(self):
        self._check_ctx()
        data = self._api.finalize_decrypt_context(self._ctx)
        self._ctx = None
        return data
