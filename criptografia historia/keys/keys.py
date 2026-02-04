"""
Generador de Llaves Dinámicas usando ASCII
==========================================
Este módulo genera llaves criptográficas dinámicas basadas en valores ASCII.
"""

import os
import time
import random
import hashlib

# Rango de caracteres ASCII imprimibles (32-126)
ASCII_PRINTABLE_START = 32
ASCII_PRINTABLE_END = 126

# Rango de caracteres alfanuméricos
ASCII_ALFANUMERICO = (
    list(range(48, 58)) +   # 0-9
    list(range(65, 91)) +   # A-Z
    list(range(97, 123))    # a-z
)


def generar_llave_ascii_aleatoria(longitud: int = 16) -> str:
    """
    Genera una llave aleatoria usando caracteres ASCII imprimibles.
    
    Args:
        longitud: Longitud de la llave a generar
        
    Returns:
        Llave como string de caracteres ASCII
    """
    llave = ""
    for _ in range(longitud):
        codigo_ascii = random.randint(ASCII_PRINTABLE_START, ASCII_PRINTABLE_END)
        llave += chr(codigo_ascii)
    return llave


def generar_llave_alfanumerica(longitud: int = 16) -> str:
    """
    Genera una llave usando solo caracteres alfanuméricos.
    
    Args:
        longitud: Longitud de la llave a generar
        
    Returns:
        Llave alfanumérica
    """
    llave = ""
    for _ in range(longitud):
        codigo_ascii = random.choice(ASCII_ALFANUMERICO)
        llave += chr(codigo_ascii)
    return llave


def generar_llave_dinamica(mensaje: str, semilla: int) -> tuple:
    """
    Genera una llave dinámica basada en el mensaje y una semilla numérica.
    
    Proceso:
    1. Convierte el mensaje a valores ASCII
    2. Suma la semilla a cada valor ASCII
    
    Args:
        mensaje: Texto base para generar la llave
        semilla: Valor numérico a sumar (seed)
        
    Returns:
        Tupla con (llave_ascii_valores, llave_string, mensaje_ascii_original)
    """
    # Convertir mensaje a valores ASCII
    valores_ascii_mensaje = [ord(c) for c in mensaje]
    
    # Sumar la semilla a cada valor ASCII
    valores_llave = [valor + semilla for valor in valores_ascii_mensaje]
    
    # Convertir a string (manejando valores fuera del rango ASCII estándar)
    llave_string = ""
    for valor in valores_llave:
        # Si el valor está en rango imprimible, usar directamente
        if 32 <= valor <= 126:
            llave_string += chr(valor)
        else:
            # Si está fuera de rango, aplicar módulo para mantenerlo imprimible
            valor_ajustado = (valor % 95) + 32
            llave_string += chr(valor_ajustado)
    
    return valores_llave, llave_string, valores_ascii_mensaje


def mostrar_llave_dinamica(mensaje: str, semilla: int):
    """
    Muestra el proceso completo de generación de llave dinámica.
    
    Args:
        mensaje: Texto base
        semilla: Valor numérico (seed)
    """
    valores_llave, llave_string, valores_mensaje = generar_llave_dinamica(mensaje, semilla)
    
    print(f"\n{'='*50}")
    print("GENERACIÓN DE LLAVE DINÁMICA")
    print(f"{'='*50}")
    print(f"Mensaje: '{mensaje}'")
    print(f"Semilla (seed): {semilla}")
    print(f"\nPaso 1 - ASCII del mensaje: {valores_mensaje}")
    print(f"Paso 2 - Sumar semilla ({semilla}) a cada valor:")
    for i, (orig, nuevo) in enumerate(zip(valores_mensaje, valores_llave)):
        print(f"   '{mensaje[i]}': {orig} + {semilla} = {nuevo}")
    print(f"\nLlave (valores ASCII): {valores_llave}")
    print(f"Llave (string): {llave_string}")


def generar_llave_desde_frase(frase: str) -> str:
    """
    Genera una llave derivada de una frase usando valores ASCII.
    
    Args:
        frase: Frase secreta del usuario
        
    Returns:
        Llave derivada de la frase
    """
    # Obtener valores ASCII de la frase
    valores_ascii = [ord(c) for c in frase]
    
    # Crear llave mediante operaciones con los valores ASCII
    llave = ""
    for i, valor in enumerate(valores_ascii):
        # Operación: (valor + posición) mod 95 + 32 (rango imprimible)
        nuevo_valor = ((valor + i) % 95) + 32
        llave += chr(nuevo_valor)
    
    return llave


def generar_llave_secuencial(clave_maestra: str, contador: int) -> str:
    """
    Genera llaves secuenciales basadas en un contador.
    Útil para generar múltiples llaves únicas.
    
    Args:
        clave_maestra: Clave base
        contador: Número de secuencia
        
    Returns:
        Llave única para ese contador
    """
    datos = f"{clave_maestra}:{contador}"
    hash_bytes = hashlib.sha256(datos.encode()).digest()
    
    llave = ""
    for byte in hash_bytes[:16]:
        ascii_code = (byte % 95) + 32
        llave += chr(ascii_code)
    
    return llave


def llave_a_valores_ascii(llave: str) -> list:
    """
    Convierte una llave a su representación en valores ASCII.
    
    Args:
        llave: Llave a convertir
        
    Returns:
        Lista de valores ASCII
    """
    return [ord(c) for c in llave]


def valores_ascii_a_llave(valores: list) -> str:
    """
    Convierte valores ASCII a una llave string.
    
    Args:
        valores: Lista de valores ASCII
        
    Returns:
        Llave como string
    """
    return "".join(chr(v) for v in valores)


def mostrar_info_llave(llave: str, nombre: str = "Llave"):
    """
    Muestra información detallada de una llave.
    """
    valores = llave_a_valores_ascii(llave)
    print(f"\n{'='*50}")
    print(f"{nombre}")
    print(f"{'='*50}")
    print(f"Llave: {llave}")
    print(f"Longitud: {len(llave)} caracteres")
    print(f"Valores ASCII: {valores}")
    print(f"Hex: {llave.encode().hex()}")


# =============================================================================
# PROGRAMA PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("   GENERADOR DE LLAVES DINÁMICAS ASCII")
    print("="*60)
    
    while True:
        mensaje = input("\nEscribe el mensaje (o 'salir' para terminar): ")
        
        if mensaje.lower() == 'salir':
            print("\n¡Hasta luego!")
            break
        
        semilla = int(input("Ingresa la semilla (seed): "))
        
        # Generar llave dinámica
        valores_llave, llave_string, valores_mensaje = generar_llave_dinamica(mensaje, semilla)
        
        print(f"\n{'='*50}")
        print(f"Mensaje: '{mensaje}'")
        print(f"Mensaje en ASCII: {valores_mensaje}")
        print(f"Semilla: {semilla}")
        print(f"Llave dinámica: {valores_llave}")
        print(f"{'='*50}")
