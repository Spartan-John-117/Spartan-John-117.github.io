from math import (
    gcd,
)

from cryptoy.utils import (
    str_to_unicodes,
    unicodes_to_str,
)

# TP: Chiffrement affine


def compute_permutation(a: int, b: int, n: int) -> list[int]:
    return [(a * i + b) % n for i in range(n)]


def compute_inverse_permutation(a: int, b: int, n: int) -> list[int]:
    perm = compute_permutation(a, b, n)
    result = [0] * n
    for i, j in enumerate(perm):
        result[j] = i
    return result


def encrypt(msg: str, a: int, b: int) -> str:
    n = 0x110000
    perm = compute_permutation(a, b, n)
    unicodes = str_to_unicodes(msg)
    encrypted = [perm[code] for code in unicodes]
    return unicodes_to_str(encrypted)


def encrypt_optimized(msg: str, a: int, b: int) -> str:
    n = 0x110000
    unicodes = str_to_unicodes(msg)
    encrypted = [(a * code + b) % n for code in unicodes]
    return unicodes_to_str(encrypted)


def decrypt(msg: str, a: int, b: int) -> str:
    n = 0x110000
    inv_perm = compute_inverse_permutation(a, b, n)
    unicodes = str_to_unicodes(msg)
    decrypted = [inv_perm[code] for code in unicodes]
    return unicodes_to_str(decrypted)


def decrypt_optimized(msg: str, a_inverse: int, b: int) -> str:
    n = 0x110000
    unicodes = str_to_unicodes(msg)
    decrypted = [(a_inverse * (code - b)) % n for code in unicodes]
    return unicodes_to_str(decrypted)


def compute_affine_keys(n: int) -> list[int]:
    return [a for a in range(1, n) if gcd(a, n) == 1]


def compute_affine_key_inverse(a: int, affine_keys: list, n: int) -> int:
    for a_inv in affine_keys:
        if (a * a_inv) % n == 1:
            return a_inv
    raise RuntimeError(f"{a} has no inverse")


def attack() -> tuple[str, tuple[int, int]]:
    s = "࠾ੵΚઐ௯ஹઐૡΚૡೢఊஞ௯\u0c5bૡీੵΚ៚Κஞїᣍફ௯ஞૡΚր\u05ecՊՊΚஞૡΚՊեԯՊ؇ԯրՊրր"
    n = 0x110000
    b = 58
    affine_keys = compute_affine_keys(n)

    for a in affine_keys:
        try:
            decrypted = decrypt(s, a, b)
            if "bombe" in decrypted:
                return decrypted, (a, b)
        except Exception:
            continue

    raise RuntimeError("Failed to attack")


def attack_optimized() -> tuple[str, tuple[int, int]]:
    s = (
        "જഏ൮ൈ\u0c51ܲ೩\u0c51൛൛అ౷\u0c51ܲഢൈᘝఫᘝా\u0c51\u0cfc൮ܲఅܲᘝ൮ᘝܲాᘝఫಊಝ"
        "\u0c64\u0c64ൈᘝࠖܲೖఅܲఘഏ೩ఘ\u0c51ܲ\u0c51൛൮ܲఅ\u0cfc\u0cfcඁೖᘝ\u0c51"
    )
    n = 0x110000
    affine_keys = compute_affine_keys(n)

    for a in affine_keys:
        try:
            a_inv = compute_affine_key_inverse(a, affine_keys, n)
            for b in range(n):
                decrypted = decrypt_optimized(s, a_inv, b)
                if "bombe" in decrypted:
                    return decrypted, (a, b)
        except Exception:
            continue

    raise RuntimeError("Failed to attack")