import glob
import subprocess
import sys
import random
import string

import pyradamsa

# Run one fuzz case with the provided input (which is a byte array)
def execute(inp: bytearray):
    assert isinstance(inp, bytearray)
    assert type(inp) == bytearray

    # Write out the input to a temporary file
    tmpfn = f"tmpinput.lol"
    with open(tmpfn, "wb") as fd:
        fd.write(inp)

    # Run lci until completion
    sp = subprocess.Popen(["../lci/lci", tmpfn],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)
    ret = sp.wait()
    # print(ret)  # prints return code

    # Assert that the program ran successfully
    # assert ret >= 0 # crashes use negative numbers
    if ret < 0:
        print(f"CRASH - Exited with {ret}")
        # Quit because we found a bug
        sys.exit()
    elif ret != 0:
        print(f"ERR - Exited with {ret}")


rad = pyradamsa.Radamsa()

# Get a listing of all the files in the corpus
# The corpus is the set of files which we pre-seeded the fuzzers with
#  to give it valid input. These are files taht the program should be
#  able to handle parsing, that we will ultimately mutate and plice together
#  to try to find bugs!
corpus_filenames = glob.glob("corpus/*")  # glob is better b/c full paths
print(corpus_filenames)

# Load the corpus files into memory
corpus = set()  # using set to get rid of aliases/symlinks/dups
for filename in corpus_filenames:
    corpus.add(open(filename, "rb").read())

# Convert the corpus back into a list as we're done with the set for
# deduping inputs which were not unique
corpus = list(map(bytearray, corpus))  # bytearray for in-place mutations

while True:

    # Create a copy of a random existing input from the corpus
    inp = bytearray(random.choice(corpus))

    # Mutate my input by radamsa
    fuzzed = rad.fuzz(inp)

    # print(fuzzed)

    # Execute the input to the target
    execute(bytearray(fuzzed))
