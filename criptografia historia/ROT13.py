from cesar import cesar_cifrar, cesar_descifrar


def ROT13_cifrar(mensaje, desplazamiento=13):
    resultado = cesar_cifrar(mensaje, desplazamiento)
    return resultado

def ROT13_descifrar(mensaje_cifrado, desplazamiento=13):
    resultado = cesar_descifrar(mensaje_cifrado, desplazamiento)
    return resultado

if __name__ == "__main__":

    print(ROT13_cifrar("Hello, World!"))
    print(ROT13_descifrar("Uryyb, Jbeyq!"))