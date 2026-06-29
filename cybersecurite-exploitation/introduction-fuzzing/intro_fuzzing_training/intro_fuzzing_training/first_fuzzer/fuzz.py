import subprocess
import sys


# Run one fuzz case with the provided input
# which is a byte array
def execute(inp: bytearray):

    # Write out the input to a temporary file
    tmpfn = f"tmpinput.lol"
    with open(tmpfn, "wb") as fd:
        fd.write(inp)

    # Run lci until completion
    sp = subprocess.Popen(
        ["../lci/lci", tmpfn],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL)
    ret = sp.wait()
    # print(ret)  # prints return code

    # Assert that the program ran successfully
    # crashes use negative numbers
    if ret < 0:
        print(f"CRASH - Exited with {ret}")
        sys.exit()
    elif ret != 0:
        print(f"ERR - Exited with {ret}")
    else:
        print(f"OK - Exited with {ret}")


inp = b"""
HAI 1.3
VISIBLE "Lorem " "ipsum " "dolor " "sit"
KTHXBYE
"""

inp = bytearray(inp)
execute(bytearray(inp))
