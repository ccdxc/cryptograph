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

import pytest

from cryptography.hazmat.backends import _available_backends

from .utils import check_backend_support, select_backends, skip_if_empty


def pytest_generate_tests(metafunc):
    names = metafunc.config.getoption("--backend")
    selected_backends = select_backends(names, _available_backends())

    if "backend" in metafunc.fixturenames:
        filtered_backends = []
        for backend in selected_backends:
            try:
                required = metafunc.function.requires_backend_interface
            except AttributeError:
                # function does not have requires_backend_interface decorator
                filtered_backends.append(backend)
            else:
                required_interfaces = tuple(
                    mark.kwargs["interface"] for mark in required
                )
                if isinstance(backend, required_interfaces):
                    filtered_backends.append(backend)

        # If you pass an empty list to parametrize Bad Things(tm) happen
        # as of pytest 2.6.4 when the test also has a parametrize decorator
        skip_if_empty(filtered_backends, required_interfaces)

        metafunc.parametrize("backend", filtered_backends)


@pytest.mark.trylast
def pytest_runtest_setup(item):
    check_backend_support(item)


def pytest_addoption(parser):
    parser.addoption(
        "--backend", action="store", metavar="NAME",
        help="Only run tests matching the backend NAME."
    )
