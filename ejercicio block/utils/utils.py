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