#!/usr/bin/env bash
git submodule update --init --recursive --depth=1

cmake -S bang-src -B bang-src/build
cmake --build bang-src/build
cmake --install bang-src/build --prefix .