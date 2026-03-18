# RSA - Cifrado Asimetrico e Hibrido

## Descripcion del proyecto (Carpeta RSA)

Esta carpeta contiene ejemplos practicos de criptografia asimetrica con RSA usando Python y la libreria `pycryptodome`.

Incluye tres componentes principales:

- `generar_claves.py`: genera un par de claves RSA (`public_key.pem` y `private_key.pem`).
- `rsa_OAEP.py`: cifra y descifra mensajes cortos con RSA + OAEP.
- `rsa_AES_GCM.py`: implementa cifrado hibrido:
  - Cifra el documento con AES-256-GCM.
  - Cifra la clave AES con RSA-OAEP.
  - Empaqueta todo en un bloque de bytes para poder descifrar despues.

Adicionalmente, `RSA.ipynb` contiene un notebook con ejercicios o demostraciones del tema.

## Instrucciones de instalacion y uso

### 1) Requisitos

- Python 3.8 o superior
- pip

### 2) Instalar dependencia

Desde la carpeta `RSA`, ejecutar:

```bash
pip install pycryptodome
```

### 3) Ejecucion de scripts

Ubicate en la carpeta `RSA` y ejecuta:

```bash
python generar_claves.py
python rsa_OAEP.py
python rsa_AES_GCM.py
```

## Ejemplos de ejecucion

### Ejemplo 1: Generar claves

```bash
python generar_claves.py
```

Salida esperada:

```text
Claves generadas: private_key.pem y public_key.pem
```

### Ejemplo 2: Cifrado RSA con OAEP

```bash
python rsa_OAEP.py
```

Salida aproximada:

```text
Original  : b'El mensaje sera la clave secreta de AES'
Cifrado   : a1b2c3d4... (hexadecimal)
Descifrado: b'El mensaje sera la clave secreta de AES'

c1 == c2: False
```

Nota: `c1 == c2: False` demuestra que OAEP usa aleatoriedad, por eso cifrar el mismo mensaje dos veces produce resultados distintos.

### Ejemplo 3: Cifrado hibrido RSA + AES-GCM

```bash
python rsa_AES_GCM.py
```

Salida esperada:

```text
Archivo 1 MB: OK
```

Esto valida que un archivo binario de 1 MB puede cifrarse y descifrarse correctamente con el esquema hibrido.
