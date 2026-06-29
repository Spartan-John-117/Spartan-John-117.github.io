#!/usr/bin/env python3
"""
 Hexadecimal dumper
"""

import argparse
import pathlib as pl

class HexaDump:
    def __init__(self, content):
        self.content = content

    def dump(self):
        # calcule le nombre de bloc de 16 octets
        nb_block = len(self.content) // 16
        # la taille du contenu est-elle aligné sur 16 octets
        align = len(self.content) % 16 == 0
        nb_block += 1 if not align else 0
        out = []
        adr = 0
        # on traite par block de 16
        for block in range(nb_block):
            # on capture 16 octets
            row = self.content[adr : adr + 16]
            # l'affichage se fait en 2 colonne de 8 octets
            row1 = [f"{b:02x}" for b in row[:8]]
            row2 = [f"{b:02x}" for b in row[8:]]
            # on constitue une chaîne des caractères uniquement affichable sinon on remplace par un point
            dump_char = "".join([chr(c) if chr(c).isprintable() else '.' for c in row])
            # on compose la chaîne de caractère de la ligne qui sera affiché
            txt_row = f"{adr:08x}  {' '.join(row1):23}  {' '.join(row2):23}  |{dump_char:16}|"
            # on rajoute la ligne dans notre liste
            out.append(txt_row)
            # calcul l'adresse affiché en début de ligne
            adr += 16
        # si la taille du contenu n'est pas aligné la dernière ligne du dump affiche la taille en hexa du contenu
        if not align:
            # on rajoute la taille en hexa du contenu
            out.append(f"{len(self.content):08x}")
        # retourne un chaine de caractère constitué par la concaténation de notre liste de str, séparé par un retour chariot.
        return "\n".join(out)

# lorsque ce script est executé
if __name__ == "__main__":
    # on parse les paramètres en ligne de commande
    ap = argparse.ArgumentParser()
    ap.add_argument(dest="file_name", help="File to dump in Hexa")
    args = ap.parse_args()
    # on vérifie l'existance
    fn = pl.Path(args.file_name)
    if not fn.exists():
        raise ValueError(f"File {fn} isn't found.")
    # on lit le fichier
    content = None
    with open(fn, "rb") as f:
        content = f.read()
    # on affiche
    hx = HexaDump(content)
    print(hx.dump())
