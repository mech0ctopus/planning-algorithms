#!/bin/bash

echo "Running C++ Tests."
cd modules/cpp/build
./TestPrimitives

echo "Running Python Tests."
cd ../../python3
nosetests3 .
