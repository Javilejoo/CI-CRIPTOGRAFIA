from cesar import cesar_cifrar, cesar_descifrar

def analisis_frecuencia(mensaje):
    """
    Analiza la frecuencia de cada letra en un mensaje.
    Retorna un diccionario con el conteo y el total de letras.
    """
    mensaje = mensaje.upper()
    frecuencias = {}
    total_letras = 0
    
    for char in mensaje:
        if char.isalpha():
            total_letras += 1
            frecuencias[char] = frecuencias.get(char, 0) + 1
    
    return frecuencias, total_letras


def mostrar_tabla_frecuencias(mensaje):
    """
    Muestra una tabla con las frecuencias de caracteres del mensaje.
    """
    frecuencias, total = analisis_frecuencia(mensaje)
    
    if total == 0:
        print("El mensaje no contiene letras.")
        return
    
    ordenadas = sorted(frecuencias.items(), key=lambda x: x[1], reverse=True)
    
    print("=" * 50)
    print("       TABLA DE FRECUENCIA DE CARACTERES")
    print("=" * 50)
    print(f"{'Letra':<8} {'Conteo':<10} {'Porcentaje':<12} {'Gráfico'}")
    print("-" * 50)
    
    for letra, conteo in ordenadas:
        porcentaje = (conteo / total) * 100
        barra = "█" * int(porcentaje / 2)
        print(f"  {letra:<6} {conteo:<10} {porcentaje:>6.2f}%      {barra}")
    
    print("-" * 50)
    print(f"Total de letras analizadas: {total}")
    print("=" * 50)


def detectar_desplazamiento(texto_cifrado):
    """
    Detecta el desplazamiento de César usando análisis de frecuencia.
    """
    frecuencias, total = analisis_frecuencia(texto_cifrado)
    
    if not frecuencias:
        return 0
    
    letra_mas_frecuente = max(frecuencias, key=frecuencias.get)
    desplazamiento = (ord(letra_mas_frecuente) - ord('E')) % 26
    
    return desplazamiento


if __name__ == "__main__":
    mensaje = "Hola mundo, este es un mensaje secreto"
    desplazamiento = 3
    
    texto_cifrado = cesar_cifrar(mensaje, desplazamiento)
    desplazamiento_detectado = detectar_desplazamiento(texto_cifrado)
    texto_descifrado = cesar_descifrar(texto_cifrado, desplazamiento_detectado)
    
    print(f"Mensaje original:    {mensaje}")
    print(f"Mensaje cifrado:     {texto_cifrado}")
    print(f"Mensaje descifrado:  {texto_descifrado}")
    print()
    mostrar_tabla_frecuencias(texto_cifrado)