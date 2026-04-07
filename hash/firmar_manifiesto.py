import argparse
import sys
from pathlib import Path

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

BASE_DIR = Path(__file__).resolve().parent


def calcular_hash_archivo(ruta_archivo):
    resumen = SHA256.new()
    with ruta_archivo.open("rb") as archivo:
        while True:
            bloque = archivo.read(65536)
            if not bloque:
                break
            resumen.update(bloque)
    return resumen


def cargar_clave_privada(ruta_clave_privada):
    return RSA.import_key(ruta_clave_privada.read_bytes())


def firmar_hash(resumen_hash, clave_privada):
    return pkcs1_15.new(clave_privada).sign(resumen_hash)


def construir_parser():
    parser = argparse.ArgumentParser(
        description="Firma digitalmente un manifiesto SHA256SUMS.txt con RSA."
    )
    parser.add_argument(
        "manifiesto",
        help="Ruta del archivo SHA256SUMS.txt que se desea firmar.",
    )
    parser.add_argument(
        "--clave-privada",
        default=str(BASE_DIR / "medisoft_priv.pem"),
        help="Ruta de la clave privada RSA de MediSoft.",
    )
    parser.add_argument(
        "--salida",
        help="Ruta del archivo de firma. Si se omite, se genera SHA256SUMS.sig junto al manifiesto.",
    )
    return parser


def main():
    parser = construir_parser()
    args = parser.parse_args()

    ruta_manifiesto = Path(args.manifiesto).resolve()
    ruta_clave_privada = Path(args.clave_privada).resolve()
    ruta_salida = (
        Path(args.salida).resolve()
        if args.salida
        else ruta_manifiesto.with_suffix(".sig")
    )

    if not ruta_manifiesto.exists():
        print(f"Error: no existe el manifiesto {ruta_manifiesto}", file=sys.stderr)
        return 1

    if not ruta_clave_privada.exists():
        print(
            f"Error: no existe la clave privada {ruta_clave_privada}",
            file=sys.stderr,
        )
        return 1

    try:
        resumen_hash = calcular_hash_archivo(ruta_manifiesto)
        clave_privada = cargar_clave_privada(ruta_clave_privada)
        firma = firmar_hash(resumen_hash, clave_privada)
        ruta_salida.write_bytes(firma)
    except (ValueError, TypeError, OSError) as error:
        print(f"Error al firmar el manifiesto: {error}", file=sys.stderr)
        return 1

    print(f"Manifiesto firmado: {ruta_manifiesto}")
    print(f"SHA-256 del manifiesto: {resumen_hash.hexdigest()}")
    print(f"Firma guardada en: {ruta_salida}")
    print(f"Tamano de la firma: {len(firma)} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
