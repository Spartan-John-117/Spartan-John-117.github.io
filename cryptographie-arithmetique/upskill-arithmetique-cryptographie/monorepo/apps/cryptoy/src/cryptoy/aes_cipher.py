from cryptography.hazmat.primitives.ciphers.aead import (
    AESGCM,
)


def encrypt(msg: bytes, key: bytes, nonce: bytes) -> bytes:
    # AES-GCM encryption using the provided key and nonce
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, msg, associated_data=None)
    return ciphertext


def decrypt(msg: bytes, key: bytes, nonce: bytes) -> bytes:
    # AES-GCM decryption using the provided key and nonce
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, msg, associated_data=None)
    return plaintext
