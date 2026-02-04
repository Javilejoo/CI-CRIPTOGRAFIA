def analisis_frecuencia(mensaje):
    """
    Analiza la frecuencia de cada letra en un mensaje.
    Retorna un diccionario con el conteo y el total de letras.
    """
    mensaje = mensaje.upper()
    frecuencias = {}
    total_letras = 0
    
    # Contar cada letra
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
    
    # Ordenar por frecuencia (mayor a menor)
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


if __name__ == "__main__":
    # Ejemplo de uso
    mensaje = "Hola mundo, este es un mensaje de prueba para analizar frecuencias"
    
    print(f"Mensaje: {mensaje}\n")
    mostrar_tabla_frecuencias(mensaje)
    
    print("\n--- Ejemplo con texto cifrado ---\n")
    texto_cifrado = "Krod pxqgr, hvwh hv xq phqvdmh vhfuhwr"
    print(f"Texto cifrado: {texto_cifrado}\n")
    mostrar_tabla_frecuencias(texto_cifrado)
