"""Generación de claves para DES, 3DES y AES.

DES usa una clave de 64 bits (8 bytes), donde 8 bits son de paridad,
y de ahí genera 16 subclaves de 48 bits para las 16 rondas.
"""


def _permute(data: int, table: list[int], input_bits: int) -> int:
    """Aplica una permutación según una tabla (índices 1-based de la especificación DES)."""
    result = 0
    for pos in table:
        bit = (data >> (input_bits - pos)) & 1
        result = (result << 1) | bit
    return result


def _left_rotate_28(value: int, shifts: int) -> int:
    """Rotación circular izquierda para valores de 28 bits."""
    return ((value << shifts) | (value >> (28 - shifts))) & 0x0FFFFFFF


def generate_des_subkeys(key: bytes) -> list[int]:
    """Genera las 16 subclaves DES (48 bits cada una).

    Args:
        key: clave de 8 bytes (64 bits, incluye paridad)

    Returns:
        Lista de 16 enteros (cada uno representa una subclave de 48 bits)
    """
    if not isinstance(key, bytes):
        raise TypeError("key debe ser de tipo bytes")
    if len(key) != 8:
        raise ValueError("key debe tener exactamente 8 bytes")

    key_int = int.from_bytes(key, "big")

    # PC-1: 64 -> 56 bits (descarta bits de paridad)
    permuted_key = _permute(key_int, PC1, 64)

    # Separar en C y D (28 bits cada uno)
    c = (permuted_key >> 28) & 0x0FFFFFFF
    d = permuted_key & 0x0FFFFFFF

    subkeys: list[int] = []

    for shifts in KEY_SHIFTS:
        c = _left_rotate_28(c, shifts)
        d = _left_rotate_28(d, shifts)
        cd = (c << 28) | d

        # PC-2: 56 -> 48 bits
        subkey = _permute(cd, PC2, 56)
        subkeys.append(subkey)

    return subkeys


def generate_3des_subkeys(key: bytes) -> list[list[int]]:
    """Genera subclaves para 3DES a partir de una llave de 16 o 24 bytes.

    - 16 bytes: modo 2-key (K1, K2, K1)
    - 24 bytes: modo 3-key (K1, K2, K3)

    Returns:
        Lista con 3 elementos; cada elemento es una lista de 16 subclaves DES.
    """
    if not isinstance(key, bytes):
        raise TypeError("key debe ser de tipo bytes")
    if len(key) not in (16, 24):
        raise ValueError("key para 3DES debe tener 16 o 24 bytes")

    if len(key) == 16:
        k1 = key[:8]
        k2 = key[8:16]
        k3 = k1
    else:
        k1 = key[:8]
        k2 = key[8:16]
        k3 = key[16:24]

    return [
        generate_des_subkeys(k1),
        generate_des_subkeys(k2),
        generate_des_subkeys(k3),
    ]


def _rot_word(word: int) -> int:
    """Rota una palabra de 32 bits a la izquierda por 8 bits."""
    return ((word << 8) & 0xFFFFFFFF) | (word >> 24)


def _sub_word(word: int) -> int:
    """Aplica S-Box AES byte a byte a una palabra de 32 bits."""
    b0 = AES_SBOX[(word >> 24) & 0xFF]
    b1 = AES_SBOX[(word >> 16) & 0xFF]
    b2 = AES_SBOX[(word >> 8) & 0xFF]
    b3 = AES_SBOX[word & 0xFF]
    return (b0 << 24) | (b1 << 16) | (b2 << 8) | b3


def generate_aes_round_keys(key: bytes) -> list[bytes]:
    """Genera round keys para AES-128/192/256.

    Args:
        key: 16, 24 o 32 bytes.

    Returns:
        Lista de round keys de 16 bytes (Nr + 1 llaves).
        - AES-128: 11 round keys
        - AES-192: 13 round keys
        - AES-256: 15 round keys
    """
    if not isinstance(key, bytes):
        raise TypeError("key debe ser de tipo bytes")
    if len(key) not in (16, 24, 32):
        raise ValueError("key para AES debe tener 16, 24 o 32 bytes")

    nk = len(key) // 4
    nr_map = {4: 10, 6: 12, 8: 14}
    nr = nr_map[nk]
    nb = 4

    words = [int.from_bytes(key[i:i + 4], "big") for i in range(0, len(key), 4)]

    for i in range(nk, nb * (nr + 1)):
        temp = words[i - 1]
        if i % nk == 0:
            temp = _sub_word(_rot_word(temp)) ^ (AES_RCON[(i // nk) - 1] << 24)
        elif nk > 6 and i % nk == 4:
            temp = _sub_word(temp)
        words.append(words[i - nk] ^ temp)

    round_keys: list[bytes] = []
    for round_index in range(nr + 1):
        chunk = words[round_index * 4:(round_index + 1) * 4]
        round_key = b"".join(w.to_bytes(4, "big") for w in chunk)
        round_keys.append(round_key)

    return round_keys


# Permuted Choice 1 (PC-1): 64 -> 56
PC1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4,
]

# Permuted Choice 2 (PC-2): 56 -> 48
PC2 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32,
]

# Rotaciones por ronda
KEY_SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]


# AES S-Box
AES_SBOX = [
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
]

# RCON para expansión de llaves AES
AES_RCON = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]


if __name__ == "__main__":
    key_des = b"\x13\x34\x57\x79\x9B\xBC\xDF\xF1"
    subkeys_des = generate_des_subkeys(key_des)
    print("Subclaves DES (48 bits):")
    for i, k in enumerate(subkeys_des, start=1):
        print(f"K{i:02d}: {k:012X}")

    key_3des = b"\x01\x23\x45\x67\x89\xAB\xCD\xEF\x13\x34\x57\x79\x9B\xBC\xDF\xF1"
    subkeys_3des = generate_3des_subkeys(key_3des)
    print("\n3DES: cantidad de grupos de subclaves:", len(subkeys_3des))
    print("Subclaves por grupo:", len(subkeys_3des[0]))

    key_aes = b"\x2b\x7e\x15\x16\x28\xae\xd2\xa6\xab\xf7\x15\x88\x09\xcf\x4f\x3c"
    round_keys_aes = generate_aes_round_keys(key_aes)
    print("\nRound keys AES:", len(round_keys_aes))
    print("Round key 0:", round_keys_aes[0].hex().upper())
    print("Round key final:", round_keys_aes[-1].hex().upper())
