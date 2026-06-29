#!/bin/bash

if [[ $1 == *.c || $1 == *.h ]]; then
	count=$(cpp -P "$1" | grep -v '^[[:space:]]*$' | grep -v '^\s*#' | grep -v '^\s*;' | wc -l)

else 
	count=$(grep -v '^[[:space:]]*$' "$1" | grep -v '^\s*#' | grep -v '^\s*;' | wc -l)
fi

echo "$count"
