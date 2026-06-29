LEXEMES = r"""(?umx)                                                    # Le r permet de ne pas avoir à doubler les /
                                                                        # Espaces
    (?P<spaces>\s+)

                                                                        # Commentaires
    | (?P<comments>
        /\*[\s\S]*?\*/                                                  # Commentaire multi-ligne, incluant les sauts de ligne
        | //.*?$                                                        # Commentaire mono-ligne
    )

                                                                        # Mots-clés
    | (?P<keywords>
        \b(?:int|float|char|double|if|else|while|for|return|void|static|struct)\b
    )

                                                                        # Identifiants
    | (?P<identifiers>
        [a-zA-Z_]\w*
    )
    
                                                                        # Littéraux de caractères
    | (?P<characters>
        '(\\.|[^\\'])'                                                  # Caractères entre guillemets simples
    )

                                                                        # Constantes
    | (?P<constants>
        \b\d+(\.\d*|\.)([eE][+-]?\d+)?                                  # Nombres décimaux, y compris avec un point seul
        | \b\d+([uU]|[lL]|[uU][lL]|[lL][uU])?\b                         # Nombres entiers avec suffixes
        | 0[bB][01]+([uU]|[lL]|[uU][lL]|[lL][uU])?                      # Constantes binaires
        | 0[xX][0-9a-fA-F]+([uU]{1,2}|[lL]{1,2}|[uU][lL]|[lL][uU])?     # Hexadécimal
    )

                                                                        # Chaînes de caractères
    | (?P<strings>
        \"(\\.|[^\\"])*\"                                               # Chaîne de caractères entre guillemets doubles
    )

    | (?P<operators>
        \+= | -= | \*= | /=                                             # Affectations augmentées
        | \+\+ | --                                                     # Incrément et décrément
        | == | != | >= | <=                                             # Comparateurs
        | && | \|\|                                                     # Opérateurs logiques
        | >>= | <<=                                                     # Décalages et assignations
        | >> | <<                                                       # Décalages
        | \|=                                                           # OU bit à bit avec affectation
        | [&|~^]                                                        # Bitwise
    )

                                                                        # Symboles
    | (?P<symbols>
        [\[\](){}.,:;#]                                                 # Symboles simples
        | =                                                     
        | \* (?=\S)                                                     # Étoile non suivie d'un égal
    )
"""
