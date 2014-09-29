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

import os
import platform
import subprocess
import sys
from distutils.command.build import build

import pkg_resources

from setuptools import find_packages, setup
from setuptools.command.install import install
from setuptools.command.test import test


base_dir = os.path.dirname(__file__)

about = {}
with open(os.path.join(base_dir, "cryptography", "__about__.py")) as f:
    exec(f.read(), about)


SETUPTOOLS_DEPENDENCY = "setuptools"
CFFI_DEPENDENCY = "cffi>=0.8"
SIX_DEPENDENCY = "six>=1.4.1"
VECTORS_DEPENDENCY = "cryptography_vectors=={0}".format(about['__version__'])

requirements = [
    CFFI_DEPENDENCY,
    SIX_DEPENDENCY,
    SETUPTOOLS_DEPENDENCY
]

# If you add a new dep here you probably need to add it in the tox.ini as well
test_requirements = [
    "pytest",
    "pyasn1",
    "pretend",
    "iso8601",
]

# If there's no vectors locally that probably means we are in a tarball and
# need to go and get the matching vectors package from PyPi
if not os.path.exists(os.path.join(base_dir, "vectors/setup.py")):
    test_requirements.append(VECTORS_DEPENDENCY)


def cc_is_available():
    return sys.platform == "darwin" and list(map(
        int, platform.mac_ver()[0].split("."))) >= [10, 8, 0]


backends = [
    "openssl = cryptography.hazmat.backends.openssl:backend"
]

if cc_is_available():
    backends.append(
        "commoncrypto = cryptography.hazmat.backends.commoncrypto:backend",
    )


def get_ext_modules():
    from cryptography.hazmat.bindings.commoncrypto.binding import (
        Binding as CommonCryptoBinding
    )
    from cryptography.hazmat.bindings.openssl.binding import (
        Binding as OpenSSLBinding
    )
    from cryptography.hazmat.primitives import constant_time, padding

    ext_modules = [
        OpenSSLBinding().ffi.verifier.get_extension(),
        constant_time._ffi.verifier.get_extension(),
        padding._ffi.verifier.get_extension()
    ]
    if cc_is_available():
        ext_modules.append(CommonCryptoBinding().ffi.verifier.get_extension())
    return ext_modules


class CFFIBuild(build):
    """
    This class exists, instead of just providing ``ext_modules=[...]`` directly
    in ``setup()`` because importing cryptography requires we have several
    packages installed first.

    By doing the imports here we ensure that packages listed in
    ``setup_requires`` are already installed.
    """

    def finalize_options(self):
        self.distribution.ext_modules = get_ext_modules()
        build.finalize_options(self)


class CFFIInstall(install):
    """
    As a consequence of CFFIBuild and it's late addition of ext_modules, we
    need the equivalent for the ``install`` command to install into platlib
    install-dir rather than purelib.
    """

    def finalize_options(self):
        self.distribution.ext_modules = get_ext_modules()
        install.finalize_options(self)


class PyTest(test):
    def finalize_options(self):
        test.finalize_options(self)
        self.test_args = []
        self.test_suite = True

        # This means there's a vectors/ folder with the package in here.
        # cd into it, install the vectors package and then refresh sys.path
        if VECTORS_DEPENDENCY not in test_requirements:
            subprocess.check_call(
                [sys.executable, "setup.py", "install"], cwd="vectors"
            )
            pkg_resources.get_distribution("cryptography_vectors").activate()

    def run_tests(self):
        # Import here because in module scope the eggs are not loaded.
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


def keywords_with_side_effects():
    """
    Get a dictionary with setup keywords that (can) have side effects.

    This setup.py script uses the setuptools 'setup_requires' feature because
    this is required by the cffi package to compile extension modules. The
    purpose of ``keywords_with_side_effects()`` is to avoid triggering the cffi
    build process as a result of any of the following ``setup.py`` invocations:

    - ``python setup.py --help-commands``
    - ``python setup.py --help``
    - ``python setup.py --version``
    - ``python setup.py clean``
    - ``python setup.py egg_info``

    This function is based on the `setup.py script of SciPy`_ (see also the
    discussion in `pip issue #25`_).

    .. _pip issue #25: https://github.com/pypa/pip/issues/25
    .. _setup.py script of SciPy: https://github.com/scipy/scipy/blob/master/setup.py
    """
    if len(sys.argv) >= 2 and ('--help' in sys.argv[1:] or
            sys.argv[1] in ('--help-commands', '--version', 'clean', 'egg_info')):
        return {}
    else:
        return dict(setup_requires=requirements,
                    cmdclass=dict(build=CFFIBuild,
                                  install=CFFIInstall,
                                  test=PyTest))


with open(os.path.join(base_dir, "README.rst")) as f:
    long_description = f.read()


setup(
    name=about["__title__"],
    version=about["__version__"],

    description=about["__summary__"],
    long_description=long_description,
    license=about["__license__"],
    url=about["__uri__"],

    author=about["__author__"],
    author_email=about["__email__"],

    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Security :: Cryptography",
    ],

    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,

    install_requires=requirements,
    tests_require=test_requirements,

    # for cffi
    zip_safe=False,
    ext_package="cryptography",
    entry_points={
        "cryptography.backends": backends,
    },
    **keywords_with_side_effects()
)
