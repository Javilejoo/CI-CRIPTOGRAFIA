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


def cargar_clave_publica(ruta_clave_publica):
    return RSA.import_key(ruta_clave_publica.read_bytes())


def verificar_firma(resumen_hash, firma, clave_publica):
    pkcs1_15.new(clave_publica).verify(resumen_hash, firma)


def construir_parser():
    parser = argparse.ArgumentParser(
        description="Verifica la firma digital de un archivo SHA256SUMS.txt."
    )
    parser.add_argument(
        "manifiesto",
        help="Ruta del archivo SHA256SUMS.txt que se desea validar.",
    )
    parser.add_argument(
        "--clave-publica",
        default=str(BASE_DIR / "medisoft_pub.pem"),
        help="Ruta de la clave publica RSA de MediSoft.",
    )
    parser.add_argument(
        "--firma",
        help="Ruta del archivo SHA256SUMS.sig. Si se omite, se busca junto al manifiesto.",
    )
    return parser


def main():
    parser = construir_parser()
    args = parser.parse_args()

    ruta_manifiesto = Path(args.manifiesto).resolve()
    ruta_clave_publica = Path(args.clave_publica).resolve()
    ruta_firma = (
        Path(args.firma).resolve()
        if args.firma
        else ruta_manifiesto.with_suffix(".sig")
    )

    if not ruta_manifiesto.exists():
        print(f"Error: no existe el manifiesto {ruta_manifiesto}", file=sys.stderr)
        return 1

    if not ruta_clave_publica.exists():
        print(
            f"Error: no existe la clave publica {ruta_clave_publica}",
            file=sys.stderr,
        )
        return 1

    if not ruta_firma.exists():
        print(f"Error: no existe la firma {ruta_firma}", file=sys.stderr)
        return 1

    try:
        resumen_hash = calcular_hash_archivo(ruta_manifiesto)
        clave_publica = cargar_clave_publica(ruta_clave_publica)
        firma = ruta_firma.read_bytes()
        verificar_firma(resumen_hash, firma, clave_publica)
    except (ValueError, TypeError, OSError) as error:
        print(f"Firma INVALIDA para: {ruta_manifiesto}")
        print(f"Motivo: {error}")
        return 1

    print(f"Firma VALIDA para: {ruta_manifiesto}")
    print(f"SHA-256 del manifiesto: {resumen_hash.hexdigest()}")
    print(f"Clave publica usada: {ruta_clave_publica}")
    print(f"Firma usada: {ruta_firma}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
