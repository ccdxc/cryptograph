#!/bin/bash

set -e
set -x

if [[ "$(uname -s)" == "Darwin" ]]; then
    eval "$(pyenv init -)"
    if [[ "${OPENSSL}" != "0.9.8" ]]; then
        # travis has 1.0.1e installed via homebrew on OS X by default
        # so set our flags to use that
        export ARCHFLAGS="-arch x86_64"
        export LDFLAGS="-L/usr/local/opt/openssl/lib"
        export CFLAGS="-I/usr/local/opt/openssl/include"
    fi
fi
source ~/.venv/bin/activate
tox -e $TOX_ENV
