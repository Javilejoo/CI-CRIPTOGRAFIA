lista = []
bits = []
def string_to_ascii(s):
    for char in s:
        lista.append(ord(char))

string_to_ascii("hola")
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
