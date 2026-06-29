#!/usr/bin/env python3

import struct


def ushort_uint(buffer):    
                                                                # Filtre : ">" = Big Endian, "H" = entier court non signé 
                                                                # sur 2 octets (ushort), "I" entier non signé sur 4 octets 
                                                                # (uint).

    ushort, uint = struct.unpack('>HI', buffer[:6])             # le buffer doit faire au moins 6 octets, pour contenir 
                                                                # le deux informations
    return ushort, uint

def buf2latin(buffer):
    size = struct.unpack('>H', buffer[:2])[0]                   # Obtient la taille en prenant les deux premiers octets de 
                                                                # la chaîne et en les considérant comme des entiers courts 
                                                                # non signés.

    latin1_str = buffer[2:2+size].decode('latin-1')             # Obtient la chaîne de caractères en partant de l'octet 
                                                                # suivant la taille et prenant autant d'octets que précisé 
                                                                # par size et décode la chaine en latin-1

    return size, latin1_str

def ascii2buf(*strings):
    buffer = bytearray()

    buffer.extend(struct.pack('>I', len(strings)))              # On ajoute au buffer la longueur totale des strings

    for string in strings:                                      # Pour chaque chaîne dans la chaîne de chaîne
        encoded_string = string.encode('ascii')                 # Encodage la chaîne en ASCII
        buffer.extend(struct.pack('>H', len(encoded_string)))   # Ajoute la taille de la chaîne au buffer (entier court )
        buffer.extend(encoded_string)                           # Ajoute la chaîne encodée au buffer

    return buffer
    
