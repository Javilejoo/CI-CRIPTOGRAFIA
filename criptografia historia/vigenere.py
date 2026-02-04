def vigenere_cifrar(mensaje, clave):
    """
    Cifra un mensaje usando el cifrado de Vigenère.
    La clave se repite hasta cubrir la longitud del mensaje.
    """
    cifrado = ""
    clave = clave.upper()
    indice_clave = 0
    
    for char in mensaje:
        if char.isalpha():
            # Obtener el desplazamiento de la letra de la clave (A=0, B=1, ..., Z=25)
            desplazamiento = ord(clave[indice_clave % len(clave)]) - ord('A')
            
            if char.islower():
                cifrado += chr((ord(char) - ord('a') + desplazamiento) % 26 + ord('a'))
            else:
                cifrado += chr((ord(char) - ord('A') + desplazamiento) % 26 + ord('A'))
            
            indice_clave += 1
        else:
            cifrado += char
    
    return cifrado


def vigenere_descifrar(mensaje_cifrado, clave):
    """
    Descifra un mensaje cifrado con Vigenère.
    La clave se repite hasta cubrir la longitud del mensaje.
    """
    descifrado = ""
    clave = clave.upper()
    indice_clave = 0
    
    for char in mensaje_cifrado:
        if char.isalpha():
            # Obtener el desplazamiento de la letra de la clave (A=0, B=1, ..., Z=25)
            desplazamiento = ord(clave[indice_clave % len(clave)]) - ord('A')
            
            if char.islower():
                descifrado += chr((ord(char) - ord('a') - desplazamiento) % 26 + ord('a'))
            else:
                descifrado += chr((ord(char) - ord('A') - desplazamiento) % 26 + ord('A'))
            
            indice_clave += 1
        else:
            descifrado += char
    
    return descifrado


if __name__ == "__main__":
    # Ejemplos de uso
    mensaje = "hola"
    clave = "ab"
    
    cifrado = vigenere_cifrar(mensaje, clave)
    print(f"Mensaje original: {mensaje}")
    print(f"Clave: {clave}")
    print(f"Mensaje cifrado: {cifrado}")
    
    descifrado = vigenere_descifrar(cifrado, clave)
    print(f"Mensaje descifrado: {descifrado}")
    
    print("\n--- Descifrado directo ---")
    mensaje_cifrado = "hplb"
    clave2 = "ab"
    
    descifrado2 = vigenere_descifrar(mensaje_cifrado, clave2)
    print(f"Mensaje cifrado: {mensaje_cifrado}")
    print(f"Clave: {clave2}")
    print(f"Mensaje descifrado: {descifrado2}") 
