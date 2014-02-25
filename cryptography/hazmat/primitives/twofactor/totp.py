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

import math

from cryptography.exceptions import InvalidToken
from cryptography.hazmat.primitives import constant_time
from cryptography.hazmat.primitives.twofactor.hotp import HOTP


class TOTP(object):
    def __init__(self, key, length, algorithm, time_step, backend):

        self._time_step = time_step
        self.hotp = HOTP(key, length, algorithm, backend)

    def generate(self, time):
        counter = int(math.floor(time/self._time_step))
        return self.hotp.generate(counter)

    def verify(self, totp, time):
        if not constant_time.bytes_eq(self.generate(time), totp):
            raise InvalidToken("Supplied HOTP value does not match")
