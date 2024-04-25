#!/usr/bin/env bash
git submodule update --init --recursive --depth=1

cmake -S bang-src -B build
cmake --build build
cmake --install build --prefix .