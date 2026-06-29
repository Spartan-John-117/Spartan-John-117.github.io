import sys
from typing import Dict, Tuple, Callable, List, Optional, Union
from enum import IntEnum, auto
import pathlib as pl
import struct
from minivm_errors import *

class TypeOfChunk:
    DATANULL = 240 # F0 en hexa
    DATAOPCODE = 241 # F1
    DATAINT = 242 # F2
    DATASTR = 243 # F3
    DATABYTE = 244 # F4: Seulement pour la gestion des appels systèmes
    DATALABEL = 245 # F5: Seulement pour la gestion des LABEL ASM
    DATAXREF = 246 # F6: Seulement quand un LABEL est utilisé dans une instruction jmp/j*/call

class OPCODE(IntEnum):
    NOP = 0
    # DEBUG
    DBG = auto()
    # Arithmetic/logical unit
    ADD_ABC = auto()
    ADD_ACB = auto()
    ADD_BAC = auto()
    ADD_BCA = auto()
    ADD_CAB = auto()
    ADD_CBA = auto()
    SUB_ABC = auto()
    SUB_ACB = auto()
    SUB_BAC = auto()
    SUB_BCA = auto()
    SUB_CAB = auto()
    SUB_CBA = auto()
    MUL_ABC = auto()
    MUL_ACB = auto()
    MUL_BAC = auto()
    MUL_BCA = auto()
    MUL_CAB = auto()
    MUL_CBA = auto()
    DIV_ABC = auto()
    DIV_ACB = auto()
    DIV_BAC = auto()
    DIV_BCA = auto()
    DIV_CAB = auto()
    DIV_CBA = auto()
    MOD_ABC = auto()
    MOD_ACB = auto()
    MOD_BAC = auto()
    MOD_BCA = auto()
    MOD_CAB = auto()
    MOD_CBA = auto()
    AND_ABC = auto()
    AND_ACB = auto()
    AND_BAC = auto()
    AND_BCA = auto()
    AND_CAB = auto()
    AND_CBA = auto()
    OR_ABC = auto()
    OR_ACB = auto()
    OR_BAC = auto()
    OR_BCA = auto()
    OR_CAB = auto()
    OR_CBA = auto()
    XOR_ABC = auto()
    XOR_ACB = auto()
    XOR_BAC = auto()
    XOR_BCA = auto()
    XOR_CAB = auto()
    XOR_CBA = auto()
    # Comparaison
    CMP_AB = auto()
    CMP_AC = auto()
    CMP_BA = auto()
    CMP_BC = auto()
    CMP_CA = auto()
    CMP_CB = auto()
    # SAUT
    JMP = auto()
    JE = auto()
    JNE = auto()
    JLT = auto()
    JLE = auto()
    JGT = auto()
    JGE = auto()
    CALL = auto()
    RET = auto()
    # operation mémoire
    MOV_AB = auto()
    MOV_AC = auto()
    MOV_BA = auto()
    MOV_BC = auto()
    MOV_CA = auto()
    MOV_CB = auto()
    PUSHA = auto()
    PUSHB = auto()
    PUSHC = auto()
    POPA = auto()
    POPB = auto()
    POPC = auto()
    # LOAD
    LOADINTA = auto()
    LOADINTB = auto()
    LOADINTC = auto()
    LOADSTRA = auto()
    LOADSTRB = auto()
    LOADSTRC = auto()
    LENSTR_AB = auto()
    LENSTR_AC = auto()
    LENSTR_BA = auto()
    LENSTR_BC = auto()
    LENSTR_CA = auto()
    LENSTR_CB = auto()
    # ENTER/LEAVE/FETCH/STORE
    ENTER = auto()
    LEAVE = auto()
    FETCHA = auto()
    FETCHB = auto()
    FETCHC = auto()
    STOREA = auto()
    STOREB = auto()
    STOREC = auto()
    # STRING operation
    GETAT_ABC = auto()
    GETAT_ACB = auto()
    GETAT_BAC = auto()
    GETAT_BCA = auto()
    GETAT_CAB = auto()
    GETAT_CBA = auto()
    SETAT_ABC = auto()
    SETAT_ACB = auto()
    SETAT_BAC = auto()
    SETAT_BCA = auto()
    SETAT_CAB = auto()
    SETAT_CBA = auto()
    # conversion
    CASTINTA = auto()
    CASTINTB = auto()
    CASTINTC = auto()
    CASTSTRA = auto()
    CASTSTRB = auto()
    CASTSTRC = auto()
    ORDA = auto()
    ORDB = auto()
    ORDC = auto()
    CHRA = auto()
    CHRB = auto()
    CHRC = auto()
    # appel système
    SYSCALL = auto()

class SYSCALLS(IntEnum):
    SYSEXIT = 0
    SYSECHO = auto()

syscalls = {
        SYSCALLS.SYSEXIT: lambda machine: machine.sysexit(),
        SYSCALLS.SYSECHO: lambda machine: machine.sysecho(machine.a),
}

def cmp_str(txt1, txt2):
    for a, b in zip(txt1, txt2):
        c = ord(a) - ord(b)
        if c != 0:
            return c
    return 0

class Machine:
    def __init__(self):
        # Nos 3 registres généraux
        self.a = 0
        self.b = 0
        self.c = 0
        # Nos registres spécifiques
        ## Pointeur d'instruction
        self.ip = 0
        ## Drapeaux d'état du dernier calcul de la machine
        self.flags = 0
        ## PILE SYSTEME
        ### Haut de la pile
        self.sp = 100
        ### Cadre de pile
        self.bp = 100
        ### PILE
        self.stack = [None] * 100

    def set(self, name, v):
        self.log(f"{name} = {v}")
        setattr(self, name, v)

    def log(self, txt):
        with open("Vm[SUPPRIME_2600].log", "a+") as f:
            f.write(txt + "\n")

    def load(self, b: bytes):
        self.mem = b

    def execute(self):
        # import la fonction de décodage d'opcode uniquement pour l'execution
        from minivm_decode import decode_opcode
        # import le dictionnaire d'instruction
        from minivm_insn import instructions
        try:
            while True:
                self.ip, prefix_opcode = decode_opcode(self.mem, self.ip)
                # On s'arrête quand on arrive à la fin de la mémoire
                if prefix_opcode[1] is None:
                    raise RuntimeError(f"Instruction Pointer going nowhere...")
                #self.log(f"{self.ip} {prefix_opcode}")
                if prefix_opcode[0] != TypeOfChunk.DATAOPCODE:
                    raise ValueError(f"Incoherent executable: bad prefix {prefix_opcode[0]}")
                self.opcode = prefix_opcode[1]
                if self.opcode not in instructions:
                    raise ValueError(f"Unkown opcode {opcode}")
                param = instructions[self.opcode][0]
                self.log(f"PARAM {param} for opcode {self.opcode}")
                if param == TypeOfChunk.DATANULL:
                    instructions[self.opcode][1](self)
                elif param == TypeOfChunk.DATABYTE:
                    self.ip, prefix_param = decode_opcode(self.mem, self.ip)
                    if prefix_param[0] != param:
                        raise ValueError(f"Incoherent executable: prefix conflict {prefix_param[0]}")
                    self.log(f"TYPEBYTE {type(prefix_param[1])} {prefix_param[1]}")
                    instructions[self.opcode][1](self, prefix_param[1])
                elif param == TypeOfChunk.DATAINT:
                    self.ip, prefix_param = decode_opcode(self.mem, self.ip)
                    if prefix_param[0] != param:
                        raise ValueError(f"Incoherent executable: prefix conflict {prefix_param[0]}")
                    self.log(f"TYPEINT {type(prefix_param[1])} {prefix_param[1]}")
                    instructions[self.opcode][1](self, prefix_param[1])
                elif param == TypeOfChunk.DATASTR:
                    self.ip, prefix_param = decode_opcode(self.mem, self.ip)
                    if prefix_param[0] != param:
                        raise ValueError(f"Incoherent disassembly: {prefix_param[0]}")
                    self.log(f"TYPESTR {type(prefix_param[1])}")
                    instructions[self.opcode][1](self, prefix_param[1])
                delattr(self, 'opcode')
        except StopMachine:
            return True
        except Exception as e:
            raise e

    # LISTE DES INSTRUCTIONS FOURNIS

    def dbg(self, txt):
        self.log(f"\nMACHINE DBG WHEN {txt}")
        self.log(f"A: {repr(self.a)} B: {repr(self.b)} C: {repr(self.c)}")
        self.log(f"IP: {self.ip} SP: {self.sp} BP: {self.bp} FLAGS: {self.flags}")
        self.log(f"STACK {self.stack}")

    def push(self, v):
        # on va stocker une valeur
        self.sp -= 1
        # la pile est-elle pleine?
        if self.sp < 0:
            raise StackOverflow()
        # on stocke
        self.stack[self.sp] = v
        self.log(f"PUSH STACK {v} - {self.stack}")

    def enter(self, size):
        # on stocke la valeur précédente de BP car on va le modifier
        # l'ancienne valeur permettait d'accéder au variable local de la fonction appelante
        self.push(self.bp)
        # on sauve aussi la taille du cadre de pile pour FETCH/STORE
        self.push(size)
        self.log(f"ENTER {size}")
        self.log(f"STACK {self.stack}")
        # le cadre de pile commence après la sauvegarde de BP/SIZE
        self.bp = self.sp
        # on reserve la zone
        self.sp -= size

    def fetch(self, regname, idx):
        self.log(f"FETCH {self.bp} - {idx}")
        self.log(f"STACK {self.stack}")
        # on récupere la taille du cadre de pile
        sz = self.stack[self.bp]
        self.log(f"GET SZ {sz}")
        # si l'index déborde la taille du cadre c'est une erreur
        if idx >= sz:
            self.log(f"INDEX OVER STACK FRAME {idx} >= {sz}")
            raise StackFrameError()
        # si bp permet d'acceder à la taille, on rajoute le -1 car on a préservé l'ancien BP aussi sur la pile
        setattr(self, regname, self.stack[self.bp - idx - 1])

    def setat(self, name, idx, val):
        # on récupere le registre préciser dans la variable name
        tab = getattr(self, name)
        self.log(f"SETAT IDX {idx} L {len(tab)}")
        # si l'index est supérieur à la taille de la chaine, on l'augmente
        if idx >= len(tab):
            self.log(f"EXPAND")
            # on augmente d'un nombre de caractère égale à la différence entre l'index et la taille
            tab = tab + ' ' * ((idx + 1) - len(tab))
        # les chaines de caractère sont immutable (non-modifiable) en python
        # donc pour modifier le caractère à la position idx, on le fait comme si c'était une liste
        tab = list(tab)
        tab[idx] = val
        # on retransforme en chaine
        val = "".join(tab)
        # finallement, on modifie le registre
        setattr(self, name, val)

    def syscall(self, numsyscall):
        # si le numéro de l'appel système n'est pas dans notre liste
        if numsyscall not in syscalls:
            self.log(f"Unknown SYSCALL number {numsyscall}")
            raise InstructionFault()
        # appel l'appel système
        syscalls[numsyscall](self)

    def sysexit(self):
        # appel système qui arrête la machine
        raise StopMachine()

    def sysecho(self, p):
        # appel système qui affiche le paramètre
        if type(p) is not str:
            raise InstructionFault()
        print(p, end='')

    ##


# Monkey Patching de 'minivm_insn.py:Machine' vers 'minivm.py:Machine'
from minivm_insn import Machine as Insn
# toutes les méthodes non magique de Insn sont des méthodes de Machine
for k, v in vars(Insn).items():
    if k[0] != '_':
        # on rajoute dans la classe Machine la méthode de Insn
        setattr(Machine, k, v)

# A titre indicatif, cette variable de module permet de savoir le nombre d'instuction de cette machine
instruction_numbers = len([insn for insn in vars(OPCODE).keys() if insn[0] != '_'])
