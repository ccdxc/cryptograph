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

import pytest

from cryptography.exceptions import InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.hashes import SHA1
from cryptography.hazmat.primitives.twofactor.totp import TOTP
from tests.utils import load_vectors_from_file, load_nist_vectors

vectors = load_vectors_from_file(
    "twofactor/rfc-6238.txt", load_nist_vectors)


@pytest.mark.hmac
class TestTOTP(object):

    @pytest.mark.parametrize("params", vectors)
    def test_generate(self, backend, params):
        secret = params["secret"]
        time = int(params["time"])
        mode = params["mode"]
        totp_value = params["totp"]

        algorithm = getattr(hashes, mode.decode())
        totp = TOTP(secret, 8, algorithm(), 30, backend)
        assert totp.generate(time) == totp_value

    @pytest.mark.parametrize("params", vectors)
    def test_verify(self, backend, params):
        secret = params["secret"]
        time = int(params["time"])
        mode = params["mode"]
        totp_value = params["totp"]

        algorithm = getattr(hashes, mode.decode())
        totp = TOTP(secret, 8, algorithm(), 30, backend)

        assert totp.verify(totp_value, time) is None

    def test_invalid_verify(self, backend):
            secret = b"12345678901234567890"
            time = 59

            totp = TOTP(secret, 8, SHA1(), 30, backend)

            with pytest.raises(InvalidToken):
                totp.verify(b"12345678", time)
