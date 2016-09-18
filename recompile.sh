#!/bin/bash
pushd .
cd RF24
make install -B
popd
make clean && make
