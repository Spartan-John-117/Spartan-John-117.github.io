import struct
from typing import Union, List, Tuple, Literal
from enum import IntEnum

class TypeOfChunk:
    DATANULL = 240 # F0 en hexa
    DATAOPCODE = 241 # F1
    DATAINT = 242 # F2
    DATASTR = 243 # F3

def encode_opcodes(ls: List[Union[Tuple[Literal[TypeOfChunk.DATAOPCODE], bytes], Tuple[Literal[TypeOfChunk.DATAINT], int], Tuple[Literal[TypeOfChunk.DATASTR], str]]]):
    # on constitue une liste de tout les morceaux
    chunks = bytearray()
    for d in ls:
        prefix, value = d
        buf = None
        # on test toutes les valeurs possibles de prefix
        if prefix == TypeOfChunk.DATANULL:
            # on ajoute l'octet du prefix
            buf = b"\xf0"
        elif prefix == TypeOfChunk.DATAOPCODE:
            # TODO: encode le prefix et la valeur dans buf
            buf = b"\xf1"
            buf += struct.pack('c', value)
            pass
        elif prefix == TypeOfChunk.DATAINT:
            # TODO: encode le prefix et la valeur dans buf
            buf = b"\xf2"
            buf += struct.pack('>i', value)
            pass
        elif prefix == TypeOfChunk.DATASTR:
            # on encode la chaîne de caractère sous forme de bloc d'octet en UTF-8
            btxt = value.encode("utf-8")
            # on calcul la taille de ce bloc d'octet
            n = len(btxt)
            # TODO: encode le prefix, n et la valeur btxt
            buf = b"\xf3"
            buf += struct.pack(f'B{n}s', n, btxt)
            pass
        # on concatene tous les morceaux pour faire un seul buffer
        chunks += buf
    # on convertie notre 'bytearray' en 'bytes' en sortant
    return bytes(chunks)

