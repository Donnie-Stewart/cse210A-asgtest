!/usr/bin/env bash
export PATH=$PATH:$PWD/libexec/bats-core
make
./bin/bats tests/