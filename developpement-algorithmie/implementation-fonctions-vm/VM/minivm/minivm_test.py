import unittest
from minivm import *
from minivm_insn import instructions

class TestMachine(unittest.TestCase):

    def test_add(self):
        m = Machine()
        m.b = 1
        m.c = 1
        print(f"m.b = {m.b} m.c = {m.c}")
        instructions[OPCODE.ADD_ABC][1](m)
        print(f"m.a = {m.a}")
        self.assertTrue(m.a == 2)
        m = Machine()
        m.b = 1
        m.c = 8
        print(f"m.b = {m.b} m.c = {m.c}")
        instructions[OPCODE.ADD_ACB][1](m)
        print(f"m.a = {m.a}")
        self.assertTrue(m.a == 9)
        m = Machine()
        m.a = 1
        m.c = 17
        print(f"m.a = {m.a} m.c = {m.c}")
        instructions[OPCODE.ADD_BAC][1](m)
        print(f"m.b = {m.b}")
        self.assertTrue(m.b == 18)
        m = Machine()
        m.a = 1
        m.c = 5
        print(f"m.a = {m.a} m.c = {m.c}")
        instructions[OPCODE.ADD_BCA][1](m)
        print(f"m.b = {m.b}")
        self.assertTrue(m.b == 6)
        m = Machine()
        m.a = 1
        m.b = 9
        print(f"m.a = {m.a} m.b = {m.b}")
        instructions[OPCODE.ADD_CAB][1](m)
        print(f"m.c = {m.c}")
        self.assertTrue(m.c == 10)
        m = Machine()
        m.a = 1
        m.b = 4
        print(f"m.a = {m.a} m.b = {m.b}")
        instructions[OPCODE.ADD_CBA][1](m)
        print(f"m.c = {m.c}")
        self.assertTrue(m.c == 5)

    def test_sub(self):
        m = Machine()
        m.b = 10
        m.c = 1
        print(f"m.b = {m.b} m.c = {m.c}")
        instructions[OPCODE.SUB_ABC][1](m)
        print(f"m.a = {m.a}")
        self.assertTrue(m.a == 9)
        # TODO vous pouvez compléter les tests si vous le souhaitez.
        m = Machine()
        m.c = 100
        m.b = 1
        print(f"m.c = {m.c} m.b = {m.b}")
        instructions[OPCODE.SUB_ACB][1](m)
        print(f"m.a = {m.a}")
        self.assertTrue(m.a == 99)
        m = Machine()
        m.a = 1586
        m.c = 1
        print(f"m.a = {m.a} m.c = {m.c}")
        instructions[OPCODE.SUB_BAC][1](m)
        print(f"m.b = {m.b}")
        self.assertTrue(m.b == 1585)
        m = Machine()
        m.c = 17856
        m.a = 1
        print(f"m.c = {m.c} m.a = {m.a}")
        instructions[OPCODE.SUB_BCA][1](m)
        print(f"m.b = {m.b}")
        self.assertTrue(m.b == 17855)
        m = Machine()
        m.a = 15
        m.b = 1
        print(f"m.a = {m.a} m.b = {m.b}")
        instructions[OPCODE.SUB_CAB][1](m)
        print(f"m.c = {m.c}")
        self.assertTrue(m.c == 14)
        m = Machine()
        m.b = 19
        m.a = 1
        print(f"m.b = {m.b} m.a = {m.a}")
        instructions[OPCODE.SUB_CBA][1](m)
        print(f"m.c = {m.c}")
        self.assertTrue(m.c == 18)

    def test_mul(self):
        m = Machine()
        m.b = 2
        m.c = 2
        print(f"m.b = {m.b} m.c = {m.c}")
        instructions[OPCODE.MUL_ABC][1](m)
        print(f"m.a = {m.a}")
        self.assertTrue(m.a == 4)
        # TODO vous pouvez compléter les tests si vous le souhaitez.
        m = Machine()
        m.c = 18
        m.b = 1
        print(f"m.c = {m.c} m.b = {m.b}")
        instructions[OPCODE.MUL_ACB][1](m)
        print(f"m.a = {m.a}")
        self.assertTrue(m.a == 18)
        m = Machine()
        m.a = 2
        m.c = 18
        print(f"m.a = {m.a} m.c = {m.c}")
        instructions[OPCODE.MUL_BAC][1](m)
        print(f"m.b = {m.b}")
        self.assertTrue(m.b == 36)
        m = Machine()
        m.c = 11
        m.a = 13
        print(f"m.c = {m.c} m.a = {m.a}")
        instructions[OPCODE.MUL_BCA][1](m)
        print(f"m.b = {m.b}")
        self.assertTrue(m.b == 143)
        m = Machine()
        m.a = 19
        m.b = 5
        print(f"m.a = {m.a} m.b = {m.b}")
        instructions[OPCODE.MUL_CAB][1](m)
        print(f"m.c = {m.c}")
        self.assertTrue(m.c == 95)
        m = Machine()
        m.b = 6
        m.a = 5
        print(f"m.b = {m.b} m.a = {m.a}")
        instructions[OPCODE.MUL_CBA][1](m)
        print(f"m.c = {m.c}")
        self.assertTrue(m.c == 30)

    def test_div(self):
        m = Machine()
        m.b = 8
        m.c = 2
        print(f"m.b = {m.b} m.c = {m.c}")
        instructions[OPCODE.DIV_ABC][1](m)
        print(f"m.a = {m.a}")
        self.assertTrue(m.a == 4)
        # TODO vous pouvez compléter les tests si vous le souhaitez.
        m = Machine()
        m.c = 1258
        m.b = 10
        print(f"m.c = {m.c} m.b = {m.b}")
        instructions[OPCODE.DIV_ACB][1](m)
        print(f"m.a = {m.a}")
        self.assertTrue(m.a == 125)
        m = Machine()
        m.a = 169
        m.c = 4
        print(f"m.a = {m.a} m.c = {m.c}")
        instructions[OPCODE.DIV_BAC][1](m)
        print(f"m.b = {m.b}")
        self.assertTrue(m.b == 42)
        m = Machine()
        m.c = 5896
        m.a = 564
        print(f"m.c = {m.c} m.a = {m.a}")
        instructions[OPCODE.DIV_BCA][1](m)
        print(f"m.b = {m.b}")
        self.assertTrue(m.b == 10)
        m = Machine()
        m.a = 97
        m.b = 9
        print(f"m.a = {m.a} m.b = {m.b}")
        instructions[OPCODE.DIV_CAB][1](m)
        print(f"m.c = {m.c}")
        self.assertTrue(m.c == 10)
        m = Machine()
        m.b = 5784
        m.a = 56
        print(f"m.b = {m.b} m.a = {m.a}")
        instructions[OPCODE.DIV_CBA][1](m)
        print(f"m.c = {m.c}")
        self.assertTrue(m.c == 103)

    def test_mod(self):
        m = Machine()
        m.b = 8
        m.c = 6
        print(f"m.b = {m.b} m.c = {m.c}")
        instructions[OPCODE.MOD_ABC][1](m)
        print(f"m.a = {m.a}")
        self.assertTrue(m.a == 2)
        # TODO vous pouvez compléter les tests si vous le souhaitez.
        m = Machine()
        m.c = 1258
        m.b = 10
        print(f"m.c = {m.c} m.b = {m.b}")
        instructions[OPCODE.MOD_ACB][1](m)
        print(f"m.a = {m.a}")
        self.assertTrue(m.a == 8)
        m = Machine()
        m.a = 169
        m.c = 4
        print(f"m.a = {m.a} m.c = {m.c}")
        instructions[OPCODE.MOD_BAC][1](m)
        print(f"m.b = {m.b}")
        self.assertTrue(m.b == 1)
        m = Machine()
        m.c = 5896
        m.a = 564
        print(f"m.c = {m.c} m.a = {m.a}")
        instructions[OPCODE.MOD_BCA][1](m)
        print(f"m.b = {m.b}")
        self.assertTrue(m.b == 256)
        m = Machine()
        m.a = 97
        m.b = 9
        print(f"m.a = {m.a} m.b = {m.b}")
        instructions[OPCODE.MOD_CAB][1](m)
        print(f"m.c = {m.c}")
        self.assertTrue(m.c == 7)
        m = Machine()
        m.b = 5784
        m.a = 56
        print(f"m.b = {m.b} m.a = {m.a}")
        instructions[OPCODE.MOD_CBA][1](m)
        print(f"m.c = {m.c}")
        self.assertTrue(m.c == 16)

    def test_and(self):
        m = Machine()
        m.b = 0b0011
        m.c = 0b0110
        print(f"m.b = {m.b:#06b}, m.c = {m.c:#06b}")
        instructions[OPCODE.AND_ABC][1](m)
        print(f"m.a = {m.a:#06b}")
        self.assertTrue(m.a == 0b0010)
        # TODO vous pouvez compléter les tests si vous le souhaitez.
        m = Machine()
        m.c = 0b0000
        m.b = 0b0001
        print(f"m.c = {m.c:#06b}, m.b = {m.b:#06b}")
        instructions[OPCODE.AND_ACB][1](m)
        print(f"m.a = {m.a:#06b}")
        self.assertTrue(m.a == 0b0000)
        m = Machine()
        m.a = 0b0111
        m.c = 0b0100
        print(f"m.a = {m.a:#06b}, m.c = {m.c:#06b}")
        instructions[OPCODE.AND_BAC][1](m)
        print(f"m.b = {m.b:#06b}")
        self.assertTrue(m.b == 0b0100)
        m = Machine()
        m.c = 0b1111
        m.a = 0b1111
        print(f"m.c = {m.c:#06b}, m.a = {m.a:#06b}")
        instructions[OPCODE.AND_BCA][1](m)
        print(f"m.b = {m.b:#06b}")
        self.assertTrue(m.b == 0b1111)
        m = Machine()
        m.a = 0b1010
        m.b = 0b0110
        print(f"m.a = {m.a:#06b}, m.b = {m.b:#06b}")
        instructions[OPCODE.AND_CAB][1](m)
        print(f"m.c = {m.c:#06b}")
        self.assertTrue(m.c == 0b0010)
        m = Machine()
        m.b = 0b1000
        m.a = 0b1000
        print(f"m.b = {m.b:#06b}, m.a = {m.a:#06b}")
        instructions[OPCODE.AND_CBA][1](m)
        print(f"m.c = {m.c:#06b}")
        self.assertTrue(m.c == 0b1000)

    def test_or(self):
        m = Machine()
        m.b = 0b0011
        m.c = 0b0110
        instructions[OPCODE.OR_ABC][1](m)
        self.assertTrue(m.a == 0b0111)
        # TODO vous pouvez compléter les tests si vous le souhaitez.
        m = Machine()
        m.c = 0b0000
        m.b = 0b0001
        print(f"m.c = {m.c:#06b}, m.b = {m.b:#06b}")
        instructions[OPCODE.OR_ACB][1](m)
        print(f"m.a = {m.a:#06b}")
        self.assertTrue(m.a == 0b0001)
        m = Machine()
        m.a = 0b0111
        m.c = 0b0100
        print(f"m.a = {m.a:#06b}, m.c = {m.c:#06b}")
        instructions[OPCODE.OR_BAC][1](m)
        print(f"m.b = {m.b:#06b}")
        self.assertTrue(m.b == 0b0111)
        m = Machine()
        m.c = 0b1111
        m.a = 0b1111
        print(f"m.c = {m.c:#06b}, m.a = {m.a:#06b}")
        instructions[OPCODE.OR_BCA][1](m)
        print(f"m.b = {m.b:#06b}")
        self.assertTrue(m.b == 0b1111)
        m = Machine()
        m.a = 0b1010
        m.b = 0b0110
        print(f"m.a = {m.a:#06b}, m.b = {m.b:#06b}")
        instructions[OPCODE.OR_CAB][1](m)
        print(f"m.c = {m.c:#06b}")
        self.assertTrue(m.c == 0b1110)
        m = Machine()
        m.b = 0b1000
        m.a = 0b1000
        print(f"m.b = {m.b:#06b}, m.a = {m.a:#06b}")
        instructions[OPCODE.OR_CBA][1](m)
        print(f"m.c = {m.c:#06b}")
        self.assertTrue(m.c == 0b1000)

    def test_xor(self):
        m = Machine()
        m.b = 0b0011
        m.c = 0b0110
        instructions[OPCODE.XOR_ABC][1](m)
        self.assertTrue(m.a == 0b0101)
        # TODO vous pouvez compléter les tests si vous le souhaitez.
        m = Machine()
        m.c = 0b0000
        m.b = 0b0001
        print(f"m.c = {m.c:#06b}, m.b = {m.b:#06b}")
        instructions[OPCODE.XOR_ACB][1](m)
        print(f"m.a = {m.a:#06b}")
        self.assertTrue(m.a == 0b0001)
        m = Machine()
        m.a = 0b0111
        m.c = 0b0100
        print(f"m.a = {m.a:#06b}, m.c = {m.c:#06b}")
        instructions[OPCODE.XOR_BAC][1](m)
        print(f"m.b = {m.b:#06b}")
        self.assertTrue(m.b == 0b0011)
        m = Machine()
        m.c = 0b1111
        m.a = 0b1111
        print(f"m.c = {m.c:#06b}, m.a = {m.a:#06b}")
        instructions[OPCODE.XOR_BCA][1](m)
        print(f"m.b = {m.b:#06b}")
        self.assertTrue(m.b == 0b0000)
        m = Machine()
        m.a = 0b1010
        m.b = 0b0110
        print(f"m.a = {m.a:#06b}, m.b = {m.b:#06b}")
        instructions[OPCODE.XOR_CAB][1](m)
        print(f"m.c = {m.c:#06b}")
        self.assertTrue(m.c == 0b1100)
        m = Machine()
        m.b = 0b1000
        m.a = 0b1000
        print(f"m.b = {m.b:#06b}, m.a = {m.a:#06b}")
        instructions[OPCODE.XOR_CBA][1](m)
        print(f"m.c = {m.c:#06b}")
        self.assertTrue(m.c == 0b0000)

    def test_cmp(self):
        m = Machine()
        m.b = 2
        m.c = 1
        print(f"m.b = {m.b} m.c = {m.c}")
        instructions[OPCODE.CMP_BC][1](m)
        print(f"m.flags = {m.flags}")
        self.assertTrue(m.flags > 0)
        m.b = 1
        m.c = 2
        print(f"m.b = {m.b} m.c = {m.c}")
        instructions[OPCODE.CMP_BC][1](m)
        print(f"m.flags = {m.flags}")
        self.assertTrue(m.flags < 0)
        m.b = 1
        m.c = 1
        print(f"m.b = {m.b} m.c = {m.c}")
        instructions[OPCODE.CMP_BC][1](m)
        print(f"m.flags = {m.flags}")
        self.assertTrue(m.flags == 0)

    def test_mov(self):
        m = Machine()
        m.b = [SUPPRIME_2600]
        print(f"m.a = {m.a} m.b = {m.b}")
        instructions[OPCODE.MOV_AB][1](m)
        print(f"m.a = {m.a}")
        self.assertTrue(m.a == [SUPPRIME_2600])
        m = Machine()
        m.c = [SUPPRIME_2600]
        print(f"m.a = {m.a} m.c = {m.c}")
        instructions[OPCODE.MOV_AC][1](m)
        print(f"m.a = {m.a}")
        self.assertTrue(m.a == [SUPPRIME_2600])
        m = Machine()
        m.a = [SUPPRIME_2600]
        print(f"m.b = {m.b} m.a = {m.a}")
        instructions[OPCODE.MOV_BA][1](m)
        print(f"m.b = {m.b}")
        self.assertTrue(m.b == [SUPPRIME_2600])
        m = Machine()
        m.c = [SUPPRIME_2600]
        print(f"m.b = {m.b} m.c= {m.c}")
        instructions[OPCODE.MOV_BC][1](m)
        print(f"m.b = {m.b}")
        self.assertTrue(m.b == [SUPPRIME_2600])
        m = Machine()
        m.a = [SUPPRIME_2600]
        print(f"m.c = {m.c} m.a = {m.a}")
        instructions[OPCODE.MOV_CA][1](m)
        print(f"m.c = {m.c}")
        self.assertTrue(m.c == [SUPPRIME_2600])
        m = Machine()
        m.b = [SUPPRIME_2600]
        print(f"m.c = {m.c} m.b = {m.b}")
        instructions[OPCODE.MOV_CB][1](m)
        print(f"m.c = {m.c}")
        self.assertTrue(m.c == [SUPPRIME_2600])

    def test_pusha(self):
        m = Machine()
        m.a = [SUPPRIME_2600]
        print(f"m.sp = {m.sp}")
        instructions[OPCODE.PUSHA][1](m)
        print(f"m.sp = {m.sp}")
        print(f"m.a = {m.a}")
        self.assertTrue(m.pop() == [SUPPRIME_2600])

    def test_pushb(self):
        m = Machine()
        m.b = [SUPPRIME_2600]
        print(f"m.sp = {m.sp}")
        instructions[OPCODE.PUSHB][1](m)
        print(f"m.sp = {m.sp}")
        print(f"m.a = {m.b}")
        self.assertTrue(m.pop() == [SUPPRIME_2600])

    def test_pushc(self):
        m = Machine()
        m.c = [SUPPRIME_2600]
        print(f"m.sp = {m.sp}")
        instructions[OPCODE.PUSHC][1](m)
        print(f"m.sp = {m.sp}")
        print(f"m.c = {m.c}")
        self.assertTrue(m.pop() == [SUPPRIME_2600])

    def test_popa(self):
        m = Machine()
        m.push([SUPPRIME_2600])
        print(f"m.sp = {m.sp}")
        print(f"m.a = {m.a}")
        instructions[OPCODE.POPA][1](m)
        print(f"m.sp = {m.sp}")
        print(f"m.a = {m.a}")
        self.assertTrue(m.a == [SUPPRIME_2600])

    def test_popb(self):
        m = Machine()
        m.push([SUPPRIME_2600])
        print(f"m.sp = {m.sp}")
        print(f"m.b = {m.b}")
        instructions[OPCODE.POPB][1](m)
        print(f"m.sp = {m.sp}")
        print(f"m.b = {m.b}")
        self.assertTrue(m.b == [SUPPRIME_2600])

    def test_popc(self):
        m = Machine()
        m.push([SUPPRIME_2600])
        print(f"m.sp = {m.sp}")
        print(f"m.c = {m.c}")
        instructions[OPCODE.POPC][1](m)
        print(f"m.sp = {m.sp}")
        print(f"m.c = {m.c}")
        self.assertTrue(m.c == [SUPPRIME_2600])

    def test_loadint(self):
        m = Machine()
        print(f"m.a = {m.a}")
        instructions[OPCODE.LOADINTA][1](m, [SUPPRIME_2600])
        print(f"m.a = {m.a}")
        self.assertTrue(m.a == [SUPPRIME_2600])

    def test_loadstr(self):
        m = Machine()
        print(f"m.a = {m.a}")
        instructions[OPCODE.LOADSTRA][1](m, "test")
        print(f"m.a = {m.a}")
        self.assertTrue(m.a == "test")

# TODO Vous aurez peut-être besoin de vous écrires des tests pour lenstr?.

    def test_lenstr(self):
        m = Machine()
        m.b = "bonjourceciestuntest"
        print(f"m.a = {m.a}")
        print(f"m.b = {m.b}")
        instructions[OPCODE.LENSTR_AB][1](m)
        print(f"m.a = {m.a}")
        self.assertTrue(m.a == 20)

    def test_castint(self):
        m = Machine()
        m.a = "12"
        instructions[OPCODE.CASTINTA][1](m)
        self.assertTrue(m.a == 12)

    def test_caststr(self):
        m = Machine()
        m.a = 12
        instructions[OPCODE.CASTSTRA][1](m)
        self.assertTrue(m.a == "12")

    def test_jmp(self):
        m = Machine()
        instructions[OPCODE.JMP][1](m, 12)
        print(f"m.ip = {m.ip}")
        self.assertTrue(m.ip == 12)
        m = Machine()
        instructions[OPCODE.JMP][1](m, 85)
        print(f"m.ip = {m.ip}")
        self.assertTrue(m.ip == 85)
        m = Machine()
        instructions[OPCODE.JMP][1](m, 5)
        print(f"m.ip = {m.ip}")
        self.assertTrue(m.ip == 5)
        m = Machine()
        instructions[OPCODE.JMP][1](m, 65)
        print(f"m.ip = {m.ip}")
        self.assertTrue(m.ip == 65)

    def test_je(self):
        m = Machine()
        m.b = 1
        m.c = 1
        print(f"m.b = {m.b} m.c = {m.c}")
        instructions[OPCODE.CMP_BC][1](m)
        print(f"m.flags = {m.flags}")
        instructions[OPCODE.JE][1](m, 12)
        print(f"m.ip = {m.ip}")
        self.assertTrue(m.ip == 12)
        m.b = 2
        m.ip = 0
        print(f"m.b = {m.b} m.ip = {m.ip}")
        instructions[OPCODE.CMP_BC][1](m)
        print(f"m.flags = {m.flags}")
        instructions[OPCODE.JE][1](m, 12)
        print(f"m.ip = {m.ip}")
        self.assertTrue(m.ip == 0)

    def test_jne(self):
        m = Machine()
        m.b = 1
        m.c = 1
        print(f"m.b = {m.b} m.c = {m.c}")
        instructions[OPCODE.CMP_BC][1](m)
        print(f"m.flags = {m.flags}")
        instructions[OPCODE.JNE][1](m, 12)
        print(f"m.ip = {m.ip}")
        self.assertTrue(m.ip == 0)
        m.b = 2
        m.ip = 0
        print(f"m.b = {m.b} m.ip = {m.ip}")
        instructions[OPCODE.CMP_BC][1](m)
        print(f"m.flags = {m.flags}")
        instructions[OPCODE.JNE][1](m, 12)
        print(f"m.ip = {m.ip}")
        self.assertTrue(m.ip == 12)

    def test_jlt(self):
        m = Machine()
        m.b = 1
        m.c = 2
        print(f"m.b = {m.b} m.c = {m.c}")
        instructions[OPCODE.CMP_BC][1](m)
        print(f"m.flags = {m.flags}")
        instructions[OPCODE.JLT][1](m, 12)
        print(f"m.ip = {m.ip}")
        self.assertTrue(m.ip == 12)
        m.b = 2
        m.ip = 0
        print(f"m.b = {m.b} m.ip = {m.ip}")
        instructions[OPCODE.CMP_BC][1](m)
        print(f"m.flags = {m.flags}")
        instructions[OPCODE.JLT][1](m, 12)
        print(f"m.ip = {m.ip}")
        self.assertTrue(m.ip == 0)

    def test_jle(self):
        m = Machine()
        m.b = 1
        m.c = 2
        print(f"m.b = {m.b} m.c = {m.c}")
        instructions[OPCODE.CMP_BC][1](m)
        print(f"m.flags = {m.flags}")
        instructions[OPCODE.JLE][1](m, 12)
        print(f"m.ip = {m.ip}")
        self.assertTrue(m.ip == 12)
        m.b = 2
        m.ip = 0
        print(f"m.b = {m.b} m.ip = {m.ip}")
        instructions[OPCODE.CMP_BC][1](m)
        print(f"m.flags = {m.flags}")
        instructions[OPCODE.JLE][1](m, 12)
        print(f"m.ip = {m.ip}")
        self.assertTrue(m.ip == 12)
        m.b = 3
        m.ip = 0
        instructions[OPCODE.CMP_BC][1](m)
        print(f"m.flags = {m.flags}")
        instructions[OPCODE.JLE][1](m, 12)
        print(f"m.ip = {m.ip}")
        self.assertTrue(m.ip == 0)

    def test_jgt(self):
        m = Machine()
        m.b = 2
        m.c = 1
        print(f"m.b = {m.b} m.c = {m.c}")
        instructions[OPCODE.CMP_BC][1](m)
        print(f"m.flags = {m.flags}")
        instructions[OPCODE.JGT][1](m, 12)
        print(f"m.ip = {m.ip}")
        self.assertTrue(m.ip == 12)
        m.b = 1
        m.ip = 0
        print(f"m.b = {m.b} m.ip = {m.ip}")
        instructions[OPCODE.CMP_BC][1](m)
        print(f"m.flags = {m.flags}")
        instructions[OPCODE.JGT][1](m, 12)
        print(f"m.ip = {m.ip}")
        self.assertTrue(m.ip == 0)

    def test_jge(self):
        m = Machine()
        m.b = 2
        m.c = 1
        print(f"m.b = {m.b} m.c = {m.c}")
        instructions[OPCODE.CMP_BC][1](m)
        print(f"m.flags = {m.flags}")
        instructions[OPCODE.JGE][1](m, 12)
        print(f"m.ip = {m.ip}")
        self.assertTrue(m.ip == 12)
        m.b = 1
        m.ip = 0
        print(f"m.b = {m.b} m.ip = {m.ip}")
        instructions[OPCODE.CMP_BC][1](m)
        print(f"m.flags = {m.flags}")
        instructions[OPCODE.JGE][1](m, 12)
        print(f"m.ip = {m.ip}")
        self.assertTrue(m.ip == 12)
        m.b = 0
        m.ip = 0
        print(f"m.b = {m.b} m.ip = {m.ip}")
        instructions[OPCODE.CMP_BC][1](m)
        print(f"m.flags = {m.flags}")
        instructions[OPCODE.JGE][1](m, 12)
        print(f"m.ip = {m.ip}")
        self.assertTrue(m.ip == 0)

    def test_call(self):
        m = Machine()
        m.ip = 42
        print(f"m.ip = {m.ip}")
        instructions[OPCODE.CALL][1](m, -42)
        print(f"m.ip = {m.ip}")
        self.assertTrue(m.ip == 0)
        self.assertTrue(m.pop() == 42)

    def test_ret(self):
        m = Machine()
        m.push(42)
        print(f"m.ip = {m.ip}")
        instructions[OPCODE.RET][1](m)
        print(f"m.ip = {m.ip}")
        self.assertTrue(m.ip == 42)

    def test_enterleave(self):
        m = Machine()
        m.log = print
        ref_sp = m.sp
        m.enter(2)
        m.a = [SUPPRIME_2600]
        m.b = 42
        m.store("a", 0)
        m.store("b", 1)
        m.leave(2)
        print("ref_sp =", ref_sp)
        print("m.sp =", m.sp)
        self.assertTrue(ref_sp == m.sp)
        m.enter(2)
        with self.assertRaises(StackFrameError):
            m.store("a", 2)
        # TODO vous pouvez compléter les tests si vous le souhaitez.

    def test_getat(self):
        m = Machine()
        m.b = "test"
        m.c = 1
        instructions[OPCODE.GETAT_ABC][1](m)
        self.assertTrue(m.a == 'e')

    def test_setat(self):
        m = Machine()
        m.a = ""
        m.b = 0
        m.c = "t"
        instructions[OPCODE.SETAT_ABC][1](m)
        self.assertTrue(m.a == 't')
        self.assertTrue(len(m.a) == 1)
        m.a = ""
        m.b = 5
        m.c = "t"
        instructions[OPCODE.SETAT_ABC][1](m)
        self.assertTrue(m.a == '     t')
        self.assertTrue(len(m.a) == 6)

# TODO Vous aurez peut-être besoin de vous écrires des tests pour ord et chr?.

    def test_ord(self):
        m = Machine()
        m.a = "a"
        instructions[OPCODE.ORDA][1](m)
        self.assertTrue(m.a == 97)
        m = Machine()
        m.a = "ab"
        with self.assertRaises(InstructionFault) as context:
            instructions[OPCODE.ORDA][1](m)  # Devrait lever une InstructionFault
        self.assertEqual(str(context.exception), "valeur ab non prise en charge")

    def test_chr(self):
        m = Machine()
        m.a = 97
        instructions[OPCODE.CHRA][1](m)
        self.assertTrue(m.a == "a")
        m = Machine()
        m.a = "ab"
        with self.assertRaises(InstructionFault) as context:
            instructions[OPCODE.ORDA][1](m)  # Devrait lever une InstructionFault
        self.assertEqual(str(context.exception), "valeur ab non prise en charge")

    def test_loadexec(self):
        from minivm_asm import AsmParser, assemble
        from minivm_encode import encode_opcodes
        code_asm = """
            loadinta [SUPPRIME_2600]
            syscall 0
        """
        asm = AsmParser(code_asm)
        print("asm =", asm)
        ast = asm.parse()
        print("ast =",ast)
        chunks = assemble(ast)
        print("chunks =", chunks)
        compiled = encode_opcodes(chunks)
        print("compiled =", compiled)
        m = Machine()
        print("machine lancée")
        m.load(compiled)
        print("m.load avec succés")
        print("m.a =", m.a)
        #print("Liste d'opcodes disponibles")
        """for opcode in OPCODE:
            print(f"{opcode.name}: {opcode.value}")"""
        m.execute()
        self.assertTrue(m.a == [SUPPRIME_2600])

if __name__ == '__main__':
    unittest.main()