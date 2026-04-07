import argparse
import string
import sys
from hashlib import sha256
from pathlib import Path

BUFFER_SIZE = 65536


def calcular_sha256_archivo(ruta_archivo):
    resumen = sha256()
    with ruta_archivo.open("rb") as archivo:
        while True:
            bloque = archivo.read(BUFFER_SIZE)
            if not bloque:
                break
            resumen.update(bloque)
    return resumen.hexdigest()


def cargar_ultimos_registros(ruta_manifiesto):
    registros = {}
    with ruta_manifiesto.open("r", encoding="utf-8") as manifiesto:
        for numero_linea, linea in enumerate(manifiesto, start=1):
            linea = linea.strip()
            if not linea:
                continue

            partes = linea.split(maxsplit=1)
            if len(partes) != 2:
                raise ValueError(
                    f"Linea {numero_linea}: se esperaba '<HASH> <nombre_archivo>'."
                )

            hash_esperado, nombre_archivo = partes
            if len(hash_esperado) != 64 or any(
                caracter not in string.hexdigits for caracter in hash_esperado
            ):
                raise ValueError(
                    f"Linea {numero_linea}: el hash SHA-256 no es valido."
                )

            hash_esperado = hash_esperado.lower()
            if nombre_archivo in registros:
                del registros[nombre_archivo]
            registros[nombre_archivo] = hash_esperado

    if not registros:
        raise ValueError("El manifiesto no contiene registros para verificar.")

    return list(registros.items())


def verificar_registros(registros, directorio_base):
    correctos = 0
    incorrectos = 0
    faltantes = 0

    print(f"Directorio verificado: {directorio_base}")
    print("-" * 72)

    for nombre_archivo, hash_esperado in registros:
        ruta_archivo = (directorio_base / Path(nombre_archivo)).resolve()

        if not ruta_archivo.exists() or not ruta_archivo.is_file():
            print(f"FALTANTE     {nombre_archivo}")
            faltantes += 1
            continue

        hash_obtenido = calcular_sha256_archivo(ruta_archivo)
        if hash_obtenido == hash_esperado:
            print(f"OK           {nombre_archivo}")
            correctos += 1
        else:
            print(f"NO COINCIDE  {nombre_archivo}")
            print(f"Esperado: {hash_esperado}")
            print(f"Obtenido: {hash_obtenido}")
            incorrectos += 1

    return correctos, incorrectos, faltantes


def construir_parser():
    parser = argparse.ArgumentParser(
        description="Verifica la integridad de un paquete usando SHA256SUMS.txt."
    )
    parser.add_argument(
        "--manifiesto",
        default="SHA256SUMS.txt",
        help="Ruta del manifiesto SHA256SUMS.txt.",
    )
    parser.add_argument(
        "--directorio",
        help="Directorio donde estan los archivos del paquete. Por defecto usa la carpeta del manifiesto.",
    )
    return parser


def main():
    parser = construir_parser()
    args = parser.parse_args()

    ruta_manifiesto = Path(args.manifiesto).resolve()
    if not ruta_manifiesto.exists():
        print(f"Error: no existe el manifiesto {ruta_manifiesto}", file=sys.stderr)
        return 1

    directorio_base = (
        Path(args.directorio).resolve() if args.directorio else ruta_manifiesto.parent
    )

    try:
        registros = cargar_ultimos_registros(ruta_manifiesto)
        correctos, incorrectos, faltantes = verificar_registros(
            registros, directorio_base
        )
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print("-" * 72)
    print(
        f"Resumen -> correctos: {correctos}, incorrectos: {incorrectos}, faltantes: {faltantes}"
    )

    return 0 if incorrectos == 0 and faltantes == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
