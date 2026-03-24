from Crypto.Hash import MD5, SHA1, SHA256, SHA3_256

def calculo_hash():
    mensaje = b"MediSoft-v2.1.0"

    md5_hash = MD5.new(mensaje).hexdigest()
    sha1_hash = SHA1.new(mensaje).hexdigest()
    sha256_hash = SHA256.new(mensaje).hexdigest()
    sha3_256_hash = SHA3_256.new(mensaje).hexdigest()

    print(f"Datos: {mensaje}")
    print(f"MD5: {md5_hash}")
    print(f"SHA1: {sha1_hash}")
    print(f"SHA256: {sha256_hash}")
    print(f"SHA3_256: {sha3_256_hash}")

calculo_hash()
