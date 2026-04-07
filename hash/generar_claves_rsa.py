import argparse
import sys
from pathlib import Path

from Crypto.PublicKey import RSA

BASE_DIR = Path(__file__).resolve().parent


def generar_par_claves(bits):
    return RSA.generate(bits)


def guardar_claves(par_claves, ruta_privada, ruta_publica):
    ruta_privada.parent.mkdir(parents=True, exist_ok=True)
    ruta_publica.parent.mkdir(parents=True, exist_ok=True)

    clave_privada = par_claves.export_key()
    clave_publica = par_claves.publickey().export_key()

    ruta_privada.write_bytes(clave_privada)
    ruta_publica.write_bytes(clave_publica)


def construir_parser():
    parser = argparse.ArgumentParser(
        description="Genera un par de claves RSA de 2048 bits para MediSoft."
    )
    parser.add_argument(
        "--bits",
        type=int,
        default=2048,
        help="Tamano del par de claves RSA. Por defecto 2048 bits.",
    )
    parser.add_argument(
        "--privada",
        default=str(BASE_DIR / "medisoft_priv.pem"),
        help="Ruta donde se guardara la clave privada.",
    )
    parser.add_argument(
        "--publica",
        default=str(BASE_DIR / "medisoft_pub.pem"),
        help="Ruta donde se guardara la clave publica.",
    )
    return parser


def main():
    parser = construir_parser()
    args = parser.parse_args()

    if args.bits != 2048:
        print(
            "Aviso: el ejercicio pide 2048 bits. Se usara el valor indicado por parametro.",
            file=sys.stderr,
        )

    ruta_privada = Path(args.privada).resolve()
    ruta_publica = Path(args.publica).resolve()

    try:
        par_claves = generar_par_claves(args.bits)
        guardar_claves(par_claves, ruta_privada, ruta_publica)
    except (ValueError, OSError) as error:
        print(f"Error al generar o guardar las claves: {error}", file=sys.stderr)
        return 1

    print(f"Clave privada guardada en: {ruta_privada}")
    print(f"Clave publica guardada en: {ruta_publica}")
    print("Recuerda mantener la clave privada en secreto.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
