#!/bin/sh

# You need to change the program counter for each target
expected_pc="0x000000502376"

tempfile=`mktemp` && cat > ${tempfile}
result=1

trap 'rm -f ${tempfile}; exit ${result}' EXIT TERM ALRM

# Command to be tested
../lci/lci ${tempfile} 2>&1 | grep -q "pc $expected_pc"

# Check if we were killed with SIGSEGV
if test $? -eq 0; then
    result=0 # We want this input
fi

