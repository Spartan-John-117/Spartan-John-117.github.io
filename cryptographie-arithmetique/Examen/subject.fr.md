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
sig = b'O\ty\x9fjY\x08\x1brU\x99u30\xb7\xa2D\n\xbcB`f\x01b/\xe0\xc5\x82dn2US\x03\xe1\
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

def compute_phi_d(p: int, q: int, e: int) -> (int, int):
     """
     Calcul le paramètre phi et d
     """

 # Paramètres RSA
 e = 0x10001
 p = 0xc36d0eb7fcd285223cfb5aaba5bda3d82c01cad19ea484a87ea4377637e75500fcb2005c5c7dd6\
     ec4ac023cda285d796c3d9e75e1efc42488bb4f1d13ac30a57
 q = 0xc000df51a7c77ae8d7c7370c1ff55b69e211c2b9e5db1ed0bf61d0d9899620f4910e4168387e3c\
     30aa1e00c339a795088452dd96a9a5ea5d9dca68da636032af

 import chiffrement as c
 phi, d = c.compute_phi_d(p, q, e)
 assert phi = 10292643285824947933653104794242355990273757824509949328589582372336151\
     54622736586226471313136130909571888451324450634203735646789600225457870437832613\
     39041149629958046790954967148370818329055950867779233478060890056194478338788042\
     671388894204595205529875228355199084054054384724525486265498322768079319585396
 assert d =25805029499273649922616867551794581881408687430691514322910024560150038307\
     53037955397279421722045100504401962816736861711945986602975617513506746422276060\
     52326101261984348105812779785604462321792072948194955218957918936093135881460721\
     97246146080898150073696951405712041933069798872061046865174502987797734221 


Écrire la fonction compute_sp_sq_qinv, tel que:

def compute_sp_sq_qinv(msg: int, p: int, q: int, e: int) -> (int, int, int):
    """
    Retrouver le parmètre sp, sq et qinv utile pour RSA-CRT
    """

import chiffrement as c
sp, sq, qinv = c.compute_sp_sq(msg, p, q, e)


Écrire la fonction sig_crt, tel que:

def sig_crt(msg: int, p: int, q: int, e: int) -> int:
    """
    Calcule la signature du message via RSA-CRT à partir de p, q et e
    """

import chiffrement as c
s = int.from_bytes(sig, byteorder='big')
s_crt = c.sig_crt(msg, p, q, e)

assert s == s_crt


Documentation: gmpy2
2- Injection de fautes
A la suite du code d'injection de faute suivant:

# Injection de fautes (bit flip) dans sp (entre 1 et 20 fautes)
from random import Random
seed = 2600
rd = Random()
rd.seed(seed)
# Inversion arbitraire de bits dans sp, et calcul de la signature corrompue
# et Récupération des indices de bits fautés
bits = sorted(rd.sample(range(0, sp.bit_length()), rd.randint(1,20)))
# Conversion vers des "large int"
faults = sum([1 << x for x in bits])
# on injectera les fautes typiquements sur le paramètre sp de la manière suivante
sp_x = sp ^ faults


Implémenter la fonction sig_crt_faulted, tel que:

def sig_crt_faulted(msg: int, p: int, q: int, e: int, seed: int) -> int:
    """
    Retourne la signature fauté à partir de p, q, e avec la seed utilisé
    pour fauter le paramètre sp
    """

import chiffrement as c
s_crt_x = c.sig_crt_faulted(msg, p, q, e, 2600)


3- Exploitation des fautes - Bellcore #1
Implémenter la fonction bellcore_1, tel que:

def bellcore_1(s_crt: int, s_crt_x: int, N: int) -> (int, int):
    """
    Retrouver p et q à partir de la signature correcte et fautée (DFA)
    """

import chiffrement as c
p, q = c.bellcore_1(s_crt, s_crt_x, N)
assert p * q == N


4- Exploitation des fautes - Bellcore #2
Implémenter la fonction bellcore_2, tel que:

def bellcore_2(msg: int, s_crt_x: int, e: int, N: int) -> (int, int):
    """
    Retrouver p et q à partir de la signature fautée seulement (SFA)
    """

import chiffrement as c
p, q = c.bellcore_2(msg, s_crt_x, e, N)
assert p * q == N


bellcore_2 est une attaque à message clair connu donc vous disposez du
msg au moment d'insérer les fautes
5- Retrouvez la clef privé
Implémenter la fonction found_priv_key, tel que:

def found_priv_key(p, q, e) -> int:
    """
    Retrouver d la clef privé à partir de p et q obtenu par bellcore_1 ou bellcore_2
    """

from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import PKCS1_v1_5 
from gmpy2 import invert
import chiffrement as c

p, q = c.bellcore_1(s_crt, s_crt_x, N)
d = c.found_priv_key(p, q, e)
pinv = invert(p, q)

hckRSA = RSA.RsaKey(n=N, e=e, d=d, p=p2, q=q2, u=pinv)
signer = PKCS1_v1_5.new(hckRSA) 
assert True = signer.verify(hash_object, sig)
