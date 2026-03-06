"""
des_cipher.py - Implementación de DES (Data Encryption Standard).
Utiliza el módulo des_core.py para las funciones compartidas.
"""
import sys
import os

# Determinamos la raíz del proyecto para importar correctamente
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Al tener una carpeta con espacio ('ejercicio block'), añadimos su ruta al path
EJERCICIO_BLOCK_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if EJERCICIO_BLOCK_DIR not in sys.path:
    sys.path.insert(0, EJERCICIO_BLOCK_DIR)

from utils.utils import ascii_to_bin
from utils.des_core import (
    generar_subclaves, des_block_encrypt, des_block_decrypt, bin_to_hex
)
from block import padding

def read_txt(file_name):
    """Lee un archivo y aplica padding a nivel de bytes antes de convertir a bits."""
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(b"Mensaje de prueba para DES")
            
    with open(file_path, 'rb') as file:
        data = file.read()
    
    print(f"Contenido original (bytes): {data}")
    return data

def generar_bloques_64bits(data_bytes):
    """Aplica padding original de bytes y luego divide en bloques de 64 bits."""
    bloques_binarios = []
    
    # Procesamos en trozos de 8 bytes (64 bits)
    for i in range(0, len(data_bytes), 8):
        fragmento = data_bytes[i:i+8]
        
        # Aplicamos el padding original si el fragmento no llega a 8 bytes
        if len(fragmento) < 8:
            fragmento = padding(fragmento, 8)
            
        # Convertimos los bytes (ya con padding) a binario
        # ascii_to_bin espera una lista de enteros (valores ASCII)
        ascii_list = list(fragmento)
        bin_list = ascii_to_bin(ascii_list)
        
        # Unimos para formar el bloque de 64 bits
        bloque_64 = "".join(bin_list)
        bloques_binarios.append(bloque_64)
        
    print(f"\nTotal de bloques de 64 bits generados: {len(bloques_binarios)}")
    return bloques_binarios


def des_encrypt(bloques_binarios, clave_bin=None):
    """Cifra los bloques usando DES con 16 rondas."""
    # Generar clave si no se proporciona
    if clave_bin is None:
        clave_bytes = os.urandom(8)
        clave_bin = "".join(format(byte, '08b') for byte in clave_bytes)
    
    print(f"\nClave (64 bits): {bin_to_hex(clave_bin)}")
    
    # Generar las 16 subclaves
    subclaves = generar_subclaves(clave_bin)
    
    bloques_cifrados = []
    
    for bloque in bloques_binarios:
        print(f"\n{'='*50}")
        print("ENCRYPTION")
        
        # Usar la función de cifrado de des_core
        bloque_cifrado = des_block_encrypt(bloque, subclaves, verbose=True)
        
        print(f"Cipher Text: {bin_to_hex(bloque_cifrado)}")
        bloques_cifrados.append(bloque_cifrado)
    
    return bloques_cifrados, clave_bin

def des_decrypt(bloques_cifrados, clave_bin):
    """Descifra los bloques usando DES con 16 rondas (claves en orden inverso)."""
    # Generar las 16 subclaves
    subclaves = generar_subclaves(clave_bin)
    
    bloques_descifrados = []
    
    for bloque in bloques_cifrados:
        print(f"\n{'='*50}")
        print("DECRYPTION")
        
        # Usar la función de descifrado de des_core
        bloque_descifrado = des_block_decrypt(bloque, subclaves, verbose=True)
        
        print(f"Plain Text: {bin_to_hex(bloque_descifrado)}")
        bloques_descifrados.append(bloque_descifrado)
    
    return bloques_descifrados

if __name__ == "__main__":
    # 1. Leer mensaje desde archivo
    datos = read_txt('des.txt')
    
    # 2. Agrupar y convertir a binario usando el padding de bytes
    lista_de_bloques = generar_bloques_64bits(datos)
    
    # 3. Cifrar con DES (16 rondas)
    bloques_cifrados, clave_usada = des_encrypt(lista_de_bloques)
    
    # 4. Descifrar con DES (verificación)
    bloques_descifrados = des_decrypt(bloques_cifrados, clave_usada)
    
    # 5. Mostrar resumen
    print(f"\n{'='*50}")
    print("RESUMEN")
    print(f"Mensaje original: {datos}")
    print(f"Clave usada (hex): {bin_to_hex(clave_usada)}")



