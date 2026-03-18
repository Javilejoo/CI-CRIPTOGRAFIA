from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
 

def cifrar_con_rsa(mensaje: bytes, public_key_pem: bytes) -> bytes:
    # Cargar la clave pública
    public_key = RSA.import_key(public_key_pem)
    
    # Crear un cifrador OAEP con la clave pública
    cipher = PKCS1_OAEP.new(public_key)
    
    # Cifrar el mensaje
    cifrado = cipher.encrypt(mensaje)
    
    return cifrado

def descifrar_con_rsa(cifrado: bytes, private_key_pem: bytes) -> bytes:
    # Cargar la clave privada
    private_key = RSA.import_key(private_key_pem)

    # Crear un descifrador OAEP con la clave privada
    cipher = PKCS1_OAEP.new(private_key)

    # Descifrar el mensaje
    descifrado = cipher.decrypt(cifrado)

    return descifrado

if __name__ == '__main__':
    # Cargar claves generadas en el ejercicio anterior
    with open("public_key.pem", "rb") as f:
        pub = f.read()
    with open("private_key.pem", "rb") as f:
        priv = f.read()

    mensaje_original = b"El mensaje sera la clave secreta de AES"
    cifrado   = cifrar_con_rsa(mensaje_original, pub)
    descifrado = descifrar_con_rsa(cifrado, priv)

    print(f"Original  : {mensaje_original}")
    print(f"Cifrado   : {cifrado.hex()[:64]}...")  # primeros 64 chars hex
    print(f"Descifrado: {descifrado}")


    # Pregunta: ¿Por qué cifrar el mismo mensaje dos veces produce
    # resultados distintos? Demuéstralo y explica qué propiedad de OAEP lo causa.
    c1 = cifrar_con_rsa(mensaje_original, pub)
    c2 = cifrar_con_rsa(mensaje_original, pub)
    print(f"\nc1 == c2: {c1 == c2}")   # Esperado: False