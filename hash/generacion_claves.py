from Crypto.Hash import SHA1, SHA256
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

contrasenas = ["admin", "123456", "hospital", "medisoft2024"]


def generar_claves_hash(contrasenas):
    claves_hash = []
    for contrasena in contrasenas:
        clave_hash = SHA256.new(contrasena.encode()).hexdigest()
        claves_hash.append((contrasena, clave_hash))
    return claves_hash


def llamar_api(clave_hash):
    prefijo = clave_hash[:5].upper()
    sufijo = clave_hash[5:].upper()
    url = f"https://api.pwnedpasswords.com/range/{prefijo}"
    headers = {
        "User-Agent": "CI-Criptografia/1.0",
        "Add-Padding": "true",
    }

    solicitud = Request(url, headers=headers)
    with urlopen(solicitud, timeout=10) as respuesta:
        contenido = respuesta.read().decode("utf-8")

    for linea in contenido.splitlines():
        hash_sufijo, apariciones = linea.split(":")
        if hash_sufijo == sufijo:
            return int(apariciones)
    return 0


def revisar_filtraciones(contrasenas):
    for contrasena, hash_sha256 in generar_claves_hash(contrasenas):
        hash_sha1_api = SHA1.new(contrasena.encode()).hexdigest().upper()

        try:
            apariciones = llamar_api(hash_sha1_api)
            print(f"{contrasena}: {hash_sha256}")
            print(f"Aparece {apariciones} veces en filtraciones conocidas.\n")
        except (HTTPError, URLError, TimeoutError) as error:
            print(f"{contrasena}: {hash_sha256}")
            print(f"No se pudo consultar la API: {error}\n")


if __name__ == "__main__":
    revisar_filtraciones(contrasenas)
