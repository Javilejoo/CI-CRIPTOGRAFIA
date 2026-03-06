"""
tripledes_cipher.py - Implementacion de Triple DES (3DES) en modo EDE con CBC.

3DES-EDE (Encrypt-Decrypt-Encrypt):
- 48 rondas totales = 16 rondas x 3 operaciones
- Clave de 112 bits (2-key variant): K1=K3, K2 diferente
- Cifrado: C = DES_K1(DES^-1_K2(DES_K1(P)))

Modo CBC (Cipher Block Chaining):
- IV (Vector de Inicializacion) de 64 bits aleatorio
- El IV es UNICO para cada mensaje cifrado
- El IV debe transmitirse junto con el texto cifrado (prepended)
- Cifrado: C[i] = 3DES(P[i] XOR C[i-1]), donde C[0] = IV
- Descifrado: P[i] = 3DES^-1(C[i]) XOR C[i-1]

Padding: Utiliza Crypto.Util.Padding (PKCS#7)
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

from utils.utils import ascii_to_bin, bytes_to_bin, bin_to_bytes, xor_blocks
from utils.des_core import (
    generar_subclaves, des_block_encrypt, des_block_decrypt, bin_to_hex
)
from Crypto.Util.Padding import pad, unpad


# --- FUNCIONES DE LECTURA Y PROCESAMIENTO DE BLOQUES ---

def read_txt(file_name):
    """Lee un archivo y retorna su contenido como bytes."""
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(b"Mensaje de prueba para 3DES")
            
    with open(file_path, 'rb') as file:
        data = file.read()
    
    print(f"Contenido original (bytes): {data}")
    return data


def generar_bloques_64bits(data_bytes):
    """Aplica padding PKCS#7 usando Crypto.Util.Padding y divide en bloques de 64 bits."""
    bloques_binarios = []
    
    # Aplicar padding PKCS#7 al mensaje completo (8 bytes = 64 bits block size DES)
    data_padded = pad(data_bytes, 8, style='pkcs7')
    
    # Dividir en bloques de 8 bytes y convertir a binario
    for i in range(0, len(data_padded), 8):
        fragmento = data_padded[i:i+8]
        
        # Convertimos los bytes a binario
        ascii_list = list(fragmento)
        bin_list = ascii_to_bin(ascii_list)
        
        # Unimos para formar el bloque de 64 bits
        bloque_64 = "".join(bin_list)
        bloques_binarios.append(bloque_64)
        
    print(f"\nTotal de bloques de 64 bits generados: {len(bloques_binarios)}")
    return bloques_binarios


# --- FUNCIONES DE GENERACIÓN DE CLAVES 3DES ---

def generate_3des_key():
    """
    Genera una clave de 112 bits para 3DES (2-key variant).
    Retorna 16 bytes (K1: 8 bytes, K2: 8 bytes), donde K3=K1.
    """
    # Generar 16 bytes aleatorios (K1 + K2)
    key_bytes = os.urandom(16)
    return key_bytes


def split_3des_key(key_bytes):
    """
    Divide la clave de 16 bytes en K1 (64 bits) y K2 (64 bits).
    K3 = K1 (2-key 3DES).
    
    Returns:
        tuple: (k1_bin, k2_bin) - cadenas binarias de 64 bits cada una
    """
    k1_bytes = key_bytes[:8]
    k2_bytes = key_bytes[8:16]
    
    k1_bin = bytes_to_bin(k1_bytes)
    k2_bin = bytes_to_bin(k2_bytes)
    
    return k1_bin, k2_bin


# --- FUNCIONES CBC ---

def generate_iv():
    """Genera un Vector de Inicialización (IV) aleatorio de 64 bits."""
    iv_bytes = os.urandom(8)
    return bytes_to_bin(iv_bytes)


# --- FUNCIONES 3DES-EDE POR BLOQUE ---

def triple_des_encrypt_block(bloque, k1_subclaves, k2_subclaves, verbose=True, block_num=1):
    """
    Cifra un bloque usando 3DES-EDE: E(K1) -> D(K2) -> E(K1).
    Total: 48 rondas (16 + 16 + 16).
    
    Args:
        bloque: Bloque binario de 64 bits
        k1_subclaves: 16 subclaves de K1
        k2_subclaves: 16 subclaves de K2
        verbose: Si True, imprime detalle de cada ronda
        block_num: Número de bloque (para el output)
    
    Returns:
        Bloque cifrado de 64 bits
    """
    if verbose:
        print(f"\n{'='*60}")
        print(f"3DES-EDE ENCRYPTION - Block {block_num}")
        print(f"{'='*60}")
    
    # --- PASO 1: ENCRYPT con K1 (Rondas 1-16) ---
    if verbose:
        print(f"\n--- ENCRYPT with K1 (Rounds 1-16) ---")
    
    bloque_e1 = des_block_encrypt(bloque, k1_subclaves, verbose=verbose, round_offset=0)
    
    if verbose:
        print(f"After E1 (K1): {bin_to_hex(bloque_e1)}")
    
    # --- PASO 2: DECRYPT con K2 (Rondas 17-32) ---
    if verbose:
        print(f"\n--- DECRYPT with K2 (Rounds 17-32) ---")
    
    bloque_d = des_block_decrypt(bloque_e1, k2_subclaves, verbose=verbose, round_offset=16)
    
    if verbose:
        print(f"After D (K2): {bin_to_hex(bloque_d)}")
    
    # --- PASO 3: ENCRYPT con K1 (Rondas 33-48) ---
    if verbose:
        print(f"\n--- ENCRYPT with K1 (Rounds 33-48) ---")
    
    bloque_e2 = des_block_encrypt(bloque_d, k1_subclaves, verbose=verbose, round_offset=32)
    
    if verbose:
        print(f"After E2 (K1): {bin_to_hex(bloque_e2)}")
    
    return bloque_e2


def triple_des_decrypt_block(bloque, k1_subclaves, k2_subclaves, verbose=True, block_num=1):
    """
    Descifra un bloque usando 3DES-DED: D(K1) -> E(K2) -> D(K1).
    Total: 48 rondas (16 + 16 + 16).
    Operación inversa a EDE.
    
    Args:
        bloque: Bloque cifrado de 64 bits
        k1_subclaves: 16 subclaves de K1
        k2_subclaves: 16 subclaves de K2
        verbose: Si True, imprime detalle de cada ronda
        block_num: Número de bloque (para el output)
    
    Returns:
        Bloque descifrado de 64 bits
    """
    if verbose:
        print(f"\n{'='*60}")
        print(f"3DES-DED DECRYPTION - Block {block_num}")
        print(f"{'='*60}")
    
    # --- PASO 1: DECRYPT con K1 (Rondas 1-16) ---
    if verbose:
        print(f"\n--- DECRYPT with K1 (Rounds 1-16) ---")
    
    bloque_d1 = des_block_decrypt(bloque, k1_subclaves, verbose=verbose, round_offset=0)
    
    if verbose:
        print(f"After D1 (K1): {bin_to_hex(bloque_d1)}")
    
    # --- PASO 2: ENCRYPT con K2 (Rondas 17-32) ---
    if verbose:
        print(f"\n--- ENCRYPT with K2 (Rounds 17-32) ---")
    
    bloque_e = des_block_encrypt(bloque_d1, k2_subclaves, verbose=verbose, round_offset=16)
    
    if verbose:
        print(f"After E (K2): {bin_to_hex(bloque_e)}")
    
    # --- PASO 3: DECRYPT con K1 (Rondas 33-48) ---
    if verbose:
        print(f"\n--- DECRYPT with K1 (Rounds 33-48) ---")
    
    bloque_d2 = des_block_decrypt(bloque_e, k1_subclaves, verbose=verbose, round_offset=32)
    
    if verbose:
        print(f"After D2 (K1): {bin_to_hex(bloque_d2)}")
    
    return bloque_d2


# --- FUNCIONES 3DES-CBC ---

def triple_des_cbc_encrypt(bloques_binarios, key_bytes=None, iv=None):
    """
    Cifra bloques usando 3DES-EDE en modo CBC.
    
    Modo CBC:
    - C[0] = 3DES(P[0] XOR IV)
    - C[i] = 3DES(P[i] XOR C[i-1])
    
    Args:
        bloques_binarios: Lista de bloques de 64 bits
        key_bytes: Clave de 16 bytes (si None, se genera)
        iv: Vector de inicialización de 64 bits (si None, se genera)
    
    Returns:
        tuple: (bloques_cifrados, key_bytes, iv)
    """
    # Generar clave si no se proporciona
    if key_bytes is None:
        key_bytes = generate_3des_key()
    
    # Generar IV si no se proporciona
    if iv is None:
        iv = generate_iv()
    
    # Obtener K1 y K2 en binario
    k1_bin, k2_bin = split_3des_key(key_bytes)
    
    # Generar subclaves para K1 y K2
    k1_subclaves = generar_subclaves(k1_bin)
    k2_subclaves = generar_subclaves(k2_bin)
    
    # Mostrar información de claves
    print(f"\n{'='*60}")
    print("3DES-CBC ENCRYPTION")
    print(f"{'='*60}")
    print(f"Key K1 (64 bits): {bin_to_hex(k1_bin)}")
    print(f"Key K2 (64 bits): {bin_to_hex(k2_bin)}")
    print(f"Combined Key (112 bits effective): {bin_to_hex(k1_bin)}{bin_to_hex(k2_bin)}")
    print(f"IV (64 bits): {bin_to_hex(iv)}")
    
    bloques_cifrados = []
    bloque_anterior = iv  # El primer bloque usa el IV
    
    for i, bloque in enumerate(bloques_binarios):
        # XOR del bloque actual con el bloque anterior (o IV para el primero)
        bloque_xor = xor_blocks(bloque, bloque_anterior)
        
        if i == 0:
            print(f"\nBlock {i+1}: P XOR IV = {bin_to_hex(bloque_xor)}")
        else:
            print(f"\nBlock {i+1}: P XOR C[{i}] = {bin_to_hex(bloque_xor)}")
        
        # Cifrar con 3DES-EDE
        bloque_cifrado = triple_des_encrypt_block(
            bloque_xor, k1_subclaves, k2_subclaves, 
            verbose=True, block_num=i+1
        )
        
        print(f"\nCipher Text Block {i+1}: {bin_to_hex(bloque_cifrado)}")
        
        bloques_cifrados.append(bloque_cifrado)
        bloque_anterior = bloque_cifrado  # El siguiente bloque usará este ciphertext
    
    return bloques_cifrados, key_bytes, iv


def triple_des_cbc_decrypt(bloques_cifrados, key_bytes, iv):
    """
    Descifra bloques usando 3DES-DED en modo CBC.
    
    Modo CBC (descifrado):
    - P[0] = 3DES^-1(C[0]) XOR IV
    - P[i] = 3DES^-1(C[i]) XOR C[i-1]
    
    Args:
        bloques_cifrados: Lista de bloques cifrados de 64 bits
        key_bytes: Clave de 16 bytes
        iv: Vector de inicialización de 64 bits
    
    Returns:
        Lista de bloques descifrados
    """
    # Obtener K1 y K2 en binario
    k1_bin, k2_bin = split_3des_key(key_bytes)
    
    # Generar subclaves para K1 y K2
    k1_subclaves = generar_subclaves(k1_bin)
    k2_subclaves = generar_subclaves(k2_bin)
    
    # Mostrar información de claves
    print(f"\n{'='*60}")
    print("3DES-CBC DECRYPTION")
    print(f"{'='*60}")
    print(f"Key K1 (64 bits): {bin_to_hex(k1_bin)}")
    print(f"Key K2 (64 bits): {bin_to_hex(k2_bin)}")
    print(f"IV (64 bits): {bin_to_hex(iv)}")
    
    bloques_descifrados = []
    bloque_anterior = iv  # El primer bloque usa el IV
    
    for i, bloque in enumerate(bloques_cifrados):
        # Descifrar con 3DES-DED
        bloque_des = triple_des_decrypt_block(
            bloque, k1_subclaves, k2_subclaves,
            verbose=True, block_num=i+1
        )
        
        # XOR con el bloque anterior (o IV para el primero)
        bloque_descifrado = xor_blocks(bloque_des, bloque_anterior)
        
        if i == 0:
            print(f"\nBlock {i+1}: D XOR IV = {bin_to_hex(bloque_descifrado)}")
        else:
            print(f"\nBlock {i+1}: D XOR C[{i}] = {bin_to_hex(bloque_descifrado)}")
        
        print(f"Plain Text Block {i+1}: {bin_to_hex(bloque_descifrado)}")
        
        bloques_descifrados.append(bloque_descifrado)
        bloque_anterior = bloque  # El siguiente bloque usará el ciphertext actual
    
    return bloques_descifrados


def remove_padding_pkcs7(data_bytes):
    """Elimina el padding PKCS#7 usando Crypto.Util.Padding."""
    return unpad(data_bytes, 8, style='pkcs7')


# --- FUNCIONES PARA EMPAQUETAR IV CON CIPHERTEXT ---

def pack_ciphertext_with_iv(bloques_cifrados, iv):
    """
    Empaqueta el IV junto con el texto cifrado para transmisión.
    Formato: IV (8 bytes) + Ciphertext (n bloques de 8 bytes)
    
    Args:
        bloques_cifrados: Lista de bloques cifrados en binario
        iv: IV en formato binario (64 bits)
    
    Returns:
        bytes: IV + Ciphertext empaquetados
    """
    # Convertir IV de binario a bytes
    iv_bytes = bin_to_bytes(iv)
    
    # Convertir bloques cifrados de binario a bytes
    ciphertext_bytes = b""
    for bloque in bloques_cifrados:
        ciphertext_bytes += bin_to_bytes(bloque)
    
    # Empaquetado: IV primero, luego ciphertext
    return iv_bytes + ciphertext_bytes


def unpack_ciphertext_with_iv(packed_data):
    """
    Desempaqueta el IV y el texto cifrado recibido.
    
    Args:
        packed_data: bytes que contienen IV (8 bytes) + Ciphertext
    
    Returns:
        tuple: (bloques_cifrados en binario, iv en binario)
    """
    # Extraer IV (primeros 8 bytes)
    iv_bytes = packed_data[:8]
    iv_bin = bytes_to_bin(iv_bytes)
    
    # Extraer ciphertext (resto de los bytes)
    ciphertext_bytes = packed_data[8:]
    
    # Convertir ciphertext a bloques binarios de 64 bits
    bloques_cifrados = []
    for i in range(0, len(ciphertext_bytes), 8):
        bloque_bytes = ciphertext_bytes[i:i+8]
        bloque_bin = bytes_to_bin(bloque_bytes)
        bloques_cifrados.append(bloque_bin)
    
    return bloques_cifrados, iv_bin


# --- MAIN ---

if __name__ == "__main__":
    # 1. Leer mensaje desde archivo
    print("="*60)
    print("TRIPLE DES (3DES-EDE) CON MODO CBC")
    print("="*60)
    
    datos = read_txt('3des.txt')
    
    # 2. Generar bloques de 64 bits con padding
    lista_de_bloques = generar_bloques_64bits(datos)
    
    # 3. Cifrar con 3DES-CBC (48 rondas por bloque)
    bloques_cifrados, clave_usada, iv_usado = triple_des_cbc_encrypt(lista_de_bloques)
    
    # 4. Descifrar con 3DES-CBC (verificación)
    bloques_descifrados = triple_des_cbc_decrypt(bloques_cifrados, clave_usada, iv_usado)
    
    # 5. Convertir bloques descifrados a bytes y remover padding
    mensaje_descifrado_bytes = b""
    for bloque in bloques_descifrados:
        mensaje_descifrado_bytes += bin_to_bytes(bloque)
    
    mensaje_descifrado_bytes = remove_padding_pkcs7(mensaje_descifrado_bytes)
    
    # 6. Demostrar empaquetado de IV con ciphertext para transmisión
    print(f"\n{'='*60}")
    print("EMPAQUETADO DE IV + CIPHERTEXT PARA TRANSMISION")
    print(f"{'='*60}")
    
    packed_data = pack_ciphertext_with_iv(bloques_cifrados, iv_usado)
    print(f"Datos empaquetados (hex): {packed_data.hex()}")
    print(f"Tamano total: {len(packed_data)} bytes (IV: 8 bytes + Ciphertext: {len(packed_data)-8} bytes)")
    
    # Desempaquetar (simular receptor)
    bloques_recibidos, iv_recibido = unpack_ciphertext_with_iv(packed_data)
    print(f"IV recibido (hex): {bin_to_hex(iv_recibido)}")
    print(f"Bloques cifrados recibidos: {len(bloques_recibidos)}")
    
    # 7. Mostrar resumen
    print(f"\n{'='*60}")
    print("RESUMEN")
    print(f"{'='*60}")
    print(f"Mensaje original: {datos}")
    print(f"Mensaje descifrado: {mensaje_descifrado_bytes}")
    print(f"Clave K1 (hex): {bin_to_hex(bytes_to_bin(clave_usada[:8]))}")
    print(f"Clave K2 (hex): {bin_to_hex(bytes_to_bin(clave_usada[8:16]))}")
    print(f"IV (hex): {bin_to_hex(iv_usado)}")


