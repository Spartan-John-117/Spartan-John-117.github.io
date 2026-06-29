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
    # Generate random length
    inp_len = random.randint(2, 20)

    # Generate random string
    inp = ''.join(
        random.choices(string.ascii_letters + string.digits, k=inp_len))

    # Execute the input to the target
    execute(bytearray(inp.encode('ascii')))
