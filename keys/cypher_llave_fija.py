"""
Cifrador ASCII tipo César Generalizado - Llave Fija
====================================================
Cifra y descifra mensajes usando desplazamiento ASCII con llave fija.

Cifrado:   C = (ASCII + k) mod 128
Descifrado: ASCII = (C - k) mod 128
"""

# Configuración
LLAVE_FIJA = 100  # Valor k fijo


def cesar_cifrar(mensaje: str, k: int = LLAVE_FIJA) -> tuple:
    """
    Cifra un mensaje usando César generalizado en ASCII.
    
    Fórmula: C = (ASCII + k) mod 128
    
    Args:
        mensaje: Texto a cifrar
        k: Llave de desplazamiento (por defecto 100)
        
    Returns:
        Tupla (mensaje_cifrado, ascii_original, ascii_cifrado)
    """
    ascii_original = [ord(c) for c in mensaje]
    ascii_cifrado = [(valor + k) % 128 for valor in ascii_original]
    mensaje_cifrado = "".join(chr(c) for c in ascii_cifrado)
    
    return mensaje_cifrado, ascii_original, ascii_cifrado


def cesar_descifrar(mensaje_cifrado: str, k: int = LLAVE_FIJA) -> tuple:
    """
    Descifra un mensaje usando César generalizado en ASCII.
    
    Fórmula: ASCII = (C - k) mod 128
    
    Args:
        mensaje_cifrado: Texto cifrado
        k: Llave de desplazamiento (por defecto 100)
        
    Returns:
        Tupla (mensaje_descifrado, ascii_cifrado, ascii_descifrado)
    """
    ascii_cifrado = [ord(c) for c in mensaje_cifrado]
    ascii_descifrado = [(valor - k) % 128 for valor in ascii_cifrado]
    mensaje_descifrado = "".join(chr(c) for c in ascii_descifrado)
    
    return mensaje_descifrado, ascii_cifrado, ascii_descifrado


def mostrar_proceso_cifrado(mensaje: str, k: int = LLAVE_FIJA):
    """
    Muestra el proceso completo de cifrado paso a paso.
    """
    mensaje_cifrado, ascii_orig, ascii_cif = cesar_cifrar(mensaje, k)
    
    print(f"\n{'='*50}")
    print("CIFRADO CÉSAR ASCII")
    print(f"{'='*50}")
    print(f"Llave k = {k}")
    print(f"Fórmula: C = (ASCII + k) mod 128")
    print(f"\nMensaje original: '{mensaje}'")
    print(f"\nProceso de cifrado:")
    for i, char in enumerate(mensaje):
        print(f"   {char} → {ascii_orig[i]} + {k} = {ascii_orig[i] + k} mod 128 = {ascii_cif[i]}")
    print(f"\nASCII original: {ascii_orig}")
    print(f"ASCII cifrado:  {ascii_cif}")
    print(f"Mensaje cifrado: '{mensaje_cifrado}'")


def mostrar_proceso_descifrado(mensaje_cifrado: str, k: int = LLAVE_FIJA):
    """
    Muestra el proceso completo de descifrado paso a paso.
    """
    mensaje_desc, ascii_cif, ascii_desc = cesar_descifrar(mensaje_cifrado, k)
    
    print(f"\n{'='*50}")
    print("DESCIFRADO CÉSAR ASCII")
    print(f"{'='*50}")
    print(f"Llave k = {k}")
    print(f"Fórmula: ASCII = (C - k) mod 128")
    print(f"\nMensaje cifrado: '{mensaje_cifrado}'")
    print(f"\nProceso de descifrado:")
    for i, char in enumerate(mensaje_cifrado):
        print(f"   {repr(char)} → {ascii_cif[i]} - {k} = {ascii_cif[i] - k} mod 128 = {ascii_desc[i]}")
    print(f"\nASCII cifrado:    {ascii_cif}")
    print(f"ASCII descifrado: {ascii_desc}")
    print(f"Mensaje descifrado: '{mensaje_desc}'")


# =============================================================================
# PROGRAMA PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("   CIFRADOR CÉSAR ASCII - LLAVE FIJA")
    print("="*60)
    
    while True:
        # Input seed (k)
        entrada_k = input("\nIngresa la seed (k) [o 'salir']: ")
        if entrada_k.lower() == 'salir':
            print("\n¡Hasta luego!")
            break
        
        k = int(entrada_k)
        
        # Input mensaje
        mensaje = input("Ingresa el mensaje: ")
        
        # Cifrar
        mensaje_cifrado, ascii_orig, ascii_cif = cesar_cifrar(mensaje, k)
        
        # Descifrar (para verificar)
        mensaje_descifrado, _, _ = cesar_descifrar(mensaje_cifrado, k)
        
        # Mostrar resultados
        print(f"\n{'='*50}")
        print(f"Mensaje original:    '{mensaje}'")
        print(f"Mensaje en ASCII:    {ascii_orig}")
        print(f"Mensaje cifrado:     '{mensaje_cifrado}'")
        print(f"ASCII cifrado:       {ascii_cif}")
        print(f"Mensaje descifrado:  '{mensaje_descifrado}'")
        print(f"Llave generada (k):  {k}")
        print(f"{'='*50}")
