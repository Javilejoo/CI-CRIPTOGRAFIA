import random
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from asciibin import string_to_ascii

def generar_keystream(seed: str, longitud: int, mensaje: str = "") -> bytes:
    """
    Genera un keystream pseudoaleatorio.

    Args:
        seed: Clave para inicializar el PRNG
        longitud: Longitud del keystream en bytes
        mensaje: Mensaje a cifrar

    Returns:
        Keystream de la longitud especificada
    """
    if mensaje:
        longitud = max(longitud, len(mensaje))

    rng = random.Random(seed)
    return bytes(rng.randrange(0, 256) for _ in range(longitud))


def keystream(seed: str, longitud: int, mensaje: str = ""):
    ascii = string_to_ascii(mensaje)
    stream = generar_keystream(seed, longitud, mensaje)
    print(f"Mensaje en ASCII: {ascii}")
    print(f"Keystream: {stream}")


keystream("semilla", 10, "hola")#b'@"\x80\xb9\xf2\xd6\xed\x16"\x1e' keystream