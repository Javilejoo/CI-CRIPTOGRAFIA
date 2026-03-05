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
from block import padding

# --- TABLAS GLOBALES Y CONSTANTES DE DES ---
IP_TABLE = [
    58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7
]

PC1_TABLE = [
    57, 49, 41, 33, 25, 17,  9,  1, 58, 50, 42, 34, 26, 18,
    10,  2, 59, 51, 43, 35, 27, 19, 11,  3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,  7, 62, 54, 46, 38, 30, 22,
    14,  6, 61, 53, 45, 37, 29, 21, 13,  5, 28, 20, 12,  4
]

PC2_TABLE = [
    14, 17, 11, 24,  1,  5,  3, 28, 15,  6, 21, 10,
    23, 19, 12,  4, 26,  8, 16,  7, 27, 20, 13,  2,
    41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32
]

E_TABLE = [
    32,  1,  2,  3,  4,  5,  4,  5,  6,  7,  8,  9,
     8,  9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32,  1
]

P_TABLE = [
    16,  7, 20, 21, 29, 12, 28, 17,  1, 15, 23, 26, 5, 18, 31, 10, 
     2,  8, 24, 14, 32, 27,  3,  9, 19, 13, 30,  6, 22, 11,  4, 25
]

S_BOXES = [
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7], [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8], [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0], [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10], [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5], [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15], [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8], [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1], [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7], [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15], [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9], [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4], [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9], [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6], [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14], [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11], [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8], [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6], [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1], [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6], [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2], [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7], [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2], [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8], [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
]

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
print(read_txt('des.txt'))

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


def des(bloques_binarios):
    # Generar una clave aleatoria de 64 bits para cada ejecución
    clave_bytes = os.urandom(8)
    clave_bin = "".join(format(byte, '08b') for byte in clave_bytes)
    print(f"Clave Aleatoria (64 bits): {clave_bin}")

    # --- Key Schedule para Ronda 1 ---
    clave_56 = ''.join(clave_bin[i-1] for i in PC1_TABLE)
    c_0, d_0 = clave_56[:28], clave_56[28:]
    c_1, d_1 = left_rotate(c_0, 1), left_rotate(d_0, 1)
    clave_ronda_1 = ''.join((c_1 + d_1)[i-1] for i in PC2_TABLE)
    print(f"Clave de ronda 1 (48 bits, PC-2): {clave_ronda_1}")

    for bloque in bloques_binarios:
        # Aplicar la permutación inicial
        bloque_permutado = ''.join(bloque[i-1] for i in IP_TABLE)
        print(f"\n--- Procesando Bloque ---")
        print(f"Bloque permutado: {bloque_permutado}")

        # Dividir el bloque en mitades L0 y R0
        l_0, r_0 = bloque_permutado[:32], bloque_permutado[32:]
        print(f"l0: {l_0}")
        print(f"r0: {r_0}")

        # --- CÁLCULO F(R0, K1) PARA RONDA 1 ---
        f_resultado = f_function(r_0, clave_ronda_1)
        
        # --- CÁLCULO DE L1 y R1 ---
        l_1 = r_0
        r_1 = format(int(l_0, 2) ^ int(f_resultado, 2), '032b')
        
        print(f"\n--- Resultados de Ronda 1 ---")
        print(f"L1: {l_1}")
        print(f"R1: {r_1}")

def f_function(r0, k1):
    """Calcula la función F de Feistel: F(R, K)"""
    # 1. Expansión (32 -> 48 bits)
    r0_expandido = ''.join(r0[i-1] for i in E_TABLE)
    print(f"R0 expandido (48 bits): {r0_expandido}")

    # 2. XOR con la clave de la ronda (K1)
    xor_res = int(r0_expandido, 2) ^ int(k1, 2)
    xor_res_bin = format(xor_res, '048b')
    print(f"Resultado XOR (R0_E ^ K1): {xor_res_bin}")

    # 3. Sustitución con S-Boxes
    sboxes_resultado = s_box_substitution(xor_res_bin)

    # 4. Permutación P
    resultado_p = "".join(sboxes_resultado[i-1] for i in P_TABLE)
    print(f"Resultado tras Permutación P: {resultado_p}")
    return resultado_p

def s_box_substitution(xor_bin):
    """Divide la entrada de 48 bits y aplica las S-Boxes."""
    bloques_6bits = [xor_bin[i:i+6] for i in range(0, len(xor_bin), 6)]
    print(f"Bloques de 6 bits para S-boxes: {bloques_6bits}")
    
    sboxes_out = ""
    for i in range(8):
        bloque = bloques_6bits[i]
        fila = int(bloque[0] + bloque[5], 2)
        columna = int(bloque[1:5], 2)
        
        valor_decimal = S_BOXES[i][fila][columna]
        bloque_4bits = format(valor_decimal, '04b')
        sboxes_out += bloque_4bits
        
        print(f"S-Box {i+1}: Bloque {bloque} -> Fila {fila}, Col {columna} -> Valor {valor_decimal} ({bloque_4bits})")

    print(f"\nResultado Final tras las 8 S-Boxes (32 bits): {sboxes_out}")
    return sboxes_out


def left_rotate(bits, n):
    """Realiza una rotación circular a la izquierda de 'n' posiciones en la cadena de bits."""
    return bits[n:] + bits[:n]

if __name__ == "__main__":
    # 1. Leer como bytes
    datos = read_txt('des.txt')
    
    # 2. Agrupar y convertir a binario usando el padding de bytes
    lista_de_bloques = generar_bloques_64bits(datos)
    
    # 3. Procesar los bloques con DES
    des(lista_de_bloques)



