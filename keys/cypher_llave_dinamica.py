"""
Cifrador ASCII con Llave Dinámica
==================================
La llave cambia en cada posición según la fórmula: k_i = k_0 + i

Cifrado:   C_i = (ASCII_i + k_i) mod 128
Descifrado: ASCII_i = (C_i - k_i) mod 128

Donde k_i = k_0 + i (posición)
"""


def generar_llave_dinamica(k0: int, longitud: int) -> list:
    """
    Genera la llave dinámica basada en la posición.
    
    Fórmula: k_i = k_0 + i
    
    Args:
        k0: Valor base de la llave (seed)
        longitud: Longitud del mensaje
        
    Returns:
        Lista de llaves [k_0, k_1, k_2, ..., k_n]
    """
    return [k0 + i for i in range(longitud)]


def cifrar_dinamico(mensaje: str, k0: int) -> tuple:
    """
    Cifra un mensaje con llave dinámica.
    
    Fórmula: C_i = (ASCII_i + k_i) mod 128
    Donde: k_i = k_0 + i
    
    Args:
        mensaje: Texto a cifrar
        k0: Valor base de la llave (seed)
        
    Returns:
        Tupla (mensaje_cifrado, ascii_original, ascii_cifrado, llave_dinamica)
    """
    ascii_original = [ord(c) for c in mensaje]
    llave_dinamica = generar_llave_dinamica(k0, len(mensaje))
    
    ascii_cifrado = []
    for i, valor in enumerate(ascii_original):
        cifrado = (valor + llave_dinamica[i]) % 128
        ascii_cifrado.append(cifrado)
    
    mensaje_cifrado = "".join(chr(c) for c in ascii_cifrado)
    
    return mensaje_cifrado, ascii_original, ascii_cifrado, llave_dinamica


def descifrar_dinamico(mensaje_cifrado: str, k0: int) -> tuple:
    """
    Descifra un mensaje con llave dinámica.
    
    Fórmula: ASCII_i = (C_i - k_i) mod 128
    Donde: k_i = k_0 + i
    
    Args:
        mensaje_cifrado: Texto cifrado
        k0: Valor base de la llave (seed)
        
    Returns:
        Tupla (mensaje_descifrado, ascii_cifrado, ascii_descifrado, llave_dinamica)
    """
    ascii_cifrado = [ord(c) for c in mensaje_cifrado]
    llave_dinamica = generar_llave_dinamica(k0, len(mensaje_cifrado))
    
    ascii_descifrado = []
    for i, valor in enumerate(ascii_cifrado):
        descifrado = (valor - llave_dinamica[i]) % 128
        ascii_descifrado.append(descifrado)
    
    mensaje_descifrado = "".join(chr(c) for c in ascii_descifrado)
    
    return mensaje_descifrado, ascii_cifrado, ascii_descifrado, llave_dinamica


# =============================================================================
# PROGRAMA PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("   CIFRADOR ASCII - LLAVE DINÁMICA")
    print("   k_i = k_0 + i")
    print("="*60)
    
    while True:
        # Input seed (k0)
        entrada_k = input("\nIngresa la seed (k_0) [o 'salir']: ")
        if entrada_k.lower() == 'salir':
            print("\n¡Hasta luego!")
            break
        
        k0 = int(entrada_k)
        
        # Input mensaje
        mensaje = input("Ingresa el mensaje: ")
        
        # Cifrar
        mensaje_cifrado, ascii_orig, ascii_cif, llave = cifrar_dinamico(mensaje, k0)
        
        # Descifrar (para verificar)
        mensaje_descifrado, _, _, _ = descifrar_dinamico(mensaje_cifrado, k0)
        
        # Mostrar resultados
        print(f"\n{'='*50}")
        print(f"Mensaje original:    '{mensaje}'")
        print(f"Mensaje en ASCII:    {ascii_orig}")
        print(f"Llave dinámica:      {llave}")
        print(f"Mensaje cifrado:     '{mensaje_cifrado}'")
        print(f"ASCII cifrado:       {ascii_cif}")
        print(f"Mensaje descifrado:  '{mensaje_descifrado}'")
        print(f"{'='*50}")
