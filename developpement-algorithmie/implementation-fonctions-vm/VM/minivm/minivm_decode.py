from minivm import TypeOfChunk
from typing import Dict, Tuple, Callable, List, Optional, Union
import struct

def decode_opcode(buf: bytes, pos) -> Tuple[int, Tuple[TypeOfChunk, Optional[Union[int, str]]]]:
    # attention pos ne peut pas être au dela de la taille du buffer
    if pos == len(buf):
        return (0, (TypeOfChunk.DATANULL, None))
    # Lire un octet dans le bloc d'octet 'buf' à la position 'pos'
    # recoie donc un tuple d'un seul élément
    #print("buf decode =", buf)
    prefix = struct.unpack_from('B', buf, pos)
    # passe à l'octet suivant
    pos += 1
    # variable pour stocker le morceau (en anglais chunk)
    chunk = None
    # on test tous les cas possibles pour l'octet de prefix
    #print("prefix decode =", prefix)
    if prefix[0] == TypeOfChunk.DATANULL:
        # DATANULL ne préfixe pas de valeur...
        chunk = (prefix[0], None)
    elif prefix[0] == TypeOfChunk.DATAOPCODE or prefix[0] == TypeOfChunk.DATABYTE:
        # lire un 'unsigned char' dans le bloc d'octet 'buf' à la position 'pos'
        # TODO ...
        d = struct.unpack_from('B', buf, pos)
        # passe à l'octet suivant
        pos += 1
        # compose le tuple TypeOfChunk et la valeur du morceau
        chunk = (prefix[0], d[0])
    elif prefix[0] == TypeOfChunk.DATAINT:
        # lire un entier signé sur 4 octet en big-endian dans le bloc d'octet 'buf' à la position 'pos'
        # TODO ...
        d = struct.unpack_from('>i', buf, pos)
        # saute 4 octets, c-a-d la taille de l'entier signé précedent
        pos += 4
        # compose le tuple TypeOfChunk et la valeur du morceau
        chunk = (prefix[0], d[0])
    elif prefix[0] == TypeOfChunk.DATASTR:
        # lit un octet encodant la taille de la chaîne de caractère qui suivra
        n = struct.unpack_from('B', buf, pos)
        # passe à l'octet suivant
        pos += 1
        # encode la chaine de caractère
        # TODO ...
        d = struct.unpack_from(f'{n[0]}s', buf, pos)
        #d = struct.unpack_from(str(n[0]) + 's', buf, pos)
        # saute N octets correspondant à la taille de la chaîne de caractère 
        pos += n[0]
        # compose le tuple TypeOfChunk et la valeur du morceau
        chunk = (prefix[0], d[0].decode('utf-8'))
    else:
        # si l'octet de prefix n'est pas reconnu
        #print(f"Debug: buffer so far: {buf[:pos]}")
        raise ValueError(f"Unkown prefix value {prefix[0]} at pos {pos} in: {buf}")
    # on renvoie l'instruction décodé
    return (pos, chunk)
