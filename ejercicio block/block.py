def padding(string, block_size):
    if not isinstance(string, str):
        raise TypeError("string debe ser de tipo str")

    if not isinstance(block_size, int):
        raise TypeError("block_size debe ser de tipo int")

    if block_size <= 0:
        raise ValueError("block_size debe ser mayor que 0")

    if len(string) > block_size:
        raise ValueError("El tamaño del bloque debe ser mayor o igual a la longitud del string.")

    block_sizes = list(string)
    faltantes = block_size - len(string)

    if faltantes > 0:
        byte_padding = hex(faltantes)
        block_sizes.extend([byte_padding] * faltantes)

    return block_sizes


print(padding("tu", 8))