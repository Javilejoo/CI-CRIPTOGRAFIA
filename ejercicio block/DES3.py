"""Generación de subclaves para 3DES (solo key schedule)."""


def _permute(data: int, table: list[int], input_bits: int) -> int:
    result = 0
    for pos in table:
        bit = (data >> (input_bits - pos)) & 1
        result = (result << 1) | bit
    return result


def _left_rotate_28(value: int, shifts: int) -> int:
    return ((value << shifts) | (value >> (28 - shifts))) & 0x0FFFFFFF


def _generate_des_subkeys(key8: bytes) -> list[int]:
    if len(key8) != 8:
        raise ValueError("Cada segmento de llave DES debe tener 8 bytes")

    key_int = int.from_bytes(key8, "big")
    permuted_key = _permute(key_int, PC1, 64)

    c = (permuted_key >> 28) & 0x0FFFFFFF
    d = permuted_key & 0x0FFFFFFF

    subkeys: list[int] = []
    for shifts in KEY_SHIFTS:
        c = _left_rotate_28(c, shifts)
        d = _left_rotate_28(d, shifts)
        cd = (c << 28) | d
        subkeys.append(_permute(cd, PC2, 56))

    return subkeys


def generate_3des_subkeys(key: bytes) -> list[list[int]]:
    """Genera subclaves para 3DES.

    - key de 16 bytes: K1, K2, K1
    - key de 24 bytes: K1, K2, K3

    Retorna 3 listas, cada una con 16 subclaves DES de 48 bits.
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
        _generate_des_subkeys(k1),
        _generate_des_subkeys(k2),
        _generate_des_subkeys(k3),
    ]


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

KEY_SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]


if __name__ == "__main__":
    key = b"\x01\x23\x45\x67\x89\xAB\xCD\xEF\x13\x34\x57\x79\x9B\xBC\xDF\xF1"
    groups = generate_3des_subkeys(key)
    print("Grupos:", len(groups))
    print("Subclaves por grupo:", len(groups[0]))
    print("K1_01:", f"{groups[0][0]:012X}")
