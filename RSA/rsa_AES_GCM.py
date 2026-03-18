import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from generar_claves import generar_par_claves


def encrypt_document(document: bytes, recipient_public_key_pem: bytes) -> bytes:
    # 1. Cifrar el documento con AES-256-GCM
    # a) Generar clave AES aleatoria de 256 bits
    aes_key = os.urandom(32)  # 32 bytes = 256 bits

    # b) Cifrar el documento con AES-GCM
    aes_cipher = AES.new(aes_key, AES.MODE_GCM)
    ciphertext, tag = aes_cipher.encrypt_and_digest(document)
    nonce = aes_cipher.nonce

    # c) Cifrar la clave AES con la clave pública RSA usando OAEP
    recipient_public_key = RSA.import_key(recipient_public_key_pem)
    rsa_cipher = PKCS1_OAEP.new(recipient_public_key)
    encrypted_aes_key = rsa_cipher.encrypt(aes_key)

    # Empaquetar todo en un solo bloque de bytes
    # Formato:
    # [2 bytes: longitud de encrypted_aes_key]
    # [encrypted_aes_key]
    # [16 bytes nonce]
    # [16 bytes tag]
    # [ciphertext]
    encrypted_key_len = len(encrypted_aes_key).to_bytes(2, byteorder="big")

    package = (
        encrypted_key_len +
        encrypted_aes_key +
        nonce +
        tag +
        ciphertext
    )

    return package


def decrypt_document(pkg: bytes, recipient_private_key_pem: bytes) -> bytes:
    # 1) Leer la longitud de la clave AES cifrada con RSA
    encrypted_key_len = int.from_bytes(pkg[:2], byteorder="big")

    # 2) Extraer encrypted_aes_key, nonce, tag y ciphertext
    start = 2
    end = start + encrypted_key_len

    encrypted_aes_key = pkg[start:end]
    nonce = pkg[end:end + 16]
    tag = pkg[end + 16:end + 32]
    ciphertext = pkg[end + 32:]

    # 3) Descifrar la clave AES con la clave privada RSA
    recipient_private_key = RSA.import_key(recipient_private_key_pem)
    rsa_cipher = PKCS1_OAEP.new(recipient_private_key)
    aes_key = rsa_cipher.decrypt(encrypted_aes_key)

    # 4) Descifrar el documento con AES-GCM
    aes_cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
    document = aes_cipher.decrypt_and_verify(ciphertext, tag)

    return document

if __name__ == '__main__':
    generar_par_claves(2048)

    with open("public_key.pem", "rb") as f: pub = f.read()
    with open("private_key.pem", "rb") as f: priv = f.read()

    # Generen un cifrado de un texto
    doc = b"Contrato de confidencialidad No. 2025-GT-001"
    pkg = encrypt_document(doc, pub)
    resultado = decrypt_document(pkg, priv)


    # Prueba con archivo de 1 MB (simula un contrato real)
    doc_grande = os.urandom(1024 * 1024)
    pkg2 = encrypt_document(doc_grande, pub)
    assert decrypt_document(pkg2, priv) == doc_grande
    print("Archivo 1 MB: OK")
