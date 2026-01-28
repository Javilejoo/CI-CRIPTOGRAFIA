lista = []
bits = []
def string_to_ascii(s):
    for char in s:
        lista.append(ord(char))

string_to_ascii("Sun")
print(lista)

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


# convertir todos los elemento de la lista ASCII
binary_list = ascii_to_bin(lista)
print(binary_list)

# Concatenar lista binary list
def concatenar_lista(binary_list):
    return ''.join(map(str, binary_list))

concatenado = concatenar_lista(binary_list)
print(concatenado)

def bloques_de_6(cadena):
    bloques = []
    for i in range(0, len(cadena), 6):
        bloques.append(cadena[i:i+6])
    return bloques

bloquesix = bloques_de_6(concatenado)
print(bloques_de_6(concatenado))

def binario_a_decimal(binario):
    decimal = 0
    longitud = len(binario)

    for i in range(longitud):
        bit = int(binario[longitud - 1 - i])
        decimal += bit * (2 ** i)

    return decimal


decimales = [binario_a_decimal(b) for b in bloquesix]
print(decimales)

base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

# Función para obtener el carácter Base64 dado un índice decimal
def decimal_to_base64_char(indice):
    return base64_chars[indice]

# Usando la lista de decimales (índices) para obtener los caracteres base64
base64_string = ''.join([decimal_to_base64_char(d) for d in decimales])
print("Base64:", base64_string)


