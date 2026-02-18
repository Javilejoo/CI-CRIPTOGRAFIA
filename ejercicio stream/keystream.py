import random
import hashlib

def string_to_ascii(s):
    lista = []
    for char in s:
        lista.append(ord(char))
    return lista

def generar_keystream(seed: str, longitud: int, mensaje: str = "", nonce: str = "") -> bytes:
    """
    Genera un keystream pseudoaleatorio determinístico.
    
    ⚠️ IMPORTANTE: Este PRNG (Mersenne Twister) es educativo, NO es criptográficamente seguro.
    Para producción, usa: secrets.token_bytes(), os.urandom(), o ChaCha20/AES-CTR.

    Args:
        seed: Clave para inicializar el PRNG (se hashea con SHA-256)
        longitud: Longitud del keystream en bytes
        mensaje: Mensaje a cifrar (opcional). Si es más largo, ajusta la longitud.
        nonce: Valor único por encriptación (opcional). Previene reutilización de keystream.

    Returns:
        Keystream de la longitud especificada en formato bytes

    Requisitos cumplidos:
        ✓ Determinístico: mismo seed + nonce = mismo keystream
        ✓ PRNG básico: Mersenne Twister de Python
        ✓ Longitud variable: se ajusta al mensaje
        ✓ Aceptar seed: parámetro requerido
    """
    # Ajustar longitud según el mensaje
    if mensaje:
        longitud = max(longitud, len(mensaje))
    
    # Combinar seed + nonce para mayor seguridad
    # Hasheamos para evitar strings similares generen secuencias parecidas
    combined = f"{seed}:{nonce}".encode('utf-8')
    hash_seed = hashlib.sha256(combined).hexdigest()
    
    # Usar el hash como seed del PRNG para mejor distribución
    rng = random.Random(hash_seed)
    return bytes(rng.randrange(0, 256) for _ in range(longitud))


def keystream(seed: str, longitud: int, mensaje: str = "", nonce: str = ""):
    """
    Función wrapper para test y demostración.
    """
    ascii = string_to_ascii(mensaje)
    stream = generar_keystream(seed, longitud, mensaje, nonce)
    print(f"Mensaje en ASCII: {ascii}")
    print(f"Keystream ({len(stream)} bytes): {stream}")
    return stream


keystream("semilla", 10, "hola")#b'@"\x80\xb9\xf2\xd6\xed\x16"\x1e' keystream}
keystream("semilla", 10, "mundo")#b'@"\x80\xb9\xf2\xd6\xed\x16"\x1e' keystream}