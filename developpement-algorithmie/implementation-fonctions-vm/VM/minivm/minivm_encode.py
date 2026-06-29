from minivm import TypeOfChunk
import struct

def encode_opcodes(ls):
    # on constitue une liste de tout les morceaux
    chunks = bytearray()
    # pour stocker l'adresse des labels
    labels = {}
    # pour stocker les references croisées de l'utilisation des labels
    xrefs = {}
    # pour chaque instruction
    for d in ls:
        # on traite le prefix et la valeur associée
        prefix, value = d
        # buf servira à stocker le bloc d'octet
        buf = None
        # on test toutes les valeurs possibles de prefix
        if prefix == TypeOfChunk.DATANULL:
            # on ajoute un octet NULL
            buf = b"\x00"
        elif prefix == TypeOfChunk.DATALABEL:
            # la valeur est le nom du label
            label = value
            # avons-nous déjà déclaré ce label
            if label in labels:
                raise ValueError(f"Multiple re-defined for label {label}")
            # étape 2: la position en octet courante sera la futur adresse de l'instruction qui suis le label
            # on la sauve ici pour l'étape 3 qui viendra à la fin de l'encodage
            labels[label] = len(chunks)
        elif prefix == TypeOfChunk.DATAXREF:
            # la valeur est une utilisation d'un label lors d'une instruction de saut
            if value not in xrefs:
                xrefs[value] = []
            # on enregistre la position des 4 octets qui suivent le prefix
            xrefs[value].append(len(chunks) + 1)
            # on écrit des 0 qu'on viendra modifier lors de l'étape 3 de la résolution des labels
            # encode le prefix et la valeur
            buf = struct.pack('>BI', TypeOfChunk.DATAINT, 0)
        elif prefix == TypeOfChunk.DATAOPCODE or prefix == TypeOfChunk.DATABYTE:
            # encode le prefix et la valeur. La valeur est sur un 'unsigned char'
            # TODO ...
            buf = struct.pack('B', prefix)
            buf += struct.pack('B', value)
            pass
        elif prefix == TypeOfChunk.DATAINT:
            # encode le prefix et la valeur. La valeur est sur un entier signé sur 4 octet en big-endian
            # TODO ...
            buf = struct.pack('B', TypeOfChunk.DATAINT)
            buf += struct.pack('>I', value)
            pass
        elif prefix == TypeOfChunk.DATASTR:
            # on encode la chaîne de caractère sous forme de bloc d'octet en UTF-8
            btxt = value.encode("utf-8")
            # on calcul la taille de ce bloc d'octet
            n = len(btxt)
            # encode le prefix, n et la valeur de la chaine
            # TODO ...
            buf = struct.pack(f'BB{n}s', TypeOfChunk.DATASTR, n, btxt)
            pass
        # on concatène les morceaux d'octets
        if buf is not None:
            chunks += buf
    # étape 3: traitement des références croisées
    # pour chaques labels utilisés en référence
    for xref in xrefs.keys():
        # si on fait reférence à un label qui n'existe pas
        if xref not in labels:
            raise ValueError(f"Unknown reference to label {xref}.")
        # on cherche l'adresse associé au label
        adr = labels[xref]
        # pour chaque référence à ce label
        for adr_to_mod in xrefs[xref]:
            # on stocke l'adresse dans le buffer global
            # on tient compte de la taille de l'instruction contenant la XREF car l'adresse est appliqué après la lecture de l'instruction
            struct.pack_into(">i", chunks, adr_to_mod, (adr - 4 - adr_to_mod))
    # on convertie notre 'bytearray' (modifiable) en 'bytes' (non-modifiable) en sortant
    return bytes(chunks)
