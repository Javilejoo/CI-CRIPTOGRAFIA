# CI-CRIPTOGRAFIA

Proyecto académico con ejercicios y demostraciones de criptografía clásica y moderna en Python. Incluye conversión ASCII/binario/Base64, cifrados históricos, generación de llaves, cifrado por flujo, cifrado por bloques y ejemplos de RSA con cifrado híbrido.

## Contenido del proyecto

- `asciibin.py`
  Script de apoyo para convertir texto entre ASCII, binario y Base64, además de mostrar un ejemplo de XOR binario.

- `historia_de_criptografia.ipynb`
  Notebook con material de apoyo sobre historia de la criptografía.

- `criptografia historia/`
  Implementaciones básicas de cifrados clásicos y análisis de frecuencia.

- `keys/`
  Ejercicios de generación de llaves y cifrado ASCII con llave fija y dinámica.

- `ejercicio stream/`
  Cifrador de flujo basado en XOR con un keystream pseudoaleatorio.

- `ejercicio block/`
  Ejercicios de cifrado por bloques con DES, 3DES y AES.

- `RSA/`
  Ejemplos de criptografía asimétrica con RSA y cifrado híbrido RSA + AES-GCM.

- `.venv/` y `venv/`
  Entornos virtuales locales. No forman parte de la lógica del proyecto; solo contienen dependencias instaladas en la máquina.

## Requisitos

- Python 3.10 o superior
- `pip`
- Opcional: Jupyter Notebook o VS Code con soporte para notebooks si deseas abrir los archivos `.ipynb`

## Librerías necesarias

El proyecto usa estas librerías externas:

- `pycryptodome`
  Se utiliza en `ejercicio block/` y `RSA/`.
  Proporciona primitivas criptográficas modernas como:
  - `Crypto.Cipher.AES`
  - `Crypto.Cipher.PKCS1_OAEP`
  - `Crypto.PublicKey.RSA`
  - `Crypto.Util.Padding`

- `Pillow`
  Se utiliza en `ejercicio block/src/aes_cipher.py`.
  Sirve para abrir imágenes, convertirlas a BMP y demostrar la diferencia visual entre AES en modo ECB y CBC.

- `jupyter`
  Es opcional.
  Solo se necesita si quieres abrir y ejecutar `historia_de_criptografia.ipynb` o `RSA/RSA.ipynb`.

Módulos de la librería estándar usados en el proyecto:

- `os`
- `sys`
- `io`
- `random`
- `hashlib`
- `datetime`
- `subprocess`
- `unittest`
- `time`

## Crear un entorno virtual

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

### Windows CMD

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
```

### Linux o macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

Para salir del entorno virtual:

```bash
deactivate
```

## Instalar las librerías del proyecto

Desde la raíz del repositorio:

```bash
pip install pycryptodome Pillow jupyter
```

Si solo quieres ejecutar scripts y no usar notebooks:

```bash
pip install pycryptodome Pillow
```

También puedes instalar las dependencias específicas de `ejercicio block` con:

```bash
pip install -r "ejercicio block/requirements.txt"
```

## Estructura del proyecto y definición de cada carpeta

### 1. `criptografia historia/`

Contiene ejemplos de criptografía clásica:

- `cesar.py`
  Implementa cifrado y descifrado César.

- `ROT13.py`
  Implementa ROT13 reutilizando el cifrado César con desplazamiento 13.

- `vigenere.py`
  Implementa cifrado y descifrado Vigenère.

- `analisis_frecuencia.py`
  Cuenta frecuencias de letras y estima el desplazamiento de un cifrado César.

- `analisis_frecuancia.py`
  Archivo adicional con nombre similar; conviene revisarlo si se desea unificar o corregir duplicados.

Dependencias externas:

- No requiere librerías externas.

Ejemplos de ejecución:

```bash
python "criptografia historia/cesar.py"
python "criptografia historia/ROT13.py"
python "criptografia historia/vigenere.py"
python "criptografia historia/analisis_frecuencia.py"
```

### 2. `keys/`

Carpeta enfocada en llaves y desplazamientos ASCII:

- `keys.py`
  Genera llaves ASCII aleatorias, alfanuméricas, dinámicas y secuenciales.

- `cypher_llave_fija.py`
  Cifra y descifra texto con un desplazamiento ASCII fijo.

- `cypher_llave_dinamica.py`
  Cifra y descifra texto con una llave que cambia por posición.

Dependencias externas:

- No requiere librerías externas.

Ejemplos de ejecución:

```bash
python "keys/keys.py"
python "keys/cypher_llave_fija.py"
python "keys/cypher_llave_dinamica.py"
```

### 3. `ejercicio stream/`

Implementa un cifrador de flujo con XOR:

- `keystream.py`
  Genera un keystream pseudoaleatorio a partir de clave y nonce, cifra y descifra mensajes.

- `validacion_pruebas.py`
  Ejecuta ejemplos demostrativos del cifrado.

- `pruebas_unitarias.py`
  Ejecuta pruebas automáticas con `unittest`.

- `README.md`
  Documentación interna de esta práctica.

Dependencias externas:

- No requiere librerías externas.

Ejemplos de ejecución:

```bash
python "ejercicio stream/keystream.py"
python "ejercicio stream/validacion_pruebas.py"
python "ejercicio stream/pruebas_unitarias.py"
```

### 4. `ejercicio block/`

Carpeta dedicada al cifrado por bloques:

- `src/des_cipher.py`
  Implementa DES sobre bloques de 64 bits y muestra el proceso de cifrado/descifrado.

- `src/tripledes_cipher.py`
  Implementa 3DES en modo EDE con CBC y padding PKCS#7.

- `src/aes_cipher.py`
  Implementa AES-256 en modos ECB y CBC, incluyendo cifrado de imágenes.

- `utils/des_core.py`
  Funciones internas compartidas para DES.

- `utils/utils.py`
  Funciones auxiliares de binario, bytes y XOR.

- `block.py`
  Lógica de padding usada por DES.

- `src/des.txt`
  Texto de prueba para DES.

- `src/3des.txt`
  Texto de prueba para 3DES.

- `images/pic.png`
  Imagen base para la demostración de AES.

- `images/aes_ecb.bmp`
  Resultado esperado del cifrado en ECB.

- `images/aes_cbc.bmp`
  Resultado esperado del cifrado en CBC.

- `test/test_cipher.py`
  Ejecuta pruebas de DES, 3DES y AES.

- `requirements.txt`
  Dependencias específicas de esta carpeta.

Dependencias externas:

- `pycryptodome`
- `Pillow`

Ejemplos de ejecución:

```bash
python "ejercicio block/src/des_cipher.py"
python "ejercicio block/src/tripledes_cipher.py"
python "ejercicio block/src/aes_cipher.py"
python "ejercicio block/test/test_cipher.py"
```

### 5. `RSA/`

Ejemplos de criptografía asimétrica:

- `generar_claves.py`
  Genera un par de claves RSA y crea `public_key.pem` y `private_key.pem`.

- `rsa_OAEP.py`
  Cifra y descifra mensajes cortos usando RSA con OAEP.

- `rsa_AES_GCM.py`
  Implementa cifrado híbrido:
  - cifra el documento con AES-256-GCM
  - cifra la clave AES con RSA-OAEP
  - empaqueta nonce, tag, clave cifrada y ciphertext

- `RSA.ipynb`
  Notebook de apoyo para esta unidad.

- `README.md`
  Documentación interna de esta carpeta.

Dependencias externas:

- `pycryptodome`

Ejemplos de ejecución:

```bash
python "RSA/generar_claves.py"
python "RSA/rsa_OAEP.py"
python "RSA/rsa_AES_GCM.py"
```

Importante:

- Primero ejecuta `python "RSA/generar_claves.py"` si aún no existen `public_key.pem` y `private_key.pem`.

## Archivos principales fuera de carpetas

### `asciibin.py`

Demuestra:

- ASCII a binario
- binario a ASCII
- binario a Base64
- Base64 a binario
- Base64 a ASCII
- XOR bit a bit

Ejemplo de ejecución:

```bash
python asciibin.py
```

### `historia_de_criptografia.ipynb`

Notebook para lectura o ejecución interactiva.

Para abrirlo:

```bash
jupyter notebook
```

Luego selecciona el archivo `historia_de_criptografia.ipynb`.

## Orden recomendado para probar todo el proyecto

Si quieres recorrer el proyecto de forma ordenada, puedes ejecutar:

```bash
python asciibin.py
python "criptografia historia/cesar.py"
python "criptografia historia/ROT13.py"
python "criptografia historia/vigenere.py"
python "criptografia historia/analisis_frecuencia.py"
python "keys/keys.py"
python "keys/cypher_llave_fija.py"
python "keys/cypher_llave_dinamica.py"
python "ejercicio stream/keystream.py"
python "ejercicio stream/validacion_pruebas.py"
python "ejercicio stream/pruebas_unitarias.py"
python "ejercicio block/src/des_cipher.py"
python "ejercicio block/src/tripledes_cipher.py"
python "ejercicio block/src/aes_cipher.py"
python "ejercicio block/test/test_cipher.py"
python "RSA/generar_claves.py"
python "RSA/rsa_OAEP.py"
python "RSA/rsa_AES_GCM.py"
```

## Ejemplo completo de instalación y ejecución

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install pycryptodome Pillow jupyter
python asciibin.py
python "ejercicio stream/pruebas_unitarias.py"
python "ejercicio block/test/test_cipher.py"
python "RSA/generar_claves.py"
python "RSA/rsa_OAEP.py"
```

## Notas importantes

- Las carpetas con espacios en su nombre deben ejecutarse entre comillas, por ejemplo:

```bash
python "ejercicio block/src/aes_cipher.py"
```

- `pycryptodome` es indispensable para los módulos de `RSA/` y `ejercicio block/`.

- `Pillow` es indispensable para ejecutar el cifrado de imágenes en AES.

- Los notebooks `.ipynb` no son obligatorios para correr los scripts `.py`.

- Si ya tienes creadas las carpetas `.venv/` o `venv/`, puedes usarlas, pero se recomienda trabajar con un solo entorno virtual para evitar confusión.
