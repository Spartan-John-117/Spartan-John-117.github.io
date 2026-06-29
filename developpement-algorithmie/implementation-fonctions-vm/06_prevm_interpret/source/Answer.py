from enum import IntEnum, auto
from typing import List

class OPCODE(IntEnum):
    NOP = 0
    # Arithmetic/logical unit
    ADD = auto()
    MUL = auto()
    # operation mémoire
    PUSHA = auto()
    PUSHB = auto()
    PUSHC = auto()
    POPA = auto()
    POPB = auto()
    POPC = auto()
    
# TODO: Fonctions additionnels

# Instructions associées aux opcodes
instructions = {
    OPCODE.NOP: lambda machine: machine.nop(),
    OPCODE.ADD: lambda machine: machine.set("a", machine.b + machine.c),
    OPCODE.MUL: lambda machine: machine.set("a", machine.b * machine.c),
    OPCODE.PUSHA: lambda machine: machine.push(machine.a),
    OPCODE.POPA: lambda machine: machine.set("a", machine.pop()),  
    # TODO
    OPCODE.PUSHB: lambda machine: machine.push(machine.b),
    OPCODE.POPB: lambda machine: machine.set("b", machine.pop()),
    OPCODE.PUSHC: lambda machine: machine.push(machine.c),
    OPCODE.POPC: lambda machine: machine.set("c", machine.pop()),
}

class Machine:
    def __init__(self):
        self.a = 0
        self.b = 0
        self.c = 0
        self.ip = 0
        self.list_instructions = []
        self.sp = 100
        self.stack = [None] * 100

    def nop(self):
        pass

    def set(self, name, v):
        #print(f"set {name} = {v}")
        setattr(self, name, v)

    def get(self, name):
        return getattr(self, name)

    def push(self, v):
        self.sp -= 1
        if self.sp < 0:
            raise RuntimeError("Stack overflow")
        #print(f"PUSH: {v}")
        self.stack[self.sp] = v

    def pop(self) -> int:
    # TODO 
        if self.sp >= len(self.stack):
            raise RuntimeError("Stack underflow")
        value = self.stack[self.sp]
        #print(f"POP: {value}")
        self.sp += 1
        return value

    def load_instructions(self, ls: List[OPCODE]):
        self.list_instructions += ls

    def next_instruction(self):
        self.ip += 1
        #print(f"NEW IP: {self.ip}")

    def get_instruction(self) -> OPCODE:
        if self.ip < len(self.list_instructions):
            return self.list_instructions[self.ip]
        return None

    def execute(self):
        while True:
            opcode = self.get_instruction()
            if opcode is None:
                return
            if opcode in instructions:
                instructions[opcode](self)
            else:
                raise ValueError(f"Unkown opcode {opcode}")
            self.next_instruction()

