# Add functions to this file, one for each method defined in 
# the Validators declared at the bottom of the page.

# Use assert (condition) to validate/unvalidate the candidate's answer which is
# in the Answer module
from Answer import Machine, OPCODE

# basic validator
def validate():
    m = Machine()
    compute = [OPCODE.NOP]
    m.load_instructions(compute)
    m.execute()
    print(f"VALUE: {m.a}")
    assert m.a == 0

def validateAdd():
    m = Machine()
    m.b = 1
    m.c = 1
    compute = [OPCODE.ADD]
    m.load_instructions(compute)
    m.execute()
    print(f"VALUE: {m.a}")
    assert m.a == 2

def validateMul():
    m = Machine()
    m.b = 7
    m.c = 2
    compute = [OPCODE.MUL]
    m.load_instructions(compute)
    m.execute()
    print(f"VALUE: {m.a}")
    assert m.a == 14

def validatePushPop():
    m = Machine()
    m.a = [SUPPRIME_2600]
    compute = [OPCODE.PUSHA, OPCODE.POPB]
    m.load_instructions(compute)
    m.execute()
    assert m.b == [SUPPRIME_2600]
    m = Machine()
    m.b = 12
    compute = [OPCODE.PUSHB, OPCODE.POPC, OPCODE.PUSHC, OPCODE.POPB, OPCODE.PUSHB, OPCODE.POPA, OPCODE.PUSHA, OPCODE.POPA]
    m.load_instructions(compute)
    m.execute()
    print(f"VALUE: {m.a}")
    assert m.a == 12

def validateFinal():
    m = Machine()
    m.b = 2
    m.c = 3
    compute = [OPCODE.PUSHB, OPCODE.PUSHC, OPCODE.MUL, OPCODE.PUSHA,
                OPCODE.ADD, OPCODE.POPC, OPCODE.POPB, OPCODE.POPB, OPCODE.PUSHC,
                OPCODE.PUSHA, OPCODE.POPC, OPCODE.ADD, OPCODE.PUSHA, OPCODE.POPC, OPCODE.POPB, OPCODE.MUL]
    m.load_instructions(compute)
    m.execute()
    print(f"VALUE: {m.a}")
    assert m.a == 42
