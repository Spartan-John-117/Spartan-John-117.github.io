#!/usr/bin/env python3
"""
Désassembleur pour le projet mini Vm[SUPPRIME_2600].
"""

import argparse
import pathlib as pl
from minivm import OPCODE, TypeOfChunk, SYSCALLS
import struct

def decode_opcodes(buf: bytes):
    # import la fonction de décodage d'un opcode
    from minivm_decode import decode_opcode
    # liste de résultat
    ls = []
    # position dans le buffer
    pos = 0
    # valeur maximal pour la variable position
    maxpos = len(buf)
    # pour tous les octets à lire
    while pos < maxpos:
        # on appel le décodeur d'instruction
        pos, chunk = decode_opcode(buf, pos)
        # on ajoute le morceau dans la liste
        ls.append(chunk)
    return ls

class Disasm:
    """
    Classe principale du désassembleur pour la mini Vm[SUPPRIME_2600].
    """
    def __init__(self, content):
        # le contenu est forcément un bloc d'octet
        if type(content) is not bytes:
            raise ValueError(f"content is not binary")
        # on stocke pour plus tard
        self.content = content

    def dump(self) -> str:
        # import le dictionnaire d'instruction pour le dump
        from minivm_insn import instructions
        # on récupere la liste d'instruction inverse à partir du bloc d'octet
        ls = decode_opcodes(self.content)
        # on se constitue une association entre la valeur d'une instruction et le nom de cet instruction
        str_opcodes = {intop: strop.lower() for strop, intop in vars(OPCODE).items() if type(strop) is str and strop[0] != '_'}
        # on se constitue une association entre la valeur d'un appel système et le nom de cet appel
        str_syscalls = {intsys: strsys.lower() for strsys, intsys in vars(SYSCALLS).items() if type(strsys) is str and strsys[0] != '_'}
        # on va lire nos instruction de manière non-linéraire, c'est préférable d'utiliser ce qu'on appel un 'itérateur'
        # ce concept sera vu plus tard dans la formation, mais peut être facilement compris par l'usage
        itcode = iter(ls)
        # on va constituer une liste de chaine pour l'affichage
        out = []
        # on va calculer l'adresse mémoire de chaque instruction
        adr = 0
        while True:
            # entre 2 instructions on va calculer l'incrément de l'adresse
            inc_adr = 0
            try:
                # on essaie de lire une instruction
                op = next(itcode)
            except StopIteration:
                # on est arrivé à la fin, on sors
                break
            # normalement on ne devrait rencontré que des DATAOPCODE
            if op[0] != TypeOfChunk.DATAOPCODE:
                raise ValueError(f"Incoherent file, found a standalone prefix {op[0]}")
            # on compte le prefix puis l'opcode
            inc_adr += 2
            # on stocke l'instruction
            insn = op[1]
            # si on ne connait pas l'instruction c'est un problème
            if insn not in instructions:
                raise ValueError(f"Unknown instruction {insn}")
            # on récupère les caractèristiques de l'instruction
            instruction = instructions[insn]
            # on récupère le type d'opérande de l'instruction
            param = instruction[0]
            # pour stocker l'operande sous forme de chaine
            txt_param = None
            # on test tous les cas d'operande
            if param == TypeOfChunk.DATANULL:
                # l'instruction ne prend pas d'opérande
                pass
            elif param == TypeOfChunk.DATABYTE:
                # dans le cas particulier de l'appel système
                # on récupère l'opérande
                p = next(itcode)
                # on transforme l'entier en chaine
                txt_param = str(p[1])
                # on compte la taille de l'opérande (1 seul octet)
                inc_adr += 2
                # on rajoute le nom de l'appel système
                txt_param += f" ({str_syscalls[p[1]]})"
            elif param == TypeOfChunk.DATAINT:
                # dans le cas d'un entier en opérande
                # on récupère l'opérande
                p = next(itcode)
                # on transforme l'entier en chaine
                txt_param = str(p[1])
                # on compte la taille de l'opérande
                inc_adr += 5
                # dans le cas d'une instruction de saut, on calcul et on rajoute l'adresse hexa dans le dump
                if insn >= OPCODE.JMP and insn <= OPCODE.CALL:
                    txt_param += f" ({adr + inc_adr + p[1]:08x})"
            elif param == TypeOfChunk.DATASTR:
                # dans le cas d'une chaine en opérande
                # on récupère l'opérande
                p = next(itcode)
                # on lit la chaine et transformons les caractères spéciaux sous forme de séquence d'échappement
                txt_param = '"' + p[1].encode('unicode_escape').decode('utf-8') + '"'
                # on compte la taille de l'opérande
                inc_adr += 2 + len(p[1])
            # on récupère le nom de l'instruction
            txt_insn = str_opcodes[insn]
            # s'il y a un texte d'operande non null, on le rajoute
            if txt_param is not None:
                txt_insn += " " + txt_param
            # on récupère la sequence d'octet pour l'affichage
            row = self.content[adr : adr + inc_adr]
            # on transforme la sequence en hexa
            binsn = [f"{b:02x}" for b in row]
            txt_bytes = ' '.join(binsn)
            # si la sequence est trop longue (grosse chaine de caractère)
            col_size = 60
            if len(txt_bytes) > col_size:
                # on n'affichera pas tout
                txt_bytes = txt_bytes[:(col_size - 3)] + '...'
            # on constitue une ligne d'affichage
            out.append(f"{adr:08x} | {txt_bytes:60} | {txt_insn}")
            # on passe à l'instruction suivante
            adr += inc_adr
        # on concaténe toutes les lignes d'affichages entre elles
        return "\n".join(out)

# lorsque ce script est executé
if __name__ == "__main__":
    # on parse les paramètres en ligne de commande
    ap = argparse.ArgumentParser()
    ap.add_argument(dest="file_name", help="File to disassemble")
    args = ap.parse_args()
    # on vérifie l'existance et l'extension du fichier
    fn = pl.Path(args.file_name)
    if not fn.exists():
        raise ValueError(f"File {fn} isn't found.")
    if fn.suffix != '.bin[SUPPRIME_2600]':
        raise ValueError(f"File {fn} must have a '.bin[SUPPRIME_2600]' extension.")
    # on lit le fichier
    content = None
    with open(fn, "rb") as f:
        content = f.read()
    # on instancie notre objet responsable du désassemblage avec le contenu du fichier
    asm = Disasm(content)
    # on affiche le dump obtenu
    print(asm.dump())
