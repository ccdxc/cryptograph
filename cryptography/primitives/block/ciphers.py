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


class AES(object):
    name = "AES"
    block_size = 128
    key_sizes = frozenset([128, 192, 256])

    def __init__(self, key):
        super(AES, self).__init__()
        self.key = key

        # Verify that the key size matches the expected key size
        if self.key_size not in self.key_sizes:
            raise ValueError("Invalid key size ({0}) for {1}".format(
                self.key_size, self.name
            ))

    @property
    def key_size(self):
        return len(self.key) * 8


class Camellia(object):
    name = "camellia"
    block_size = 128
    key_sizes = frozenset([128, 192, 256])

    def __init__(self, key):
        super(Camellia, self).__init__()
        self.key = key

        # Verify that the key size matches the expected key size
        if self.key_size not in self.key_sizes:
            raise ValueError("Invalid key size ({0}) for {1}".format(
                self.key_size, self.name
            ))

    @property
    def key_size(self):
        return len(self.key) * 8


class TripleDES(object):
    name = "3DES"
    block_size = 64
    # TODO: is there a better way to represent the fact that the effective key
    # size is 56 bits?
    key_sizes = set([64, 128, 192])

    def __init__(self, key):
        super(TripleDES, self).__init__()
        self.key = key
