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


class CipherBackend(six.with_metaclass(abc.ABCMeta)):
    @abc.abstractmethod
    def cipher_supported(self, cipher, mode):
        """
        """

    @abc.abstractmethod
    def register_cipher_adapter(self, cipher, mode):
        """
        """

    @abc.abstractmethod
    def create_symmetric_encryption_ctx(self, cipher, mode):
        """
        """

    @abc.abstractmethod
    def create_symmetric_decryption_ctx(self, cipher, mode):
        """
        """


class HashBackend(six.with_metaclass(abc.ABCMeta)):
    @abc.abstractmethod
    def hash_supported(self, algorithm):
        """
        """

    @abc.abstractmethod
    def create_hash_ctx(self, algorithm):
        """
        """


class HMACBackend(six.with_metaclass(abc.ABCMeta)):
    @abc.abstractmethod
    def create_hmac_ctx(self, key, algorithm):
        """
        """
