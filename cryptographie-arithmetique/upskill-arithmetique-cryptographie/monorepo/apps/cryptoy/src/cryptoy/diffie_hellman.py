import random
import sys

from cryptoy.utils import (
    pow_mod,
)

sys.setrecursionlimit(5000)  # Required for pow_mod for large exponents


def keygen(prime_number: int, generator: int) -> dict[str, int]:
    # 1. Tirer une clé privée aléatoire
    private_key = random.randint(2, prime_number - 1)
    
    # 2. Calculer la clé publique
    public_key = pow_mod(generator, private_key, prime_number)
    
    # 3. Retourner les deux dans un dictionnaire
    return {"public_key": public_key, "private_key": private_key}


def compute_shared_secret_key(public: int, private: int, prime_number: int) -> int:
    # Calcul de la clé secrète partagée
    return pow_mod(public, private, prime_number)