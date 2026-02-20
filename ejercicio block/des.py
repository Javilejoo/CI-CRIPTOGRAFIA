"""Generación de subclaves de DES (Key Schedule).

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


if __name__ == "__main__":
    key = b"\x13\x34\x57\x79\x9B\xBC\xDF\xF1"
    subkeys = generate_des_subkeys(key)

    print("Subclaves DES (48 bits):")
    for i, k in enumerate(subkeys, start=1):
        print(f"K{i:02d}: {k:012X}")
