import Cryptodome
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import PKCS1_v1_5
import gmpy2
from random import Random

def hash_message(m: bytes) -> Cryptodome.Hash.SHA256.SHA256Hash:
    """
    Fabrique et retourne une empreinte SHA256 de m avec PyCryptodome
    """
    return SHA256.new(m)

def rsa_new(N: int, e: int) -> Cryptodome.PublicKey.RSA.RsaKey:
    """
    Fabrique et retourne une empreinte clef RSA avec PyCryptodome
    """
    return RSA.construct((N, e))

def PKCS1_v1_5_sig_check(pub_key: Cryptodome.PublicKey.RSA.RsaKey, \
            hash_message: Cryptodome.Hash.SHA256.SHA256Hash, sig: bytes) -> bool:
    """
    Vérifie que la signature du message correspond bien à l'expéditeur
    """
    verifier = PKCS1_v1_5.new(pub_key)
    return verifier.verify(hash_message, sig)

# Padding du PKCS#1 v1.5
def build_message(m, N):
    sha_id = "3031300d060960864801650304020105000420"
    N_len = (len(bin(N)) - 2 + 7) // 8
    pad_len = (len(hex(N)) - 2) // 2 - 3 - len(m)//2 - len(sha_id)//2
    padded_m = "0001" + "ff" * pad_len + "00" + sha_id + m
    return padded_m

def compute_phi_d(p: int, q: int, e: int):
    """
    Calcul le paramètre phi et d
    """
    phi = (p - 1) * (q - 1)
    d = int(gmpy2.invert(e, phi))
    return phi, d

def compute_sp_sq_qinv(msg: int, p: int, q: int, e: int):
    """
    Retrouver le parmètre sp, sq et qinv utile pour RSA-CRT
    """
    phi, d = compute_phi_d(p, q, e)
    dp = d % (p - 1)
    dq = d % (q - 1)
    sp = int(gmpy2.powmod(msg, dp, p))
    sq = int(gmpy2.powmod(msg, dq, q))
    qinv = int(gmpy2.invert(q, p))
    return sp, sq, qinv

# Alias pour correspondre à l'appel dans le sujet
compute_sp_sq = compute_sp_sq_qinv

def sig_crt(msg: int, p: int, q: int, e: int) -> int:
    """
    Calcule la signature du message via RSA-CRT à partir de p, q et e
    """
    sp, sq, qinv = compute_sp_sq_qinv(msg, p, q, e)
    h = (qinv * (sp - sq)) % p
    s = sq + h * q
    return s

def sig_crt_faulted(msg: int, p: int, q: int, e: int, seed: int) -> int:
    """
    Retourne la signature fauté à partir de p, q, e avec la seed utilisé
    pour fauter le paramètre sp
    """
    sp, sq, qinv = compute_sp_sq_qinv(msg, p, q, e)
    
    rd = Random()
    rd.seed(seed)
    bits = sorted(rd.sample(range(0, sp.bit_length()), rd.randint(1,20)))
    faults = sum([1 << x for x in bits])
    sp_x = sp ^ faults
    
    h = (qinv * (sp_x - sq)) % p
    s_x = sq + h * q
    return s_x

def bellcore_1(s_crt: int, s_crt_x: int, N: int):
    """
    Retrouver p et q à partir de la signature correcte et fautée (DFA)
    """
    q = int(gmpy2.gcd(abs(s_crt - s_crt_x), N))
    p = N // q
    return p, q

def bellcore_2(msg: int, s_crt_x: int, e: int, N: int):
    """
    Retrouver p et q à partir de la signature fautée seulement (SFA)
    """
    val = int(gmpy2.powmod(s_crt_x, e, N))
    diff = abs(val - msg) % N
    q = int(gmpy2.gcd(diff, N))
    p = N // q
    return p, q

def found_priv_key(p: int, q: int, e: int) -> int:
    """
    Retrouver d la clef privé à partir de p et q obtenu par bellcore_1 ou bellcore_2
    """
    phi, d = compute_phi_d(p, q, e)
    return d
