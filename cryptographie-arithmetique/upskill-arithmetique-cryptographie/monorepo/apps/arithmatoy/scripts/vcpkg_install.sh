#!/bin/bash

VCPKG_VERSION=2024.07.12 # Change vcpkg version here
VCPKG_PATH=.local/vcpkg

set -e

if [ ! -e $VCPKG_PATH/.git ]; then
  git clone https://github.com/microsoft/vcpkg $VCPKG_PATH
fi

pushd $VCPKG_PATH

git fetch --all
git checkout $VCPKG_VERSION
./bootstrap-vcpkg.sh -useSystemBinaries

./vcpkg upgrade --no-dry-run

# Add dependencies here
./vcpkg install cmocka

popd
