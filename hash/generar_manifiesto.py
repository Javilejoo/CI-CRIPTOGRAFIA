import argparse
import os
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


def resolver_archivos(rutas):
    archivos = []
    for ruta in rutas:
        archivo = Path(ruta).resolve()
        if not archivo.exists():
            raise FileNotFoundError(f"No existe el archivo: {archivo}")
        if not archivo.is_file():
            raise IsADirectoryError(f"La ruta no es un archivo: {archivo}")
        archivos.append(archivo)
    return archivos


def obtener_ruta_manifiesto(archivos, ruta_salida):
    if ruta_salida:
        return Path(ruta_salida).resolve()

    try:
        directorio_comun = Path(
            os.path.commonpath([str(archivo.parent) for archivo in archivos])
        )
    except ValueError as error:
        raise ValueError(
            "Los archivos deben estar en la misma unidad o debes indicar --manifiesto."
        ) from error

    return directorio_comun / "SHA256SUMS.txt"


def nombre_para_manifiesto(ruta_archivo, ruta_manifiesto):
    relativo = os.path.relpath(ruta_archivo, start=ruta_manifiesto.parent)
    return relativo.replace("\\", "/")


def agregar_registros_al_manifiesto(archivos, ruta_manifiesto):
    ruta_manifiesto.parent.mkdir(parents=True, exist_ok=True)

    with ruta_manifiesto.open("a", encoding="utf-8") as manifiesto:
        for archivo in archivos:
            hash_archivo = calcular_sha256_archivo(archivo)
            nombre_archivo = nombre_para_manifiesto(archivo, ruta_manifiesto)
            manifiesto.write(f"{hash_archivo} {nombre_archivo}\n")
            print(f"{nombre_archivo} -> {hash_archivo}")

    print(f"\nSe agregaron {len(archivos)} registros a {ruta_manifiesto}")


def construir_parser():
    parser = argparse.ArgumentParser(
        description="Genera un historial SHA-256 para archivos de un release."
    )
    parser.add_argument(
        "archivos",
        nargs="+",
        help="Rutas de los archivos que formaran parte del paquete.",
    )
    parser.add_argument(
        "--manifiesto",
        help="Ruta del archivo SHA256SUMS.txt. Si se omite, se crea en el directorio comun.",
    )
    return parser


def main():
    parser = construir_parser()
    args = parser.parse_args()

    if len(args.archivos) < 5:
        parser.error("Debes proporcionar al menos 5 archivos.")

    try:
        archivos = resolver_archivos(args.archivos)
        ruta_manifiesto = obtener_ruta_manifiesto(archivos, args.manifiesto)
        agregar_registros_al_manifiesto(archivos, ruta_manifiesto)
    except (FileNotFoundError, IsADirectoryError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
