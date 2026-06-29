import struct
from enum import IntEnum, auto

class TypeOfChunk:
    DATANULL = 240 # F0 en hexa
    DATAOPCODE = 241 # F1
    DATAINT = 242 # F2
    DATASTR = 243 # F3

def decode_opcodes(buf: bytes):
    # list de résultat
    ls = []
    # position dans le buffer
    pos = 0
    # valeur maximal pour la variable position
    maxpos = len(buf)
    while pos < maxpos:
        # Lire un octet dans le bloc d'octet 'buf' à la position 'pos'
        # reçoit donc un tuple d'un seul élément 
        prefix = struct.unpack_from('B', buf, pos)
        # passe à l'octet suivant
        pos += 1
        # variable pour stocker le morceau (en anglais chunk)
        chunk = None
        # on test tous les cas possibles pour l'octet de prefix
        if prefix[0] == TypeOfChunk.DATANULL:
            # DATANULL ne préfixe pas de valeur...
            chunk = (prefix[0], None)
        elif prefix[0] == TypeOfChunk.DATAOPCODE:
            # TODO: lire un caractère dans le bloc d'octet 'buf' à la position 'pos'
            d = struct.unpack_from('c', buf, pos)
            # passe à l'octet suivant
            pos += 1
            # compose le tuple TypeOfChunk et la valeur du morceau
            chunk = (prefix[0], d[0])
        elif prefix[0] == TypeOfChunk.DATAINT:
            # TODO: lire un entier signé sur 4 octet en big-endian dans le bloc d'octet 'buf' à la position 'pos'
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
            # TODO:
            d = struct.unpack_from(f'{n[0]}s', buf, pos)
            # saute N octets correspondant à la taille de la chaîne de caractère 
            pos += n[0]
            # compose le tuple TypeOfChunk et la valeur du morceau
            chunk = (prefix[0], d[0].decode('utf-8'))
        else:
            # si l'octet de prefix n'est pas reconnu
            raise ValueError(f"Unkown prefix value {prefix[0]} at pos {pos} in: {buf}")
        # on ajoute le morceau dans la liste
        ls.append(chunk)
    return ls


