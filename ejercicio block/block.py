def padding(data: bytes, block_size: int) -> bytes:
    if not isinstance(data, bytes):
        raise TypeError("data debe ser de tipo bytes")

    if not isinstance(block_size, int):
        raise TypeError("block_size debe ser de tipo int")

    if block_size <= 0:
        raise ValueError("block_size debe ser mayor que 0")

    if len(data) > block_size:
        raise ValueError("El tamaño del bloque debe ser mayor o igual a la longitud de data.")

    faltantes = block_size - len(data)

    if faltantes > 0:
        return data + bytes([faltantes]) * faltantes

    return data


print(padding(b"tu", 8))