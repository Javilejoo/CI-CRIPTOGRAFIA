def cesar_cifrar(mensaje, desplazamiento):
    cifrado = ""
    for char in mensaje:
        if char.isalpha():
            desplazado = ord(char) + desplazamiento
            if char.islower():
                if desplazado > ord('z'):
                    desplazado -= 26
                cifrado += chr(desplazado)
            elif char.isupper():
                if desplazado > ord('Z'):
                    desplazado -= 26
                cifrado += chr(desplazado)
        else:
            cifrado += char
    return cifrado

def cesar_descifrar(mensaje_cifrado, desplazamiento):
    descifrado = ""
    for char in mensaje_cifrado:
        if char.isalpha():
            desplazado = ord(char) - desplazamiento
            if char.islower():
                if desplazado < ord('a'):
                    desplazado += 26
                descifrado += chr(desplazado)
            elif char.isupper():
                if desplazado < ord('A'):
                    desplazado += 26
                descifrado += chr(desplazado)
        else:
            descifrado += char
    return descifrado

print(cesar_cifrar("abc", 3))
print(cesar_descifrar("def", 3))
