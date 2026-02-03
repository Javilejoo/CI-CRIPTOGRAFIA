lista = []
bits = []

# ==================== FUNCIONES ====================

def string_to_ascii(s):
    for char in s:
        lista.append(ord(char))

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

def decimal_to_binary(n):
    while n > 0:
        bits.append(str(n % 2))
        n = n // 2

    bits.reverse()

    # completar a 8 bits
    while len(bits) < 8:
        bits.insert(0, '0')

    return ''.join(bits)

def concatenar_lista(binary_list):
    return ''.join(map(str, binary_list))

def bloques_de_6(cadena):
    bloques = []
    for i in range(0, len(cadena), 6):
        bloques.append(cadena[i:i+6])
    return bloques

def bloques_de_8(cadena):
    bloques = []
    for i in range(0, len(cadena), 8):
        bloques.append(cadena[i:i+8])
    return bloques

def binario_a_decimal(binario):
    decimal = 0
    longitud = len(binario)

    for i in range(longitud):
        bit = int(binario[longitud - 1 - i])
        decimal += bit * (2 ** i)

    return decimal

def decimal_to_bin6(n):
    bits_local = []
    if n == 0:
        bits_local = ['0']
    else:
        while n > 0:
            bits_local.append(str(n % 2))
            n = n // 2
    bits_local.reverse()
    # completar a 6 bits
    while len(bits_local) < 6:
        bits_local.insert(0, '0')
    return ''.join(bits_local)

base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def decimal_to_base64_char(indice):
    return base64_chars[indice]

def base64_to_decimal(base64_string):
    indices = []
    for char in base64_string:
        indice = base64_chars.index(char)
        indices.append(indice)
    return indices

def decimal_a_ascii(lista):
    resultado = ""
    for num in lista:
        resultado += chr(num)
    return resultado

def XOR_to_BIN(bin1, bin2):
    """
    Aplica XOR bit a bit entre dos cadenas binarias.
    Si tienen diferente longitud, rellena con 0s a la izquierda la más corta.
    
    Tabla XOR:
    0 XOR 0 = 0
    0 XOR 1 = 1
    1 XOR 0 = 1
    1 XOR 1 = 0
    """
    max_len = max(len(bin1), len(bin2))
    bin1 = bin1.zfill(max_len)
    bin2 = bin2.zfill(max_len)
    
    resultado = []
    for i in range(len(bin1)):
        if bin1[i] != bin2[i]:
            resultado.append('1')
        else:
            resultado.append('0')
    
    return ''.join(resultado)

# ==================== EJECUCIÓN ====================

palabra = 'Sun'
string_to_ascii(palabra)
binary_list = ascii_to_bin(lista)
concatenado = concatenar_lista(binary_list)
bloquesix = bloques_de_6(concatenado)
decimales = [binario_a_decimal(b) for b in bloquesix]
base64_string = ''.join([decimal_to_base64_char(d) for d in decimales])

base64_to_decimal_index = base64_to_decimal(base64_string)
decimal_to_bin6_list = [decimal_to_bin6(n) for n in base64_to_decimal_index]
concatenado2 = concatenar_lista(decimal_to_bin6_list)
bloquesocho = bloques_de_8(concatenado2)
binario_a_decimal_lista = [binario_a_decimal(b) for b in bloquesocho]

binario_a = '01010011'
binario_b = '11111111'

print()
print('1. ASCII a BINARIO')
print(f"   '{palabra}' -> {binary_list}")
print()
print('2. BINARIO a ASCII')
print(f"   {binary_list} -> '{decimal_a_ascii(binario_a_decimal_lista)}'")
print()
print('3. BINARIO a BASE64')
print(f"   {binary_list} -> '{base64_string}'")
print()
print('4. BASE64 a BINARIO')
print(f"   '{base64_string}' -> {bloquesocho}")
print()
print('5. BASE64 a ASCII')
print(f"   '{base64_string}' -> '{decimal_a_ascii(binario_a_decimal_lista)}'")
print()
print('6. ASCII a BASE64')
print(f"   '{palabra}' -> '{base64_string}'")
print()
print('7. XOR a BINARIO')
print(f"   {binario_a} XOR {binario_b} = {XOR_to_BIN(binario_a, binario_b)}")