import random
import hashlib
from datetime import datetime

def string_to_ascii(s):
    lista = []
    for char in s:
        lista.append(ord(char))
    return lista

def generar_keystream(seed: str, longitud: int, mensaje: str = "", nonce: str = "") -> bytes:
    """
    Genera un keystream pseudoaleatorio deterministico.

    Args:
        seed: Clave para inicializar el PRNG
        longitud: Longitud del keystream en bytes
        mensaje: Mensaje a cifrar 

    Returns:
        Keystream de la longitud especificada en formato bytes
    """
    # Ajustar longitud dependiendoel mensaje
    if mensaje:
        longitud = max(longitud, len(mensaje))
    
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


def cifrar(mensaje: str, clave: str, nonce: str = "") -> bytes:
    """
    Cifra un mensaje usando XOR con un keystream.
    
    Args:
        mensaje: Texto plano a cifrar (string)
        clave: Clave para generar el keystream
        nonce: Valor único opcional (previene reutilización con misma clave)
    
    Returns:
        Mensaje cifrado en bytes
        
    Proceso:
        1. Convertir mensaje a bytes (ASCII)
        2. Generar keystream con la clave
        3. Aplicar XOR byte a byte: cifrado[i] = mensaje[i] XOR keystream[i]
    """
    # Convertir mensaje a bytes
    mensaje_bytes = mensaje.encode('utf-8')
    
    # Generar keystream de la misma longitud que el mensaje
    keystream_bytes = generar_keystream(clave, len(mensaje_bytes), mensaje, nonce)
    
    # Aplicar XOR bit a bit
    cifrado = bytes(mensaje_bytes[i] ^ keystream_bytes[i] for i in range(len(mensaje_bytes)))
    
    return cifrado


def descifrar(mensaje_cifrado: bytes, clave: str, nonce: str = "") -> str:
    """
    Descifra un mensaje que fue cifrado con la función cifrar().
    
    Args:
        mensaje_cifrado: Mensaje cifrado en bytes
        clave: Clave que se usó para cifrar
        nonce: Mismo valor único que se usó al cifrar
    
    Returns:
        Mensaje original en texto plano
        
    Nota: La operación XOR es reversible: if C = M XOR K, then M = C XOR K
    """
    # Generar el mismo keystream
    keystream_bytes = generar_keystream(clave, len(mensaje_cifrado), "", nonce)
    
    # Aplicar XOR de nuevo para recuperar el mensaje original
    mensaje_descifrado = bytes(mensaje_cifrado[i] ^ keystream_bytes[i] for i in range(len(mensaje_cifrado)))
    
    return mensaje_descifrado.decode('utf-8')




def demostrar_cifrado(mensaje: str, clave: str, nonce: str = None):
    """
    Demuestra el cifrado y descifrado de mensajes.
    
    Args:
        mensaje: Mensaje a cifrar (editable por el usuario)
        clave: Clave secreta (debe proporcionar el usuario)
        nonce: Generado automáticamente con timestamp si no se proporciona
    """
    # Generar nonce automáticamente si no se proporciona
    if nonce is None:
        nonce = datetime.now().isoformat()
    
    ks = generar_keystream(clave, len(mensaje), mensaje, nonce)
    cifrado = cifrar(mensaje, clave, nonce)
    descifrado = descifrar(cifrado, clave, nonce)
    
    print(f"Mensaje:         '{mensaje}'")
    print(f"Keystream:       {ks.hex()}")
    print(f"Mensaje cifrado: {cifrado.hex()}")
    print(f"Mensaje descifrado: '{descifrado}'")


# Valores fijos
mensaje = "que tal"
clave = "profe"
nonce = "2026-02-17"  # Nonce fija para que el keystream siempre sea igual

# Ejecutar con parámetros fijos
demostrar_cifrado(mensaje, clave, nonce)
