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
        binary_list.append(bin(num)[2:].zfill(8))
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
