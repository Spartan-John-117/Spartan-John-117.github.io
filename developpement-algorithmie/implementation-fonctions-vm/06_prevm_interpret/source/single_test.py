# To use the candidate's code, import the module Answer
from Answer import Machine, OPCODE

# Use the print(...) function to output data.

# Only the lines of code between DISPLAY_BEGIN and DISPLAY_END
# will be shown to the final user.
# ##DISPLAY_BEGIN##
m = Machine()
compute = [OPCODE.NOP]
m.load_instructions(compute)
m.execute()
print(f"VALUE: {m.a}")
assert m.a == 0
m = Machine()
m.b = 1
m.c = 1
compute = [OPCODE.ADD]
m.load_instructions(compute)
m.execute()
print(f"VALUE: {m.a}")
assert m.a == 2
m = Machine()
m.b = 7
m.c = 2
compute = [OPCODE.MUL]
m.load_instructions(compute)
m.execute()
print(f"VALUE: {m.a}")
assert m.a == 14
m = Machine()
m.a = [SUPPRIME_2600]
compute = [OPCODE.PUSHA, OPCODE.POPB]
m.load_instructions(compute)
m.execute()
print(f"VALUE: {m.b}")
assert m.b == [SUPPRIME_2600]
m = Machine()
m.b = 12
compute = [OPCODE.PUSHB, OPCODE.POPC, OPCODE.PUSHC, OPCODE.POPB, OPCODE.PUSHB, OPCODE.POPA, OPCODE.PUSHA, OPCODE.POPA]
m.load_instructions(compute)
m.execute()
print(f"VALUE: {m.a}")
assert m.a == 12
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

# ##DISPLAY_END##

