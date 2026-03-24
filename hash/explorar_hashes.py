from Crypto.Hash import MD5, SHA1, SHA256, SHA3_256


def calculo_hash():
    mensaje = b"MediSoft-v2.1.0"
    minuscula = b"medisoft-v2.1.0"

    mensajes = [
        mensaje,
        minuscula,
    ]

    algoritmos = [
        ("MD5", MD5),
        ("SHA1", SHA1),
        ("SHA256", SHA256),
        ("SHA3_256", SHA3_256),
    ]

    resultados = []
    for dato in mensajes:
        texto = dato.decode()
        for nombre, algoritmo in algoritmos:
            hash_hex = algoritmo.new(dato).hexdigest()
            longitud_hex = len(hash_hex)
            longitud_bits = longitud_hex * 4
            resultados.append((texto, nombre, longitud_bits, longitud_hex, hash_hex))

    encabezado = (
        f"{'Mensaje':<18}"
        f"{'Algoritmo':<12}"
        f"{'Longitud bits':<16}"
        f"{'Longitud hex':<15}"
        "Valor del hash"
    )
    separador = "-" * len(encabezado)

    print("Tabla comparativa de hashes\n")
    print(encabezado)
    print(separador)
    for texto, nombre, bits, longitud_hex, hash_hex in resultados:
        print(f"{texto:<18}{nombre:<12}{bits:<16}{longitud_hex:<15}{hash_hex}")


calculo_hash()
