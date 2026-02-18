"""
Archivo de Validación y Pruebas para Stream Cipher XOR

Ejemplos de Entrada/Salida mostrando:
- Texto plano original
- Clave utilizada
- Texto cifrado (hexadecimal)
- Texto descifrado
"""

import sys
import os

# Importar funciones del archivo keystream.py
sys.path.insert(0, os.path.dirname(__file__))
from keystream import generar_keystream, cifrar, descifrar


def main():
    """Ejecuta los 3 ejemplos."""
    
    # EJEMPLO 1
    print("Ejemplo 1:")
    msg1 = "Hola"
    clave1 = "secreto"
    nonce1 = "2026-02-17"
    cifrado1 = cifrar(msg1, clave1, nonce1)
    descifrado1 = descifrar(cifrado1, clave1, nonce1)
    print(f"  Texto plano original: '{msg1}'")
    print(f"  Clave utilizada: '{clave1}'")
    print(f"  Texto cifrado (hex): {cifrado1.hex()}")
    print(f"  Texto descifrado: '{descifrado1}'")
    print()
    
    # EJEMPLO 2
    print("Ejemplo 2:")
    msg2 = "Criptografia Stream"
    clave2 = "claveFuerte123"
    nonce2 = "2026-02-17T10:30:00"
    cifrado2 = cifrar(msg2, clave2, nonce2)
    descifrado2 = descifrar(cifrado2, clave2, nonce2)
    print(f"  Texto plano original: '{msg2}'")
    print(f"  Clave utilizada: '{clave2}'")
    print(f"  Texto cifrado (hex): {cifrado2.hex()}")
    print(f"  Texto descifrado: '{descifrado2}'")
    print()
    
    # EJEMPLO 3
    print("Ejemplo 3:")
    msg3 = "¡Hola Mundo! 2026"
    clave3 = "otro_secreto"
    nonce3 = "ejemplo_especial"
    cifrado3 = cifrar(msg3, clave3, nonce3)
    descifrado3 = descifrar(cifrado3, clave3, nonce3)
    print(f"  Texto plano original: '{msg3}'")
    print(f"  Clave utilizada: '{clave3}'")
    print(f"  Texto cifrado (hex): {cifrado3.hex()}")
    print(f"  Texto descifrado: '{descifrado3}'")


if __name__ == "__main__":
    main()
