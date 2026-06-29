#!/usr/bin/env python3
"""
Assembleur pour le projet mini Vm[SUPPRIME_2600].
"""

import argparse
import pathlib as pl
import re
from minivm import OPCODE, TypeOfChunk
import struct

class AsmParser:
    """
    Classe principale de l'assembleur pour la mini Vm[SUPPRIME_2600].
    """
    def __init__(self, content):
        # on sauvegarde le contenu textuel
        self.content = content
        # on fournit puis compile les "Regular Expressions" nécessaires à l'analyseur syntaxique de l'assembleur
        asm_lang = r"""(?umx)
        (?# Le groupe précedent permet d'être en mode Verbose, Multiligne ET Unicode,
         #  ce qui permet d'écrire les expressions rationnels de façon plus verbeuse.
         #  Le formalisme des expressions rationnels génére un automate proche à celui d'un PEG 
         #  autre formalisme généralement utilisé pour décrire les grammaires des langages informatiques.
         #  Outre ces considérations scientifiques, le langage d'assembleur pour mini Vm[SUPPRIME_2600] est relativement simple
         #  et correspond à la grammaire PEG suivante:

         #  stmts <- stmt* EOS
         #  stmt <- comment / standalone_space_or_return+ / label / insn_int_param / insn_str_param / insn_no_param
         #  comment <- ';' .* EOS
         #  standalone_space_or_return <- SPACE / EOS
         #  label <- IDENTIFIER ':'
         #  insn_int_param <- IDENTIFIER SPACE+ [ DIGIT / IDENTIFIER ]
         #  insn_str_param <- IDENTIFIER SPACE+ STR
         #  insn_no_param <- IDENTIFIER

         #  Note 1: si vous êtes curieux https://en.wikipedia.org/wiki/Parsing_expression_grammar
         #  Note 2: la grammaire donné à titre pédagogique en suivant le formalisme PEG permet d'être facilement comparé avec
         #  le formalisme des expressions réguliéres et d'ainsi voir les similitudes et les différences.

         #  Ces différents formalismes seront étudier dans le module de cours COMP portant sur l'écriture des compilateurs, des
         #  automates et des systèmes d'inférences et leur utilisation dans le domaine de la sécurité.
        )
        (?P<comment>;.*$)
        | (?P<standalone_space_or_return>\s+)
        | (?P<label>(?P<LABEL>\w+):)
        | (?P<insn_int_param>\s*(?P<INSN_INT>\w+)[ \t]+((?P<INT>\d+)|(?P<ID>\w+)))
        | (?P<insn_str_param>\s*(?P<INSN_STR>\w+)[ \t]+"(?P<STR>([^\\]|(\\.))*?)")
        | (?P<insn_no_param>\s*(?P<INSN>\w+))
        """
        self.asm_parser = re.compile(asm_lang)

    def parse(self):
        # on sauvera les "statements" dans une liste
        stmts = []
        # on garde la position du caractère où l'analyse c'est arrêtée
        pos = 0
        # on lit jusqu'à la fin du contenu
        while pos != len(self.content):
            # on demande au RE de faire leur travaille
            m = self.asm_parser.match(self.content, pos)
            # a-t'on identifié quelque chose?
            if m is None:
                raise ValueError(f"Failed to parse {self.content[pos:]}")
            # on stocke le résultat de l'analyse
            stmts.append(m)
            # on avance
            pos += len(m.group(0))
        return stmts

def special_char(mobj):
    """
    Fonction appelée par re.sub
    """
    # on recupére ce qui a été parsé
    d = mobj.groupdict()
    if 'HEX' in d and d['HEX'] is not None:
        # convertis la valeur hexadecimal
        h = int(d['HEX'], 16)
        # retourne le caractère dont le code est donné par h
        return chr(h)
    return ''

def assemble(ast):
    # on stockera la représentation des instructions dans une liste
    ls_chunks = []
    # on se constitue une association entre le nom de l'instruction et sa valeur
    str_opcodes = {str_opcode.lower(): int_opcode for str_opcode, int_opcode in vars(OPCODE).items() if type(str_opcode) is str and str_opcode[0] != '_'}
    # on traite tous les résultats de l'analyse syntaxique
    for stmt_insn in ast:
        # on récupère sous forme de dictionnaire le résultat de l'analyse
        insn = stmt_insn.groupdict()
        # on test les éléments capturés pendant l'analyse, cela nous donne la sémantique de ce qui a été capturé
        # est-ce un label
        if insn['LABEL'] is not None:
            # Les labels sont identifiées à part afin d'opérer le calcul de l'adresse de l'instruction qui suis le label,
            # nous allons procéder en 3 étapes.
            # étape 1: Ici on se contente de stocker le label dans la liste d'instruction.
            # La deuxième étape sera pendant l'encodage.
            ls_chunks += [(TypeOfChunk.DATALABEL, insn['LABEL'])]
        # est-ce une instruction sans opérandes
        elif insn['INSN'] is not None and insn['INSN'] in str_opcodes:
            ls_chunks += [(TypeOfChunk.DATAOPCODE, str_opcodes[insn['INSN']])]
        # est-ce une instruction avec une opérande de type entière (ou label)
        elif insn['INSN_INT'] is not None and insn['INSN_INT'] in str_opcodes:
            ls_chunks += [(TypeOfChunk.DATAOPCODE, str_opcodes[insn['INSN_INT']])]
            # cas particulier de l'appel système
            if insn['INT'] is not None and insn['INSN_INT'] == 'syscall':
                ls_chunks += [(TypeOfChunk.DATABYTE, int(insn['INT']))]
            # encodage pour l'entier
            elif insn['INT'] is not None:
                ls_chunks += [(TypeOfChunk.DATAINT, int(insn['INT']))]
            # encodage pour un label
            elif insn['ID'] is not None:
                ls_chunks += [(TypeOfChunk.DATAXREF, insn['ID'])]
        # est-ce une instruction de type chaîne
        elif insn['INSN_STR'] is not None and insn['INSN_STR'] in str_opcodes:
            ls_chunks += [(TypeOfChunk.DATAOPCODE, str_opcodes[insn['INSN_STR']])]
            # transforme les caractères backslashés de la chaîne
            txt = insn['STR']
            # on transforme les séquences de caractére (man ascii)
            txt = txt.replace(r'\0', chr(0))
            txt = txt.replace(r'\a', chr(7))
            txt = txt.replace(r'\b', chr(8))
            txt = txt.replace(r'\t', chr(9))
            txt = txt.replace(r'\n', chr(10))
            txt = txt.replace(r'\v', chr(11))
            txt = txt.replace(r'\f', chr(12))
            txt = txt.replace(r'\r', chr(13))
            txt = txt.replace(r'\\', chr(92))
            # substitue les définitions de caractères en hexa
            txt = re.sub(r'\\(x|X)(?P<HEX>[0-9a-fA-F]{2})', special_char, txt)
            # encodage pour une chaine
            ls_chunks += [(TypeOfChunk.DATASTR, txt)]
    return ls_chunks

# lorsque ce script est executé
if __name__ == "__main__":
    # on parse les paramètres en ligne de commande
    ap = argparse.ArgumentParser()
    ap.add_argument(dest="file_name", help="File to assemble")
    args = ap.parse_args()
    # on vérifie l'existance et l'extension du fichier
    fn = pl.Path(args.file_name)
    if not fn.exists():
        raise ValueError(f"File {fn} isn't found.")
    if fn.suffix != '.vm[SUPPRIME_2600]':
        raise ValueError(f"File {fn} must have a '.vm[SUPPRIME_2600]' extension.")
    # on lit le fichier
    content = None
    with open(fn, "r") as f:
        content = f.read()
    # on instancie notre objet responsable de l'assemblage avec le contenu du fichier
    asm = AsmParser(content)
    # on récupère le résultat de l'analyse syntaxique du fichier
    ast = asm.parse()
    # on récupère une liste d'instruction
    list_chunks = assemble(ast)
    # importe la fonction d'encodage en opcode
    from minivm_encode import encode_opcodes
    # on transforme notre liste d'instruction en bloc d'octet
    compiled = encode_opcodes(list_chunks)
    # on écrit dans un fichier
    out = fn.name.replace('.vm[SUPPRIME_2600]', '.bin[SUPPRIME_2600]')
    with open(out, "wb") as f:
        f.write(compiled)
