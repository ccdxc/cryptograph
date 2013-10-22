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


def register(iface):
    def register_decorator(klass):
        iface.register(klass)
        return klass
    return register_decorator


class ModeWithInitializationVector(six.with_metaclass(abc.ABCMeta)):
    pass


class ModeWithNonce(six.with_metaclass(abc.ABCMeta)):
    pass


class CipherContext(six.with_metaclass(abc.ABCMeta)):
    @abc.abstractmethod
    def update(self, data):
        """
        update takes bytes and return bytes
        """

    @abc.abstractmethod
    def finalize(self):
        """
        finalize return bytes
        """
