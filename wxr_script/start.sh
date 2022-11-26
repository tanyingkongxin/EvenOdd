#!/bin/bash

cd ..
rm -rf build/disk_*
rm -rf build/test_data
# rm -rf build
# mkdir build
cd build
cmake ..
make 

mkdir test_data
