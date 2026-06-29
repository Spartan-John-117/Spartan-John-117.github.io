#!/bin/bash

find $1 \
    ! -path "$1/rdoff/*" \
    ! -path "$1/travis/test/*" \
    ! -path "$1/doc/*" \
    -type f ! -executable \
    \( -name "*.c" -o -name "*.h" -o -name "*.pl" -o -name "*.ph" -o -name "*.asm" -o -name "*.mac" -o -name "*.inc" -o -name "*.py" \) | wc -l

