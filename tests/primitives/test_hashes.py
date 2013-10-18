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

from cryptography.primitives import hashes

from .utils import generate_base_hash_test


class TestSHA1(object):
    test_SHA1 = generate_base_hash_test(
        lambda api: hashes.SHA1(api=api),
        digest_size=20,
        block_size=64,
        only_if=lambda api: api.supports_hash("sha1"),
        skip_message="Does not support SHA1",
    )
