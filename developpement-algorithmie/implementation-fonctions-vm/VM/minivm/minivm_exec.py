#!/usr/bin/env python3
"""
Chargeur de code pour mini Vm[SUPPRIME_2600].
"""

import argparse
import pathlib as pl
from minivm import Machine

# lorsque ce script est executé
if __name__ == "__main__":
    # on parse les paramètres en ligne de commande
    ap = argparse.ArgumentParser()
    ap.add_argument(dest="file_name", help="File to exec")
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
    # on instancie notre objet responsable de l'execution avec le contenu du fichier
    asm = Machine()
    asm.load(content)
    asm.execute()
