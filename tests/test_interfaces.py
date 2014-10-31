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

import abc

import pytest

import six

from cryptography.utils import InterfaceNotImplemented, verify_interface


class TestVerifyInterface(object):
    def test_verify_missing_method(self):
        @six.add_metaclass(abc.ABCMeta)
        class SimpleInterface(object):
            @abc.abstractmethod
            def method(self):
                """A simple method"""

        class NonImplementer(object):
            pass

        with pytest.raises(InterfaceNotImplemented):
            verify_interface(SimpleInterface, NonImplementer)

    def test_different_arguments(self):
        @six.add_metaclass(abc.ABCMeta)
        class SimpleInterface(object):
            @abc.abstractmethod
            def method(self, a):
                """Method with one argument"""

        class NonImplementer(object):
            def method(self):
                """Method with no arguments"""

        with pytest.raises(InterfaceNotImplemented):
            verify_interface(SimpleInterface, NonImplementer)

    def test_handles_abstract_property(self):
        @six.add_metaclass(abc.ABCMeta)
        class SimpleInterface(object):
            @abc.abstractproperty
            def property(self):
                """An abstract property"""

        class NonImplementer(object):
            @property
            def property(self):
                """A concrete property"""

        verify_interface(SimpleInterface, NonImplementer)
