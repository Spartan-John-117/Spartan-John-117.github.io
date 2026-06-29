#!/bin/bash

files=$(find "$1" -type f -executable)

for line in $files; do

  filetype=$(file "$line")

  if echo "$filetype" | grep -q "Python script"; then
    echo "Python $line"

  elif echo "$filetype" | grep -q "Perl script"; then
    echo "Perl $line"

  elif echo "$filetype" | grep -q "shell script"; then
    echo "Shell $line"
  
  fi

done

