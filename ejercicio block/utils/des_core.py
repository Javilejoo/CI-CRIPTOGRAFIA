"""
des_core.py - Módulo con tablas y funciones core de DES reutilizables.
Este módulo es compartido entre DES y 3DES.
"""

# --- TABLAS GLOBALES Y CONSTANTES DE DES ---

# Permutación Inicial (IP)
IP_TABLE = [
    58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7
]

# Permuted Choice 1 (PC-1) - Reduce clave de 64 a 56 bits
PC1_TABLE = [
    57, 49, 41, 33, 25, 17,  9,  1, 58, 50, 42, 34, 26, 18,
    10,  2, 59, 51, 43, 35, 27, 19, 11,  3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,  7, 62, 54, 46, 38, 30, 22,
    14,  6, 61, 53, 45, 37, 29, 21, 13,  5, 28, 20, 12,  4
]

# Permuted Choice 2 (PC-2) - Selecciona 48 bits de los 56
PC2_TABLE = [
    14, 17, 11, 24,  1,  5,  3, 28, 15,  6, 21, 10,
    23, 19, 12,  4, 26,  8, 16,  7, 27, 20, 13,  2,
    41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32
]

# Tabla de Expansión E (32 -> 48 bits)
E_TABLE = [
    32,  1,  2,  3,  4,  5,  4,  5,  6,  7,  8,  9,
     8,  9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32,  1
]

# Tabla de Permutación P (32 bits)
P_TABLE = [
    16,  7, 20, 21, 29, 12, 28, 17,  1, 15, 23, 26, 5, 18, 31, 10, 
     2,  8, 24, 14, 32, 27,  3,  9, 19, 13, 30,  6, 22, 11,  4, 25
]

# Permutación Inversa Final (IP^-1)
IP_INV_TABLE = [
    40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41,  9, 49, 17, 57, 25
]

# Número de rotaciones a la izquierda por ronda
SHIFTS_TABLE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

# S-Boxes (8 cajas, cada una con 4 filas y 16 columnas)
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


# --- FUNCIONES AUXILIARES ---

def left_rotate(bits, n):
    """Realiza una rotación circular a la izquierda de 'n' posiciones en la cadena de bits."""
    return bits[n:] + bits[:n]


def bin_to_hex(bin_str):
    """Convierte una cadena binaria a hexadecimal."""
    if len(bin_str) == 0:
        return "0"
    return format(int(bin_str, 2), '0' + str(len(bin_str)//4) + 'X')


def hex_to_bin(hex_str, bits=64):
    """Convierte una cadena hexadecimal a binaria con longitud fija."""
    return format(int(hex_str, 16), f'0{bits}b')


# --- FUNCIONES CORE DE DES ---

def s_box_substitution(xor_bin):
    """Divide la entrada de 48 bits y aplica las S-Boxes."""
    bloques_6bits = [xor_bin[i:i+6] for i in range(0, len(xor_bin), 6)]
    
    sboxes_out = ""
    for i in range(8):
        bloque = bloques_6bits[i]
        fila = int(bloque[0] + bloque[5], 2)
        columna = int(bloque[1:5], 2)
        
        valor_decimal = S_BOXES[i][fila][columna]
        bloque_4bits = format(valor_decimal, '04b')
        sboxes_out += bloque_4bits

    return sboxes_out


def f_function(r, k):
    """Calcula la función F de Feistel: F(R, K)"""
    # 1. Expansión (32 -> 48 bits)
    r_expandido = ''.join(r[i-1] for i in E_TABLE)

    # 2. XOR con la clave de la ronda
    xor_res = int(r_expandido, 2) ^ int(k, 2)
    xor_res_bin = format(xor_res, '048b')

    # 3. Sustitución con S-Boxes
    sboxes_resultado = s_box_substitution(xor_res_bin)

    # 4. Permutación P
    resultado_p = "".join(sboxes_resultado[i-1] for i in P_TABLE)
    return resultado_p


def generar_subclaves(clave_bin):
    """Genera las 16 subclaves de 48 bits a partir de la clave de 64 bits."""
    # Aplicar PC-1 (64 -> 56 bits)
    clave_56 = ''.join(clave_bin[i-1] for i in PC1_TABLE)
    
    # Dividir en C0 y D0 (28 bits cada uno)
    c = clave_56[:28]
    d = clave_56[28:]
    
    subclaves = []
    for ronda in range(16):
        # Rotar C y D según la tabla de shifts
        c = left_rotate(c, SHIFTS_TABLE[ronda])
        d = left_rotate(d, SHIFTS_TABLE[ronda])
        
        # Concatenar y aplicar PC-2 para obtener la subclave de 48 bits
        cd = c + d
        subclave = ''.join(cd[i-1] for i in PC2_TABLE)
        subclaves.append(subclave)
    
    return subclaves


def des_block_encrypt(bloque, subclaves, verbose=False, round_offset=0, label="ENCRYPT"):
    """
    Cifra UN bloque de 64 bits usando DES con 16 rondas.
    
    Args:
        bloque: Cadena binaria de 64 bits
        subclaves: Lista de 16 subclaves de 48 bits
        verbose: Si True, imprime detalle de cada ronda
        round_offset: Offset para numerar las rondas (para 3DES)
        label: Etiqueta para el output
    
    Returns:
        Bloque cifrado de 64 bits (cadena binaria)
    """
    # Permutación Inicial (IP)
    bloque_ip = ''.join(bloque[i-1] for i in IP_TABLE)
    
    if verbose:
        print(f"After initial permutation: {bin_to_hex(bloque_ip)}")
    
    # Dividir en L0 y R0
    L = bloque_ip[:32]
    R = bloque_ip[32:]
    
    # 16 Rondas de Feistel
    for ronda in range(16):
        L_prev = L
        R_prev = R
        
        # L[i] = R[i-1]
        L = R_prev
        
        # R[i] = L[i-1] XOR F(R[i-1], K[i])
        f_result = f_function(R_prev, subclaves[ronda])
        R = format(int(L_prev, 2) ^ int(f_result, 2), '032b')
        
        if verbose:
            print(f"Round {ronda+1+round_offset:2d}   {bin_to_hex(L)}   {bin_to_hex(R)}   {bin_to_hex(subclaves[ronda])}")
    
    # Intercambio final (R16 + L16) y Permutación Inversa
    pre_output = R + L  # Nota: se intercambian R y L
    bloque_cifrado = ''.join(pre_output[i-1] for i in IP_INV_TABLE)
    
    return bloque_cifrado


def des_block_decrypt(bloque, subclaves, verbose=False, round_offset=0, label="DECRYPT"):
    """
    Descifra UN bloque de 64 bits usando DES con 16 rondas (subclaves en orden inverso).
    
    Args:
        bloque: Cadena binaria de 64 bits (cifrada)
        subclaves: Lista de 16 subclaves de 48 bits
        verbose: Si True, imprime detalle de cada ronda
        round_offset: Offset para numerar las rondas (para 3DES)
        label: Etiqueta para el output
    
    Returns:
        Bloque descifrado de 64 bits (cadena binaria)
    """
    # Permutación Inicial (IP)
    bloque_ip = ''.join(bloque[i-1] for i in IP_TABLE)
    
    if verbose:
        print(f"After initial permutation: {bin_to_hex(bloque_ip)}")
    
    # Dividir en L0 y R0
    L = bloque_ip[:32]
    R = bloque_ip[32:]
    
    # 16 Rondas de Feistel (con subclaves en orden INVERSO)
    for ronda in range(16):
        L_prev = L
        R_prev = R
        
        # L[i] = R[i-1]
        L = R_prev
        
        # R[i] = L[i-1] XOR F(R[i-1], K[16-i]) - Claves en orden inverso
        f_result = f_function(R_prev, subclaves[15 - ronda])
        R = format(int(L_prev, 2) ^ int(f_result, 2), '032b')
        
        if verbose:
            print(f"Round {ronda+1+round_offset:2d}   {bin_to_hex(L)}   {bin_to_hex(R)}   {bin_to_hex(subclaves[15-ronda])}")
    
    # Intercambio final (R16 + L16) y Permutación Inversa
    pre_output = R + L
    bloque_descifrado = ''.join(pre_output[i-1] for i in IP_INV_TABLE)
    
    return bloque_descifrado
