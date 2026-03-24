from Crypto.Hash import MD5, SHA1, SHA256, SHA3_256


def calculo_hash():
    mensaje = b"MediSoft-v2.1.0"

    algoritmos = [
        ("MD5", MD5),
        ("SHA1", SHA1),
        ("SHA256", SHA256),
        ("SHA3_256", SHA3_256),
    ]

    resultados = []
    for nombre, algoritmo in algoritmos:
        hash_hex = algoritmo.new(mensaje).hexdigest()
        longitud_hex = len(hash_hex)
        longitud_bits = longitud_hex * 4
        resultados.append((nombre, longitud_bits, longitud_hex, hash_hex))

    encabezado = f"{'Algoritmo':<12}{'Longitud bits':<16}{'Longitud hex':<15}Valor del hash"
    separador = "-" * len(encabezado)

    print(f"Datos: {mensaje.decode()}\n")
    print(encabezado)
    print(separador)
    for nombre, bits, longitud_hex, hash_hex in resultados:
        print(f"{nombre:<12}{bits:<16}{longitud_hex:<15}{hash_hex}")


calculo_hash()
