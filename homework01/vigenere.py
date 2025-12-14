def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    ciphertext = ""
    ALPHABET_SIZE = 26

    keyword = keyword.upper()
    key_length = len(keyword)

    for i, char in enumerate(plaintext):
        if char.isalpha():
            shift = ord(keyword[i % key_length]) - ord("A")
            base = ord("A") if char.isupper() else ord("a")
            shifted_char = chr((ord(char) - base + shift) % ALPHABET_SIZE + base)
            ciphertext += shifted_char
        else:
            ciphertext += char

    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    plaintext = ""
    ALPHABET_SIZE = 26

    keyword = keyword.upper()
    key_length = len(keyword)

    for i, char in enumerate(ciphertext):
        if char.isalpha():
            shift = ord(keyword[i % key_length]) - ord("A")
            base = ord("A") if char.isupper() else ord("a")
            original_char = chr((ord(char) - base - shift) % ALPHABET_SIZE + base)
            plaintext += original_char
        else:
            plaintext += char

    return plaintext
