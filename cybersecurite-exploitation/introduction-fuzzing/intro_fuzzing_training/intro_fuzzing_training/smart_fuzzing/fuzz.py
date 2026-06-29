import subprocess
import sys
import random
import string

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


while True:

    # Reset the input each time
    inp = b"""
HAI 1.3
    VISIBLE "Lorem " "ipsum " "dolor " "sit"
KTHXBYE
"""

    inp = bytearray(inp)

    # Mutate my input
    for _ in range(random.randint(1, 10)):
        inp[random.randint(0, len(inp) - 1)] = random.randint(0, 255)

    # print(inp)

    # Execute the input to the target
    execute(inp)
