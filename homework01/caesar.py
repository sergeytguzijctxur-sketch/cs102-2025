def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    ciphertext = ""

    for char in plaintext:
        if char.isalpha():
            base = ord("A") if char.isupper() else ord("a")
            shifted_char = chr((ord(char) - base + shift) % 26 + base)
            ciphertext += shifted_char
        else:
            ciphertext += char

    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    plaintext = ""

    for char in ciphertext:
        if char.isalpha():
            base = ord("A") if char.isupper() else ord("a")
            original_char = chr((ord(char) - base - shift) % 26 + base)
            plaintext += original_char
        else:
            plaintext += char

    return plaintext
