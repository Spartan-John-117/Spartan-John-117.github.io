# import les types principaux permettant le décodage des instructions
from minivm import OPCODE, TypeOfChunk
# import les erreurs spécifiques qui peuvent survenir lors de l'interprétation
from minivm_errors import *

# import les annotations de type pour qualifier correctement nos données
from typing import Dict, Tuple, Callable, List, Optional, Union


def fun(machine):
    machine.add("a", "b", "c")

instructions: Dict[OPCODE, Tuple[TypeOfChunk, Callable]] = {
    # NOP
    OPCODE.NOP: (TypeOfChunk.DATANULL, lambda machine: None),
    # DEBUG
    OPCODE.DBG: (TypeOfChunk.DATASTR, lambda machine, txt: machine.dbg(txt)),
    # +,-,*,/,%
    # chaque operation suis le modéle: ABC -> A = B op C
    OPCODE.ADD_ABC: (TypeOfChunk.DATANULL, fun),
    OPCODE.ADD_ACB: (TypeOfChunk.DATANULL, lambda machine: machine.add("a", "c", "b")),
    OPCODE.ADD_BAC: (TypeOfChunk.DATANULL, lambda machine: machine.add("b", "a", "c")),
    OPCODE.ADD_BCA: (TypeOfChunk.DATANULL, lambda machine: machine.add("b", "c", "a")),
    OPCODE.ADD_CAB: (TypeOfChunk.DATANULL, lambda machine: machine.add("c", "a", "b")),
    OPCODE.ADD_CBA: (TypeOfChunk.DATANULL, lambda machine: machine.add("c", "b", "a")),

    OPCODE.SUB_ABC: (TypeOfChunk.DATANULL, lambda machine: machine.sub("a", "b", "c")),
    OPCODE.SUB_ACB: (TypeOfChunk.DATANULL, lambda machine: machine.sub("a", "c", "b")),
    OPCODE.SUB_BAC: (TypeOfChunk.DATANULL, lambda machine: machine.sub("b", "a", "c")),
    OPCODE.SUB_BCA: (TypeOfChunk.DATANULL, lambda machine: machine.sub("b", "c", "a")),
    OPCODE.SUB_CAB: (TypeOfChunk.DATANULL, lambda machine: machine.sub("c", "a", "b")),
    OPCODE.SUB_CBA: (TypeOfChunk.DATANULL, lambda machine: machine.sub("c", "b", "a")),

    OPCODE.MUL_ABC: (TypeOfChunk.DATANULL, lambda machine: machine.mul("a", "b", "c")),
    OPCODE.MUL_ACB: (TypeOfChunk.DATANULL, lambda machine: machine.mul("a", "c", "b")),
    OPCODE.MUL_BAC: (TypeOfChunk.DATANULL, lambda machine: machine.mul("b", "a", "c")),
    OPCODE.MUL_BCA: (TypeOfChunk.DATANULL, lambda machine: machine.mul("b", "c", "a")),
    OPCODE.MUL_CAB: (TypeOfChunk.DATANULL, lambda machine: machine.mul("c", "a", "b")),
    OPCODE.MUL_CBA: (TypeOfChunk.DATANULL, lambda machine: machine.mul("c", "b", "a")),

    OPCODE.DIV_ABC: (TypeOfChunk.DATANULL, lambda machine: machine.div("a", "b", "c")),
    OPCODE.DIV_ACB: (TypeOfChunk.DATANULL, lambda machine: machine.div("a", "c", "b")),
    OPCODE.DIV_BAC: (TypeOfChunk.DATANULL, lambda machine: machine.div("b", "a", "c")),
    OPCODE.DIV_BCA: (TypeOfChunk.DATANULL, lambda machine: machine.div("b", "c", "a")),
    OPCODE.DIV_CAB: (TypeOfChunk.DATANULL, lambda machine: machine.div("c", "a", "b")),
    OPCODE.DIV_CBA: (TypeOfChunk.DATANULL, lambda machine: machine.div("c", "b", "a")),

    OPCODE.MOD_ABC: (TypeOfChunk.DATANULL, lambda machine: machine.mod("a", "b", "c")),
    OPCODE.MOD_ACB: (TypeOfChunk.DATANULL, lambda machine: machine.mod("a", "c", "b")),
    OPCODE.MOD_BAC: (TypeOfChunk.DATANULL, lambda machine: machine.mod("b", "a", "c")),
    OPCODE.MOD_BCA: (TypeOfChunk.DATANULL, lambda machine: machine.mod("b", "c", "a")),
    OPCODE.MOD_CAB: (TypeOfChunk.DATANULL, lambda machine: machine.mod("c", "a", "b")),
    OPCODE.MOD_CBA: (TypeOfChunk.DATANULL, lambda machine: machine.mod("c", "b", "a")),

    OPCODE.AND_ABC: (TypeOfChunk.DATANULL, lambda machine: machine.function_and("a", "b", "c")),
    OPCODE.AND_ACB: (TypeOfChunk.DATANULL, lambda machine: machine.function_and("a", "c", "b")),
    OPCODE.AND_BAC: (TypeOfChunk.DATANULL, lambda machine: machine.function_and("b", "a", "c")),
    OPCODE.AND_BCA: (TypeOfChunk.DATANULL, lambda machine: machine.function_and("b", "c", "a")),
    OPCODE.AND_CAB: (TypeOfChunk.DATANULL, lambda machine: machine.function_and("c", "a", "b")),
    OPCODE.AND_CBA: (TypeOfChunk.DATANULL, lambda machine: machine.function_and("c", "b", "a")),

    OPCODE.OR_ABC: (TypeOfChunk.DATANULL, lambda machine: machine.function_or("a", "b", "c")),
    OPCODE.OR_ACB: (TypeOfChunk.DATANULL, lambda machine: machine.function_or("a", "c", "b")),
    OPCODE.OR_BAC: (TypeOfChunk.DATANULL, lambda machine: machine.function_or("b", "a", "c")),
    OPCODE.OR_BCA: (TypeOfChunk.DATANULL, lambda machine: machine.function_or("b", "c", "a")),
    OPCODE.OR_CAB: (TypeOfChunk.DATANULL, lambda machine: machine.function_or("c", "a", "b")),
    OPCODE.OR_CBA: (TypeOfChunk.DATANULL, lambda machine: machine.function_or("c", "b", "a")),

    OPCODE.XOR_ABC: (TypeOfChunk.DATANULL, lambda machine: machine.xor("a", "b", "c")),
    OPCODE.XOR_ACB: (TypeOfChunk.DATANULL, lambda machine: machine.xor("a", "c", "b")),
    OPCODE.XOR_BAC: (TypeOfChunk.DATANULL, lambda machine: machine.xor("b", "a", "c")),
    OPCODE.XOR_BCA: (TypeOfChunk.DATANULL, lambda machine: machine.xor("b", "c", "a")),
    OPCODE.XOR_CAB: (TypeOfChunk.DATANULL, lambda machine: machine.xor("c", "a", "b")),
    OPCODE.XOR_CBA: (TypeOfChunk.DATANULL, lambda machine: machine.xor("c", "b", "a")),

    # Comparaison
    OPCODE.CMP_AB: (TypeOfChunk.DATANULL, lambda machine: machine.cmp("a", "b")),
    OPCODE.CMP_AC: (TypeOfChunk.DATANULL, lambda machine: machine.cmp("a", "c")),
    OPCODE.CMP_BA: (TypeOfChunk.DATANULL, lambda machine: machine.cmp("b", "a")),
    OPCODE.CMP_BC: (TypeOfChunk.DATANULL, lambda machine: machine.cmp("b", "c")),
    OPCODE.CMP_CA: (TypeOfChunk.DATANULL, lambda machine: machine.cmp("c", "a")),
    OPCODE.CMP_CB: (TypeOfChunk.DATANULL, lambda machine: machine.cmp("c", "b")),

    # SAUT
    OPCODE.JMP: (TypeOfChunk.DATAINT, lambda machine, inc_adr: machine.jmp(inc_adr)),
    OPCODE.JE: (TypeOfChunk.DATAINT, lambda machine, inc_adr: machine.je(inc_adr)),
    OPCODE.JNE: (TypeOfChunk.DATAINT, lambda machine, inc_adr: machine.jne(inc_adr)),
    OPCODE.JLT: (TypeOfChunk.DATAINT, lambda machine, inc_adr: machine.jlt(inc_adr)),
    OPCODE.JLE: (TypeOfChunk.DATAINT, lambda machine, inc_adr: machine.jle(inc_adr)),
    OPCODE.JGT: (TypeOfChunk.DATAINT, lambda machine, inc_adr: machine.jgt(inc_adr)),
    OPCODE.JGE: (TypeOfChunk.DATAINT, lambda machine, inc_adr: machine.jge(inc_adr)),
    OPCODE.CALL: (TypeOfChunk.DATAINT, lambda machine, inc_adr: machine.call(inc_adr)),
    OPCODE.RET: (TypeOfChunk.DATANULL, lambda machine: machine.ret()),
    # MOV
    OPCODE.MOV_AB: (TypeOfChunk.DATANULL, lambda machine: machine.mov("a", "b")),
    OPCODE.MOV_AC: (TypeOfChunk.DATANULL, lambda machine: machine.mov("a", "c")),
    OPCODE.MOV_BA: (TypeOfChunk.DATANULL, lambda machine: machine.mov("b", "a")),
    OPCODE.MOV_BC: (TypeOfChunk.DATANULL, lambda machine: machine.mov("b", "c")),
    OPCODE.MOV_CA: (TypeOfChunk.DATANULL, lambda machine: machine.mov("c", "a")),
    OPCODE.MOV_CB: (TypeOfChunk.DATANULL, lambda machine: machine.mov("c", "b")),
    # PUSH
    OPCODE.PUSHA: (TypeOfChunk.DATANULL, lambda machine: machine.push(machine.a)),
    OPCODE.PUSHB: (TypeOfChunk.DATANULL, lambda machine: machine.push(machine.b)),
    OPCODE.PUSHC: (TypeOfChunk.DATANULL, lambda machine: machine.push(machine.c)),
    # POP
    OPCODE.POPA: (TypeOfChunk.DATANULL, lambda machine: machine.set("a", machine.pop())),
    OPCODE.POPB: (TypeOfChunk.DATANULL, lambda machine: machine.set("b", machine.pop())),
    OPCODE.POPC: (TypeOfChunk.DATANULL, lambda machine: machine.set("c", machine.pop())),
    # LOAD
    OPCODE.LOADINTA: (TypeOfChunk.DATAINT, lambda machine, integer: machine.loadint("a", integer)),
    OPCODE.LOADINTB: (TypeOfChunk.DATAINT, lambda machine, integer: machine.loadint("b", integer)),
    OPCODE.LOADINTC: (TypeOfChunk.DATAINT, lambda machine, integer: machine.loadint("c", integer)),
    OPCODE.LOADSTRA: (TypeOfChunk.DATASTR, lambda machine, txt: machine.loadstr("a", txt)),
    OPCODE.LOADSTRB: (TypeOfChunk.DATASTR, lambda machine, txt: machine.loadstr("b", txt)),
    OPCODE.LOADSTRC: (TypeOfChunk.DATASTR, lambda machine, txt: machine.loadstr("c", txt)),
    OPCODE.LENSTR_AB: (TypeOfChunk.DATANULL, lambda machine: machine.lenstr("a", "b")),
    OPCODE.LENSTR_AC: (TypeOfChunk.DATANULL, lambda machine: machine.lenstr("a", "c")),
    OPCODE.LENSTR_BA: (TypeOfChunk.DATANULL, lambda machine: machine.lenstr("b", "a")),
    OPCODE.LENSTR_BC: (TypeOfChunk.DATANULL, lambda machine: machine.lenstr("b", "c")),
    OPCODE.LENSTR_CA: (TypeOfChunk.DATANULL, lambda machine: machine.lenstr("c", "a")),
    OPCODE.LENSTR_CB: (TypeOfChunk.DATANULL, lambda machine: machine.lenstr("c", "b")),
    # ENTER/LEAVE/FETCH/STORE
    OPCODE.ENTER: (TypeOfChunk.DATAINT, lambda machine, integer: machine.enter(integer)),
    OPCODE.LEAVE: (TypeOfChunk.DATAINT, lambda machine, integer: machine.leave(integer)),
    OPCODE.FETCHA: (TypeOfChunk.DATAINT, lambda machine, integer: machine.fetch('a', integer)),
    OPCODE.FETCHB: (TypeOfChunk.DATAINT, lambda machine, integer: machine.fetch('b', integer)),
    OPCODE.FETCHC: (TypeOfChunk.DATAINT, lambda machine, integer: machine.fetch('c', integer)),
    OPCODE.STOREA: (TypeOfChunk.DATAINT, lambda machine, integer: machine.store('a', integer)),
    OPCODE.STOREB: (TypeOfChunk.DATAINT, lambda machine, integer: machine.store('b', integer)),
    OPCODE.STOREC: (TypeOfChunk.DATAINT, lambda machine, integer: machine.store('c', integer)),
    # STRING operation
    OPCODE.GETAT_ABC: (TypeOfChunk.DATANULL, lambda machine: machine.getat("a", machine.b, machine.c)),
    OPCODE.GETAT_ACB: (TypeOfChunk.DATANULL, lambda machine: machine.getat("a", machine.c, machine.b)),
    OPCODE.GETAT_BAC: (TypeOfChunk.DATANULL, lambda machine: machine.getat("b", machine.a, machine.c)),
    OPCODE.GETAT_BCA: (TypeOfChunk.DATANULL, lambda machine: machine.getat("b", machine.c, machine.a)),
    OPCODE.GETAT_CAB: (TypeOfChunk.DATANULL, lambda machine: machine.getat("c", machine.a, machine.b)),
    OPCODE.GETAT_CBA: (TypeOfChunk.DATANULL, lambda machine: machine.getat("c", machine.b, machine.a)),
    OPCODE.SETAT_ABC: (TypeOfChunk.DATANULL, lambda machine: machine.setat("a", machine.b, machine.c)),
    OPCODE.SETAT_ACB: (TypeOfChunk.DATANULL, lambda machine: machine.setat("a", machine.c, machine.b)),
    OPCODE.SETAT_BAC: (TypeOfChunk.DATANULL, lambda machine: machine.setat("b", machine.a, machine.c)),
    OPCODE.SETAT_BCA: (TypeOfChunk.DATANULL, lambda machine: machine.setat("b", machine.c, machine.a)),
    OPCODE.SETAT_CAB: (TypeOfChunk.DATANULL, lambda machine: machine.setat("c", machine.a, machine.b)),
    OPCODE.SETAT_CBA: (TypeOfChunk.DATANULL, lambda machine: machine.setat("c", machine.b, machine.a)),
    # conversion
    OPCODE.CASTINTA: (TypeOfChunk.DATANULL, lambda machine: machine.castint("a")),
    OPCODE.CASTINTB: (TypeOfChunk.DATANULL, lambda machine: machine.castint("b")),
    OPCODE.CASTINTC: (TypeOfChunk.DATANULL, lambda machine: machine.castint("c")),
    OPCODE.CASTSTRA: (TypeOfChunk.DATANULL, lambda machine: machine.caststr("a")),
    OPCODE.CASTSTRB: (TypeOfChunk.DATANULL, lambda machine: machine.caststr("b")),
    OPCODE.CASTSTRC: (TypeOfChunk.DATANULL, lambda machine: machine.caststr("c")),
    OPCODE.ORDA: (TypeOfChunk.DATANULL, lambda machine: machine.ord("a")),
    OPCODE.ORDB: (TypeOfChunk.DATANULL, lambda machine: machine.ord("b")),
    OPCODE.ORDC: (TypeOfChunk.DATANULL, lambda machine: machine.ord("c")),
    OPCODE.CHRA: (TypeOfChunk.DATANULL, lambda machine: machine.chr("a")),
    OPCODE.CHRB: (TypeOfChunk.DATANULL, lambda machine: machine.chr("b")),
    OPCODE.CHRC: (TypeOfChunk.DATANULL, lambda machine: machine.chr("c")),
    # APPEL SYSTEME
    OPCODE.SYSCALL: (TypeOfChunk.DATABYTE, lambda machine, integer: machine.syscall(integer)),
}


class Machine:
    #Addition
    def add(self, x, y, z):
        """
            soit X, Y, Z des registres
            X = Y + Z
        """
        setattr(self, x, getattr(self, y) + getattr(self, z))

    #Soustraction
    def sub(self, x, y, z):
        setattr(self, x, getattr(self, y) - getattr(self, z))

    #Multiplication
    def mul(self, x, y, z):
        setattr(self, x, getattr(self, y) * getattr(self, z))

    #Division entière
    def div(self, x, y, z):
        setattr(self, x, getattr(self, y) // getattr(self, z))

    #Modulo (reste de la division)
    def mod(self, x, y, z):
        setattr(self, x, getattr(self, y) % getattr(self, z))

    #And
    def function_and(self, x, y, z):
        setattr(self, x, getattr(self, y) & getattr(self, z))

    #OR
    def function_or(self, x, y, z):
        setattr(self, x, getattr(self, y) | getattr(self, z))

    #XOR
    def xor(self, x, y, z):
        setattr(self, x, getattr(self, y) ^ getattr(self, z))

    #Comparaison
    def cmp(self, x, y):
        self.flags = 0
        val_x = getattr(self, x)
        val_y = getattr(self, y)
        #Vérifie que les deux valeurs sont du même type
        if type(val_x) != type(val_y):
            raise InstructionFault(f"Type {type(val_x)} different from {type(val_y)}")
        else:
            #Si deux entier, le registre flags prend le résultat de v1 - v2
            if (type(val_x) == int) and (type(val_y) == int):
                setattr(self, 'flags', val_x - val_y)

            #Si deux strings, le registre flags prend le résultat de la fonction cmp_str (valeur ordinal de v1 -
            #valeur ordinale de v2)
            elif (type(val_x) == str) and (type(val_y) == str):
                setattr(self, 'flags',
                    self.cmp_str(val_x, val_y))

    #Saut inconditionnel
    def jmp(self, inc_adr):
        self.ip += inc_adr

    #Saut Egal
    def je(self, inc_adr):
        #Si la valeur de flags est 0, la nouvelle adresse est la valeur en argument)
        if self.flags == 0:
            self.ip += inc_adr

    # Saut Non Egal
    def jne(self, inc_adr):
        # Si la valeur de flags est différente de 0, la nouvelle adresse est la valeur en argument)
        if self.flags != 0:
            self.ip += inc_adr

    # Saut Inférieur à
    def jlt(self, inc_adr):
        # Si la valeur de flags est strictement inférieure à 0, la nouvelle adresse est la valeur en argument)
        if self.flags < 0:
            self.ip += inc_adr

    # Saut Inférieur ou égal à
    def jle(self, inc_adr):
        # Si la valeur de flags est inférieure ou égale à 0, la nouvelle adresse est la valeur en argument)
        if self.flags <= 0:
            self.ip += inc_adr

    # Saut Supérieur à
    def jgt(self, inc_adr):
        # Si la valeur de flags est supérieure à 0, la nouvelle adresse est la valeur en argument)
        if self.flags > 0:
            self.ip += inc_adr

    # Saut Supérieur ou égal à
    def jge(self, inc_adr):
        # Si la valeur de flags est supérieure ou égale à 0, la nouvelle adresse est la valeur en argument)
        if self.flags >= 0:
            self.ip += inc_adr

    #Pop
    def pop(self) -> int:
        if self.sp >= len(self.stack):
            raise StackUnderflow("Stack underflow")
        value = self.stack[self.sp]
        self.sp += 1
        return value

    #Call
    def call(self, inc_adr):
        #On enregistre la valeur de Ip sur la pile grâce à la méthode push
        self.push(self.ip)
        #On modifie la valeur de ip
        self.ip += inc_adr

    #Ret
    def ret(self):
        self.ip = self.pop()

    #Mov (copie)
    def mov(self, x, y):
        value_y = getattr(self, y)
        setattr(self, x, value_y)

    #Loadint
    def loadint(self, x, integer):
        setattr(self, x, integer)

    #Loadstr
    def loadstr(self, x, str):
        setattr(self, x, str)

    #Lenstr
    def lenstr(self, x, y):
        compteur = 0
        txt = getattr(self, y)
        for letter in txt:
            compteur += 1
        setattr(self, x, compteur)

    #Leave
    def leave(self, size):
        # Récupère la précédente valeur de BP depuis la pile
        self.sp = self.bp
        self.bp = self.stack[self.sp]
        self.sp += size  # Réajuste SP pour libérer l'espace

    def store (self, regname, idx):
        value = getattr(self, regname)
        size = self.stack[self.bp]
        if idx >= size:
            raise StackFrameError()
        self.stack[self.bp - idx - 1] = value

    def getat(self, x, y, z):
        value = y[z]
        setattr(self, x, value)

    def castint(self, x):
        val = getattr(self, x)
        if not type(val) == str:
            raise InstructionFault(f"valeur {val} non prise en charge")
        val = int(val)
        setattr(self, x, val)

    def caststr(self, x):
        val = getattr(self, x)
        if not type(val) == int:
            raise InstructionFault(f"valeur {val} non prise en charge")
        val = str(val)
        setattr(self, x, val)

    def ord(self, x):
        val = getattr(self, x)
        if type(val) == str and len(val) == 1:
            val = ord(val)
            setattr(self, x, val)
        else:
            raise InstructionFault(f"valeur {val} non prise en charge")


    def chr(self, x):
        val = getattr(self, x)
        if type(val) == int:
            val = chr(val)
            setattr(self, x, val)

        else:
            raise InstructionFault(f"valeur {val} non prise en charge")