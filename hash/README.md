# Carpeta `hash`

Esta carpeta contiene ejercicios y utilidades relacionadas con funciones hash, verificacion de integridad y autenticidad usando firmas digitales con RSA.

## Archivos Python

### `explorar_hashes.py`

Calcula y compara hashes de dos cadenas:

- `MediSoft-v2.1.0`
- `medisoft-v2.1.0`

Muestra una tabla con los algoritmos `MD5`, `SHA1`, `SHA256` y `SHA3_256`, incluyendo longitud en bits, longitud hexadecimal y valor del hash. Sirve para observar diferencias entre algoritmos y el efecto avalancha.

### `generacion_claves.py`

Genera hashes `SHA-256` para una lista de contrasenas y consulta la API de `Have I Been Pwned` para saber cuantas veces aparece cada contrasena en filtraciones conocidas.

Puntos importantes:

- Imprime el hash `SHA-256` de cada contrasena.
- Usa `SHA-1` para consultar la API, porque ese es el formato compatible con `Pwned Passwords`.
- Requiere conexion a Internet para poder consultar la API.

### `generar_manifiesto.py`

Simula el lado de MediSoft al publicar un paquete.

Hace lo siguiente:

- Recibe la ruta de 5 o mas archivos.
- Calcula el `SHA-256` de cada archivo.
- Agrega una linea al historial `SHA256SUMS.txt` con el formato:

```text
<HASH> <nombre_archivo>
```

Sirve para crear o ampliar el manifiesto de integridad del paquete.

### `verificar_paquete.py`

Simula el lado del hospital o del administrador TI.

Hace lo siguiente:

- Lee `SHA256SUMS.txt`.
- Recalcula el `SHA-256` de cada archivo listado.
- Reporta si cada archivo esta `OK`, `NO COINCIDE` o `FALTANTE`.

Sirve para detectar alteraciones en los archivos del paquete.

### `generar_claves_rsa.py`

Genera un par de claves RSA de `2048` bits con `pycryptodome`.

Archivos generados:

- `medisoft_priv.pem`: clave privada de MediSoft.
- `medisoft_pub.pem`: clave publica de MediSoft.

La clave privada debe mantenerse secreta. La clave publica puede compartirse con el hospital para verificar firmas.

### `firmar_manifiesto.py`

Firma digitalmente el archivo `SHA256SUMS.txt`.

Hace lo siguiente:

- Calcula el `SHA-256` del contenido del manifiesto.
- Firma ese hash con la clave privada `medisoft_priv.pem`.
- Guarda la firma en un archivo binario `SHA256SUMS.sig`.

Usa el esquema `PKCS#1 v1.5`.

### `verificar_firma.py`

Verifica la autenticidad del manifiesto firmado.

Hace lo siguiente:

- Usa la clave publica `medisoft_pub.pem`.
- Lee `SHA256SUMS.txt`.
- Lee `SHA256SUMS.sig`.
- Recalcula el `SHA-256` del manifiesto.
- Valida la firma digital.

Si el manifiesto fue modificado, la firma deja de ser valida. Si solo cambia un archivo del paquete pero el manifiesto sigue intacto, la firma sigue siendo valida y el problema se detecta con `verificar_paquete.py`.

## Dependencias

La unica libreria externa necesaria para ejecutar todos los `.py` de esta carpeta es:

- `pycryptodome`

El resto de modulos usados (`argparse`, `hashlib`, `pathlib`, `sys`, `os`, `string`, `urllib`) forman parte de la biblioteca estandar de Python.

## Instalacion en un entorno virtual de Python

### 1. Crear el entorno virtual

En PowerShell, desde la raiz del proyecto:

```powershell
python -m venv .venv
```

### 2. Activar el entorno virtual

```powershell
.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activacion, puedes habilitarla para el usuario actual con:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Instalar dependencias

```powershell
pip install -r hash\requirements.txt
```

### 4. Verificar la instalacion

```powershell
python -c "from Crypto.PublicKey import RSA; print('pycryptodome OK')"
```

## Ejemplos de uso

### Comparar hashes

```powershell
python hash\explorar_hashes.py
```

### Consultar filtraciones de contrasenas

```powershell
python hash\generacion_claves.py
```

### Generar manifiesto SHA-256

```powershell
python hash\generar_manifiesto.py hash\paquete_demo\bin\medisoft_core.dll hash\paquete_demo\config\appsettings.ini hash\paquete_demo\docs\release_notes.txt hash\paquete_demo\modules\triage_rules.json hash\paquete_demo\sql\migracion_2026_03.sql --manifiesto hash\paquete_demo\SHA256SUMS.txt
```

### Verificar integridad del paquete

```powershell
python hash\verificar_paquete.py --manifiesto hash\paquete_demo\SHA256SUMS.txt
```

### Generar claves RSA

```powershell
python hash\generar_claves_rsa.py
```

### Firmar el manifiesto

```powershell
python hash\firmar_manifiesto.py hash\paquete_demo\SHA256SUMS.txt
```

### Verificar la firma digital

```powershell
python hash\verificar_firma.py hash\paquete_demo\SHA256SUMS.txt
```
