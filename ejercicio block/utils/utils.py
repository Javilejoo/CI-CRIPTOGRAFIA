def string_to_ascii(s):
    lista = []
    for char in s:
        lista.append(ord(char))
    return lista


def ascii_to_bin(ascii_list):
    binary_list = []
    for num in ascii_list:
        bits = []  # lista para guardar los residuos
        n = num
        
        # caso especial si el número es 0
        if n == 0:
            bits = ['0']
        else:
            while n > 0:
                residuo = n % 2  # obtener el residuo de la división
                bits.append(str(residuo))
                n = n // 2  # división entera
        
        # invertir porque los residuos salen al revés
        bits.reverse()
        
        # completar a 8 bits agregando 0s a la izquierda
        while len(bits) < 8:
            bits.insert(0, '0')
        
        binary_list.append(''.join(bits))
            
    return binary_list

def bytes_to_bin(key_bytes):
    """Convierte bytes a cadena binaria."""
    return "".join(format(byte, '08b') for byte in key_bytes)


def bin_to_bytes(bin_str):
    """Convierte una cadena binaria a bytes."""
    bytes_list = []
    for i in range(0, len(bin_str), 8):
        byte = int(bin_str[i:i+8], 2)
        bytes_list.append(byte)
    return bytes(bytes_list)


def xor_blocks(block1, block2):
    """Realiza XOR entre dos bloques binarios de 64 bits."""
    result = int(block1, 2) ^ int(block2, 2)
    return format(result, '064b')