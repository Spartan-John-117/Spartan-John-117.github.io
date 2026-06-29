from cryptoy.utils import (
    str_to_unicodes,
    unicodes_to_str,
)

# TP: Chiffrement de César


def encrypt(msg: str, shift: int) -> str:
    unicodes = str_to_unicodes(msg)
    shifted = [(x + shift) % 0x110000 for x in unicodes]
    return unicodes_to_str(shifted)


def decrypt(msg: str, shift: int) -> str:
    return encrypt(msg, -shift)


def attack() -> tuple[str, int]:
    s = "恱恪恸急恪恳恳恪恲恮恸急恦恹恹恦恶恺恪恷恴恳恸急恵恦恷急恱恪急恳恴恷恩怱急恲恮恳恪恿急恱恦急恿恴恳恪"

    for shift in range(0x110000):
        decrypted = decrypt(s, shift)
        if "ennemis" in decrypted:
            return decrypted, shift

    raise RuntimeError("Failed to attack")
