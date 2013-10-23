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

import pretend

import pytest

import six

from cryptography.bindings import _default_api

from cryptography.primitives import hashes

from .utils import generate_base_hash_test


class TestBaseHash(object):
    def test_base_hash_reject_unicode(self, backend):
        m = hashes.SHA1(backend=backend)
        with pytest.raises(TypeError):
            m.update(six.u("\u00FC"))

    def test_base_hash_hexdigest_string_type(self, backend):
        m = hashes.SHA1(backend=backend, data=b"")
        assert isinstance(m.hexdigest(), str)


class TestCopyHash(object):
    def test_copy_api_object(self):
        pretend_api = pretend.stub(copy_hash_context=lambda a: "copiedctx")
        pretend_ctx = pretend.stub()
        h = hashes.SHA1(api=pretend_api, ctx=pretend_ctx)
        assert h._api is pretend_api
        assert h.copy()._api is h._api


class TestDefaultAPISHA1(object):
    def test_default_api_creation(self):
        """
        This test assumes the presence of SHA1 in the default API.
        """
        h = hashes.SHA1()
        assert h._api is _default_api


class TestSHA1(object):
    test_SHA1 = generate_base_hash_test(
        hashes.SHA1,
        digest_size=20,
        block_size=64,
        only_if=lambda backend: backend.supports_hash(hashes.SHA1),
        skip_message="Does not support SHA1",
    )


class TestSHA224(object):
    test_SHA224 = generate_base_hash_test(
        hashes.SHA224,
        digest_size=28,
        block_size=64,
        only_if=lambda backend: backend.supports_hash(hashes.SHA224),
        skip_message="Does not support SHA224",
    )


class TestSHA256(object):
    test_SHA256 = generate_base_hash_test(
        hashes.SHA256,
        digest_size=32,
        block_size=64,
        only_if=lambda backend: backend.supports_hash(hashes.SHA256),
        skip_message="Does not support SHA256",
    )


class TestSHA384(object):
    test_SHA384 = generate_base_hash_test(
        hashes.SHA384,
        digest_size=48,
        block_size=128,
        only_if=lambda backend: backend.supports_hash(hashes.SHA384),
        skip_message="Does not support SHA384",
    )


class TestSHA512(object):
    test_SHA512 = generate_base_hash_test(
        hashes.SHA512,
        digest_size=64,
        block_size=128,
        only_if=lambda backend: backend.supports_hash(hashes.SHA512),
        skip_message="Does not support SHA512",
    )


class TestRIPEMD160(object):
    test_RIPEMD160 = generate_base_hash_test(
        hashes.RIPEMD160,
        digest_size=20,
        block_size=64,
        only_if=lambda backend: backend.supports_hash(hashes.RIPEMD160),
        skip_message="Does not support RIPEMD160",
    )


class TestWhirlpool(object):
    test_Whirlpool = generate_base_hash_test(
        hashes.Whirlpool,
        digest_size=64,
        block_size=64,
        only_if=lambda backend: backend.supports_hash(hashes.Whirlpool),
        skip_message="Does not support Whirlpool",
    )


class TestMD5(object):
    test_MD5 = generate_base_hash_test(
        hashes.MD5,
        digest_size=16,
        block_size=64,
        only_if=lambda backend: backend.supports_hash(hashes.MD5),
        skip_message="Does not support MD5",
    )
