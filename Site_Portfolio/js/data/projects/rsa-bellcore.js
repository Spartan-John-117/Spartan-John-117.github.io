window.projectData = window.projectData || {};
window.projectData["rsa-bellcore"] = {
    title: "Examen RSA-CRT / Bellcore",
    domain: "Cryptographie",
    technologies: ["Python", "PyCryptodome", "gmpy2", "Mathématiques"],
    content: `
L'objectif du projet est de compléter l'implementation du RSA en mode
"Reste Chinois" et d'illustrer une attaque "Bellcore". Les
différents modules pythons non-standard utilisés s'installent via un
pip install pycryptodomex pour Cryptodome et pip install gmpy2 pour gmpy2.
Il est attendu que vous fassiez dans votre code

import Cryptodome


Et que vous passiez par Cryptodome pour les différents sous-modules.
La correction suivra cette convention.

Partie 1:
Pour apprendre à maitriser le module PyCryptodome, nous allons vous
faire réaliser les fonctions suivantes
1- Dans le module chiffrement (vous rendez donc chiffrement.py), Vous implémenterez une
fonction hash_message, tel que:

def hash_message(m: bytes) -> Cryptodome.Hash.SHA256.SHA256Hash:
    """
    Fabrique et retourne une empreinte SHA256 de m avec PyCryptodome
    """


2- Dans le module chiffrement, vous implémenterez une
fonction rsa_new, tel que:

def rsa_new(N: int, e: int) -> Cryptodome.PublicKey.RSA.RsaKey:
    """
    Fabrique et retourne une empreinte clef RSA avec PyCryptodome
    """


3- Dans le module chiffrement, vous implémenterez une
fonction PKCS1_v1_5_sig_check, tel que:

def PKCS1_v1_5_sig_check(pub_key: Cryptodome.PublicKey.RSA.RsaKey, \
            hash_message: Cryptodome.Hash.SHA256.SHA256Hash, sig: bytes) -> bool:
    """
    Vérifie que la signature du message correspond bien à l'expéditeur
    """



# clé publique 
e = 0x10001
N = 0x9292758453063D803DD603D5E777D7888ED1D5BF35786190FA2F23EBC0848AEADDA92CA6C3D80B32\
    C4D109BE0F36D6AE7130B9CED7ACDF54CFC7555AC14EEBAB93A89813FBF3C4F8066D2D800F7C38A81A\
    E31942917403FF4946B0A83D3D3E05EE57C6F5F5606FB5D4BC6CD34EE0801A5E94BB77B07507233A0B\
    C7BAC8F90F79
sig = b'O\ty\x9fjY\x08\x1brU\x99u30\xb7\xa2D\n\xbcB\`f\x01b/\xe0\xc5\x82dn2US\x03\xe1\
    \x06*)\x89\xd9\xb4\xc2eC\x1a\xdbX\xdd\x85\xbb3\xc4\xbb#z1\x1b\xc4\x0c\x12yR\x8f\
    \xd6\xbb6\xf9OSJM\x82\x84\xa1\x8a\xb8\xe5g\x0esLU\xa6\xcc\xab_\xb5\xea\xe0+\xa3\
    ~-Vd\x8dz\x13\xbb\xf1z\x0e\x07\xd6\x07\xc0|\xbbr\xc7\xa7\xa7pv7n\x844\xcen\x13h2\
    \xdc\x95\xdb=\x80'

import chiffrement as c
assert True == c.PKCS1_v1_5_sig_check(c.rsa_new(N, e), \
                c.hash_message(b"Hello World!"), sig)


Documentation: PyCryptodome

Partie 2:
0- Signature du message avec padding
Le message est signé selon PKCS#1 v1.5, suivant la méthode de
rembourrage (padding) suivant : 0100message_hash| Ici, "ff..." est
une chaîne d'octets "ff" suffisamment longue pour que la taille du
message paddé soit la même que celle du modulo N, et "hash_prefix" est
un numéro d'identifiant pour la fonction de hachage utilisé sur
"message_hash". Ici, c'est SHA256 qui est utilisé, et il a le préfixe
"3031300d060960864801650304020105000420".
La fonction build_message ci-dessous implémente tout ce processus :

# Padding du PKCS#1 v1.5
def build_message(m, N):
    sha_id = "3031300d060960864801650304020105000420"
    N_len = (len(bin(N)) - 2 + 7) // 8
    pad_len = (len(hex(N)) - 2) // 2 - 3 - len(m)//2 - len(sha_id)//2
    padded_m = "0001" + "ff" * pad_len + "00" + sha_id + m
    return padded_m


Vous devrez la rajouter dans le module chiffrement.

import chiffrement as c
m = b"Hello World!"
# Encode message
hash_object = c.hash_message(m)
hashed_m = hexlify(hash_object.digest()).decode()
padded_m = c.build_message(hashed_m, N)
msg = int.from_bytes(unhexlify(padded_m), byteorder='big') 
print(f"Padded/hashed: {padded_m}")


1- Chinese Remainder Theorem
Nous allons vous faire implémtenter les différentes sous-fonctions vue
en cours.
En utilisant, gmpy2, écrire la fonction
compute_phi_d, tel que:


[... Documentation tronquée pour l'affichage ...]
`
};