#!/bin/bash

input="$1"

if [[ $input =~ command\ ([0-9]+)$ ]]; then
    	echo "INT ${BASH_REMATCH[1]}"
elif [[ $input =~ command\ ([a-z]+)$ ]]; then
	echo "LOWER ${BASH_REMATCH[1]}"
elif [[ $input =~ command\ ([A-Z][a-z]+)$ ]]; then
	echo "IDENT ${BASH_REMATCH[1]}"
elif [[ $input =~ command\ ([_][a-z0-9]+)$ ]]; then
	echo "IDENT ${BASH_REMATCH[1]}"
elif [[ $input =~ command\ [\"]([A-Za-z \?]+)[\"]$ ]]; then
	echo "STR ${BASH_REMATCH[1]}"
elif [[ $input =~ command\ ([\"])([\\])\"([A-Za-z ]+)([\\])([\"]+)$ ]]; then
    	echo "STR ${BASH_REMATCH[1]}${BASH_REMATCH[3]}${BASH_REMATCH[1]}"
else 
	echo "Unknown"
fi


