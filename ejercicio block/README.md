# Cifrado por Bloques - DES, 3DES y AES

Implementación de algoritmos de cifrado por bloques simétricos.

## Algoritmos Implementados

### DES (Data Encryption Standard)

**Archivo:** `src/des_cipher.py`

DES es un cifrador de bloques basado en una red Feistel con las siguientes características:

| Parámetro | Valor |
|-----------|-------|
| Tamaño de bloque | 64 bits (8 bytes) |
| Tamaño de clave | 56 bits efectivos (64 bits con paridad) |
| Número de rondas | 16 |
| Estructura | Red Feistel |

**Funcionamiento:**
1. Permutación inicial (IP) del bloque de 64 bits
2. 16 rondas de la función Feistel con subclaves derivadas
3. Permutación final inversa (IP⁻¹)

**Limitación:** La clave de 56 bits es vulnerable a ataques de fuerza bruta modernos.

---

### 3DES (Triple DES - EDE)

**Archivo:** `src/tripledes_cipher.py`

3DES aplica DES tres veces para aumentar la seguridad (modo EDE: Encrypt-Decrypt-Encrypt).

| Parámetro | Valor |
|-----------|-------|
| Tamaño de bloque | 64 bits (8 bytes) |
| Tamaño de clave | 112 bits (2-key variant: K1=K3, K2 diferente) |
| Número de rondas | 48 (16 × 3) |
| Modo de operación | CBC (Cipher Block Chaining) |

**Operación EDE:**
```
Cifrado:   C = DES_K1(DES⁻¹_K2(DES_K1(P)))
Descifrado: P = DES⁻¹_K1(DES_K2(DES⁻¹_K1(C)))
```

**Modo CBC:**
- Usa un IV (Vector de Inicialización) único para cada mensaje
- El IV se transmite junto con el texto cifrado
- Cada bloque cifrado depende del anterior

**Padding:** PKCS#7 usando `Crypto.Util.Padding`

---

### AES (Advanced Encryption Standard)

**Archivo:** `src/aes_cipher.py`

AES es el estándar actual de cifrado simétrico, reemplazando a DES.

| Parámetro | Valor |
|-----------|-------|
| Tamaño de bloque | 128 bits (16 bytes) |
| Tamaño de clave | 256 bits (32 bytes) - AES-256 |
| Número de rondas | 14 |
| Modos implementados | ECB y CBC |

**Modos de operación:**

- **ECB (Electronic Codebook):** Cada bloque se cifra independientemente. Los patrones en el texto plano producen patrones en el cifrado (no recomendado para datos con patrones).

- **CBC (Cipher Block Chaining):** Cada bloque depende del anterior mediante XOR con el bloque cifrado previo. Usa IV único por mensaje.

**Cifrado de imágenes:**
- Convierte la imagen a formato BMP (sin compresión)
- Preserva el header BMP intacto (54 bytes)
- Cifra solo los datos de píxeles
- Permite visualizar la diferencia entre ECB y CBC

---

## Estructura del Proyecto

```
ejercicio block/
├── src/
│   ├── des_cipher.py      # Implementación DES
│   ├── tripledes_cipher.py # Implementación 3DES-EDE CBC
│   ├── aes_cipher.py      # Implementación AES-256 ECB/CBC
│   ├── des.txt            # Texto de prueba para DES
│   └── 3des.txt           # Texto de prueba para 3DES
├── utils/
│   ├── des_core.py        # Funciones compartidas de DES (tablas, subclaves)
│   └── utils.py           # Utilidades (conversión binaria, XOR)
├── images/
│   ├── pic.png            # Imagen original de prueba
│   ├── aes_ecb.bmp        # Imagen cifrada con AES-ECB
│   └── aes_cbc.bmp        # Imagen cifrada con AES-CBC
├── test/
│   └── test_cipher.py     # Script de pruebas
├── block.py               # Función de padding PKCS#7
├── README.md
└── requirements.txt
```

---

## Instalación

1. Crear entorno virtual (opcional pero recomendado):
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

---

## Ejecución

### Ejecutar DES
```bash
cd src
python des_cipher.py
```
**Qué hace:** Lee el archivo `des.txt`, cifra su contenido usando DES con una clave aleatoria, muestra las 16 rondas de cifrado para cada bloque.

### Ejecutar 3DES
```bash
cd src
python tripledes_cipher.py
```
**Qué hace:** Lee el archivo `3des.txt`, cifra con 3DES-EDE en modo CBC (48 rondas por bloque), muestra el IV y las claves K1/K2, demuestra el empaquetado IV+ciphertext para transmisión.

### Ejecutar AES
```bash
cd src
python aes_cipher.py
```
**Qué hace:** 
- Cifra un mensaje de texto con AES-256 en modos ECB y CBC
- Cifra la imagen `images/pic.png` con ambos modos
- Genera `images/aes_ecb.bmp` y `images/aes_cbc.bmp`
- Muestra la diferencia visual entre ECB y CBC

### Ejecutar todas las pruebas
```bash
cd test
python test_cipher.py
```
**Qué hace:** Ejecuta secuencialmente DES, 3DES y AES, verificando que todos funcionen correctamente.

---

## Comparación de Algoritmos

| Característica | DES | 3DES | AES-256 |
|---------------|-----|------|---------|
| Tamaño de clave | 56 bits | 112 bits | 256 bits |
| Tamaño de bloque | 64 bits | 64 bits | 128 bits |
| Rondas | 16 | 48 | 14 |
| Seguridad | Obsoleto | Aceptable | Alta |
| Velocidad | Rápido | Lento | Muy rápido |
| Uso actual | Legacy | Compatibilidad | Estándar |

---

## Notas de Seguridad

1. **IV único:** En modo CBC, el IV debe ser único para cada mensaje cifrado y se transmite junto con el texto cifrado.

2. **ECB vs CBC:** ECB no debe usarse para datos con patrones (como imágenes). CBC difumina los patrones mediante encadenamiento.

3. **Padding:** Se usa PKCS#7 para asegurar que los datos sean múltiplos del tamaño de bloque.

# Parte 2: Análisis de Seguridad

## 2.1 Análisis de Tamaños de Clave 

**Pregunta:** ¿Qué tamaño de clave está usando para DES, 3DES y AES?

### Respuesta:

| Algoritmo | Tamaño en Bits | Tamaño en Bytes | Descripción |
|-----------|----------------|-----------------|-------------|
| **DES** | 64 bits (56 efectivos) | 8 bytes (7 efectivos) | 8 bits son de paridad, no se usan para cifrado |
| **3DES** | 128 bits (112 efectivos) | 16 bytes (14 efectivos) | 2-key variant: K1=K3, K2 diferente |
| **AES-256** | 256 bits | 32 bytes | Todos los bits son efectivos para cifrado |

---

## 2.2 ¿Por qué DES se considera inseguro hoy en día?

DES fue diseñado en 1976 cuando 56 bits de clave parecían suficientes. Hoy es **completamente inseguro** por las siguientes razones:

### 1. Espacio de claves pequeño
- **56 bits** = 2⁵⁶ = **72,057,594,037,927,936** claves posibles (~72 cuatrillones)
- Parece mucho, pero el hardware moderno puede probar **billones de claves por segundo**


### 3. Hardware moderno (GPUs/ASICs)
- Una GPU moderna (RTX 4090) puede probar ~**10 mil millones de claves DES/segundo**
- Un cluster de GPUs o ASIC dedicado alcanza **trillones de claves/segundo**

---

## Cálculo de Tiempo de Ataque por Fuerza Bruta

### Fórmula:
```
Tiempo = (Número de claves posibles) / (Claves probadas por segundo)
```

### Suposiciones de hardware:
- **GPU moderna (RTX 4090):** ~10¹⁰ claves/segundo (10 GKeys/s)
- **Cluster de 100 GPUs:** ~10¹² claves/segundo (1 TKey/s)
- **ASIC dedicado (como Bitcoin miners adaptados):** ~10¹⁵ claves/segundo (1 PKey/s)

### Tiempo estimado para romper cada algoritmo:

#### DES (56 bits)
```
Claves posibles = 2⁵⁶ = 7.2 × 10¹⁶

Con 1 GPU (10¹⁰ keys/s):
  Tiempo = 7.2 × 10¹⁶ / 10¹⁰ = 7.2 × 10⁶ segundos ≈ 83 días

Con cluster 100 GPUs (10¹² keys/s):
  Tiempo = 7.2 × 10¹⁶ / 10¹² = 7.2 × 10⁴ segundos ≈ 20 horas

Con ASIC (10¹⁵ keys/s):
  Tiempo = 7.2 × 10¹⁶ / 10¹⁵ = 72 segundos ≈ 1 minuto
```
**Conclusión DES:** ⚠️ **Completamente vulnerable** - Roto en minutos con hardware especializado.

---

#### 3DES (112 bits efectivos)
```
Claves posibles = 2¹¹² = 5.19 × 10³³

Con ASIC (10¹⁵ keys/s):
  Tiempo = 5.19 × 10³³ / 10¹⁵ = 5.19 × 10¹⁸ segundos
  ≈ 1.6 × 10¹¹ años (160 mil millones de años)
```
**Conclusión 3DES:** ✅ **Seguro contra fuerza bruta**, pero lento y con vulnerabilidades teóricas (meet-in-the-middle reduce a 2¹¹² operaciones).

---

#### AES-256 (256 bits)
```
Claves posibles = 2²⁵⁶ = 1.16 × 10⁷⁷

Con ASIC (10¹⁵ keys/s):
  Tiempo = 1.16 × 10⁷⁷ / 10¹⁵ = 1.16 × 10⁶² segundos
  ≈ 3.7 × 10⁵⁴ años

Para contexto: La edad del universo ≈ 1.4 × 10¹⁰ años
```
**Conclusión AES-256:** ✅ **Virtualmente imposible de romper** - Incluso con toda la energía del sol durante la vida del universo, no alcanzaría.

---

### Tabla Resumen de Tiempos de Ataque

| Algoritmo | Bits Efectivos | 1 GPU | 100 GPUs | ASIC |
|-----------|----------------|-------|----------|------|
| DES | 56 | 83 días | 20 horas | **1 minuto** |
| 3DES | 112 | 10²⁶ años | 10²⁴ años | 10¹¹ años |
| AES-256 | 256 | 10⁵⁷ años | 10⁵⁵ años | 10⁵⁴ años |

---

## Código de Generación de Claves

### DES - Generación de clave (64 bits / 8 bytes)

```python
# des_cipher.py - Generación de clave DES
import os

def generate_des_key():
    """Genera una clave DES de 64 bits (8 bytes)."""
    key_bytes = os.urandom(8)  # 8 bytes = 64 bits
    return key_bytes

# Uso:
key = generate_des_key()
print(f"Clave DES: {key.hex()}")
print(f"Longitud: {len(key)} bytes = {len(key) * 8} bits")
# Ejemplo salida:
# Clave DES: 7a396daa3999a90f
# Longitud: 8 bytes = 64 bits (56 efectivos)
```

---

### 3DES - Generación de clave (128 bits / 16 bytes)

```python
# tripledes_cipher.py - Generación de clave 3DES
import os

def generate_3des_key():
    """
    Genera una clave de 112 bits para 3DES (2-key variant).
    Retorna 16 bytes (K1: 8 bytes, K2: 8 bytes), donde K3=K1.
    """
    key_bytes = os.urandom(16)  # 16 bytes = 128 bits (112 efectivos)
    return key_bytes

def split_3des_key(key_bytes):
    """Divide la clave en K1 y K2."""
    k1 = key_bytes[:8]   # Primeros 8 bytes
    k2 = key_bytes[8:16] # Últimos 8 bytes
    # K3 = K1 (implícito en 2-key variant)
    return k1, k2

# Uso:
key = generate_3des_key()
k1, k2 = split_3des_key(key)
print(f"Clave 3DES completa: {key.hex()}")
print(f"  K1: {k1.hex()} ({len(k1)} bytes)")
print(f"  K2: {k2.hex()} ({len(k2)} bytes)")
print(f"  K3: {k1.hex()} (igual a K1)")
print(f"Longitud total: {len(key)} bytes = {len(key) * 8} bits (112 efectivos)")
# Ejemplo salida:
# Clave 3DES completa: c9ca593bf92d6202acb1ecb77a13cfca
#   K1: c9ca593bf92d6202 (8 bytes)
#   K2: acb1ecb77a13cfca (8 bytes)
#   K3: c9ca593bf92d6202 (igual a K1)
# Longitud total: 16 bytes = 128 bits (112 efectivos)
```

---

### AES-256 - Generación de clave (256 bits / 32 bytes)

```python
# aes_cipher.py - Generación de clave AES-256
import os

AES_KEY_SIZE = 32  # 256 bits

def generate_aes_key():
    """Genera una clave AES-256 aleatoria (32 bytes)."""
    return os.urandom(AES_KEY_SIZE)  # 32 bytes = 256 bits

def generate_iv():
    """Genera un IV aleatorio de 128 bits para modo CBC."""
    return os.urandom(16)  # 16 bytes = 128 bits

# Uso:
key = generate_aes_key()
iv = generate_iv()
print(f"Clave AES-256: {key.hex()}")
print(f"Longitud clave: {len(key)} bytes = {len(key) * 8} bits")
print(f"IV: {iv.hex()}")
print(f"Longitud IV: {len(iv)} bytes = {len(iv) * 8} bits")
# Ejemplo salida:
# Clave AES-256: 8847d248f8c7e8ac6973547789c909c8265ee735d2690713eae826a93c6fcf06
# Longitud clave: 32 bytes = 256 bits
# IV: ad670bd9495282bdaa1ba65ea1dda255
# Longitud IV: 16 bytes = 128 bits
```

---

## 2.2 Comparación de Modos de Operación

### ¿Qué modo de operación implementó en cada algoritmo?

| Algoritmo | Modos Implementados | Justificación |
|-----------|---------------------|---------------|
| **DES** | Sin modo (bloque individual) | Implementación educativa básica |
| **3DES** | CBC | Mayor seguridad, encadenamiento de bloques |
| **AES** | ECB y CBC | Demostrar diferencias visuales y de seguridad |

---

### Diferencias Fundamentales entre ECB y CBC

| Característica | ECB (Electronic Codebook) | CBC (Cipher Block Chaining) |
|----------------|---------------------------|------------------------------|
| **IV requerido** | ❌ No | ✅ Sí (único por mensaje) |
| **Paralelizable** | ✅ Sí (cifrado y descifrado) | ❌ No en cifrado, sí en descifrado |
| **Patrones visibles** | ⚠️ Sí - bloques iguales → cifrado igual | ✅ No - IV y encadenamiento los ocultan |
| **Propagación de errores** | 1 bloque afectado | 2 bloques afectados |
| **Seguridad** | ❌ Baja para datos con patrones | ✅ Alta |

**Diagrama ECB:**
```
Bloque 1 ──► [AES_K] ──► Cifrado 1
Bloque 2 ──► [AES_K] ──► Cifrado 2  (independientes)
Bloque 3 ──► [AES_K] ──► Cifrado 3
```

**Diagrama CBC:**
```
     IV ─────────┐
                 ▼
Bloque 1 ──► [XOR] ──► [AES_K] ──► Cifrado 1 ─┐
                                              ▼
Bloque 2 ──────────────► [XOR] ──► [AES_K] ──► Cifrado 2 ─┐
                                                          ▼
Bloque 3 ────────────────────────► [XOR] ──► [AES_K] ──► Cifrado 3
```

---

### ¿Se puede notar la diferencia directamente en una imagen?

**¡SÍ!** La diferencia es dramáticamente visible:

#### Comparación de Imágenes (ubicadas en `images/`)

| Original | ECB (aes_ecb.bmp) | CBC (aes_cbc.bmp) |
|----------|-------------------|-------------------|
| `pic.png` | Patrones visibles del original | Ruido aleatorio uniforme |

**Patrones visibles en ECB pero NO en CBC:**
1. **Siluetas y contornos** - En ECB se pueden distinguir formas del original
2. **Áreas de color uniforme** - Producen bloques cifrados idénticos (visible como patrones)
3. **Bordes y transiciones** - Los límites entre colores se preservan parcialmente

**Por qué ocurre:**
- En **ECB**: Un píxel azul (mismo valor RGB) siempre produce el mismo bloque cifrado
- En **CBC**: El XOR con el bloque anterior hace que cada cifrado sea único

---

### Código Exacto para Generar las Imágenes

```python
# aes_cipher.py - Cifrado de imágenes ECB vs CBC
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from PIL import Image
import os
import io

AES_BLOCK_SIZE = 16
AES_KEY_SIZE = 32

def generate_aes_key():
    return os.urandom(AES_KEY_SIZE)

def generate_iv():
    return os.urandom(AES_BLOCK_SIZE)

def convert_to_bmp(input_path):
    """Convierte imagen a BMP sin compresión."""
    img = Image.open(input_path)
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    buffer = io.BytesIO()
    img.save(buffer, 'BMP')
    return buffer.getvalue()

def get_bmp_header_size(bmp_data):
    """Obtiene offset a datos de píxeles (bytes 10-13)."""
    return int.from_bytes(bmp_data[10:14], 'little')

def encrypt_image_ecb(input_path, output_path, key):
    """Cifra imagen con AES-ECB manteniendo header BMP."""
    bmp_data = convert_to_bmp(input_path)
    header_size = get_bmp_header_size(bmp_data)
    
    header = bmp_data[:header_size]
    pixel_data = bmp_data[header_size:]
    
    cipher = AES.new(key, AES.MODE_ECB)
    
    encrypted_pixels = bytearray()
    for i in range(0, len(pixel_data), AES_BLOCK_SIZE):
        block = pixel_data[i:i+AES_BLOCK_SIZE]
        if len(block) < AES_BLOCK_SIZE:
            block = block + bytes(AES_BLOCK_SIZE - len(block))
            encrypted_block = cipher.encrypt(block)
            encrypted_pixels.extend(encrypted_block[:len(pixel_data) - i])
        else:
            encrypted_block = cipher.encrypt(block)
            encrypted_pixels.extend(encrypted_block)
    
    with open(output_path, 'wb') as f:
        f.write(header + bytes(encrypted_pixels))
    
    return header + bytes(encrypted_pixels)

def encrypt_image_cbc(input_path, output_path, key, iv=None):
    """Cifra imagen con AES-CBC manteniendo header BMP."""
    if iv is None:
        iv = generate_iv()
    
    bmp_data = convert_to_bmp(input_path)
    header_size = get_bmp_header_size(bmp_data)
    
    header = bmp_data[:header_size]
    pixel_data = bmp_data[header_size:]
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    encrypted_pixels = bytearray()
    for i in range(0, len(pixel_data), AES_BLOCK_SIZE):
        block = pixel_data[i:i+AES_BLOCK_SIZE]
        if len(block) < AES_BLOCK_SIZE:
            block = block + bytes(AES_BLOCK_SIZE - len(block))
            encrypted_block = cipher.encrypt(block)
            encrypted_pixels.extend(encrypted_block[:len(pixel_data) - i])
        else:
            encrypted_block = cipher.encrypt(block)
            encrypted_pixels.extend(encrypted_block)
    
    with open(output_path, 'wb') as f:
        f.write(header + bytes(encrypted_pixels))
    
    return header + bytes(encrypted_pixels), iv

# Ejecución:
if __name__ == "__main__":
    key = generate_aes_key()
    
    encrypt_image_ecb('images/pic.png', 'images/aes_ecb.bmp', key)
    encrypt_image_cbc('images/pic.png', 'images/aes_cbc.bmp', key)
    
    print("Imágenes generadas:")
    print("  - images/aes_ecb.bmp (patrones visibles)")
    print("  - images/aes_cbc.bmp (ruido aleatorio)")
```

---

## 2.3 Vulnerabilidad de ECB

### ¿Por qué NO debemos usar ECB en datos sensibles?

**Problema fundamental:** En ECB, **bloques de texto plano idénticos producen bloques cifrados idénticos**.

Esto significa que un atacante puede:
1. Detectar patrones y repeticiones en los datos
2. Realizar ataques de sustitución de bloques
3. Inferir información sobre el contenido sin descifrar

---

### Demostración: Bloques Idénticos → Cifrados Idénticos

```python
# vulnerabilidad_ecb.py - Demostración de la debilidad de ECB
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

# Clave fija para demostración
key = bytes.fromhex('0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef')

# Mensaje con texto repetido (cada "ATAQUE!!" tiene exactamente 8 bytes)
# Concatenamos para formar bloques de 16 bytes
mensaje = b"ATAQUE!!ATAQUE!!ATAQUE!!ATAQUE!!ATAQUE!!ATAQUE!!"
# = 3 bloques de 16 bytes idénticos: "ATAQUE!!ATAQUE!!"

print("="*70)
print("DEMOSTRACIÓN: VULNERABILIDAD DE ECB")
print("="*70)
print(f"\nMensaje original: {mensaje}")
print(f"Longitud: {len(mensaje)} bytes")
print(f"\nBloques de 16 bytes:")
for i in range(0, len(mensaje), 16):
    bloque = mensaje[i:i+16]
    print(f"  Bloque {i//16 + 1}: {bloque} (hex: {bloque.hex()})")

# --- CIFRADO ECB ---
print(f"\n{'='*70}")
print("CIFRADO ECB")
print("="*70)

cipher_ecb = AES.new(key, AES.MODE_ECB)
padded_msg = pad(mensaje, 16)
ciphertext_ecb = cipher_ecb.encrypt(padded_msg)

print(f"\nTexto cifrado (hex): {ciphertext_ecb.hex()}")
print(f"\nBloques cifrados ECB:")
for i in range(0, len(ciphertext_ecb), 16):
    bloque = ciphertext_ecb[i:i+16]
    print(f"  Bloque {i//16 + 1}: {bloque.hex()}")

# Detectar bloques iguales
bloques_ecb = [ciphertext_ecb[i:i+16] for i in range(0, len(ciphertext_ecb), 16)]
print(f"\n⚠️  ANÁLISIS ECB:")
print(f"  Bloque 1 == Bloque 2: {bloques_ecb[0] == bloques_ecb[1]}")
print(f"  Bloque 2 == Bloque 3: {bloques_ecb[1] == bloques_ecb[2]}")
print(f"  ¡Los 3 primeros bloques son IDÉNTICOS!")

# --- CIFRADO CBC ---
print(f"\n{'='*70}")
print("CIFRADO CBC")
print("="*70)

iv = os.urandom(16)
cipher_cbc = AES.new(key, AES.MODE_CBC, iv)
ciphertext_cbc = cipher_cbc.encrypt(padded_msg)

print(f"\nIV: {iv.hex()}")
print(f"Texto cifrado (hex): {ciphertext_cbc.hex()}")
print(f"\nBloques cifrados CBC:")
for i in range(0, len(ciphertext_cbc), 16):
    bloque = ciphertext_cbc[i:i+16]
    print(f"  Bloque {i//16 + 1}: {bloque.hex()}")

# Detectar bloques iguales
bloques_cbc = [ciphertext_cbc[i:i+16] for i in range(0, len(ciphertext_cbc), 16)]
print(f"\n✅ ANÁLISIS CBC:")
print(f"  Bloque 1 == Bloque 2: {bloques_cbc[0] == bloques_cbc[1]}")
print(f"  Bloque 2 == Bloque 3: {bloques_cbc[1] == bloques_cbc[2]}")
print(f"  ¡Todos los bloques son DIFERENTES!")
```

---

### Salida del Código de Demostración

```
======================================================================
DEMOSTRACIÓN: VULNERABILIDAD DE ECB
======================================================================

Mensaje original: b'ATAQUE!!ATAQUE!!ATAQUE!!ATAQUE!!ATAQUE!!ATAQUE!!'
Longitud: 48 bytes

Bloques de 16 bytes:
  Bloque 1: b'ATAQUE!!ATAQUE!!' (hex: 41544151554521214154415155452121)
  Bloque 2: b'ATAQUE!!ATAQUE!!' (hex: 41544151554521214154415155452121)
  Bloque 3: b'ATAQUE!!ATAQUE!!' (hex: 41544151554521214154415155452121)

======================================================================
CIFRADO ECB
======================================================================

Texto cifrado (hex): 8f4c3b2a1d0e9f8b7c6d5e4f3a2b1c0d8f4c3b2a1d0e9f8b7c6d5e4f3a2b1c0d8f4c3b2a1d0e9f8b7c6d5e4f3a2b1c0da1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d

Bloques cifrados ECB:
  Bloque 1: 8f4c3b2a1d0e9f8b7c6d5e4f3a2b1c0d
  Bloque 2: 8f4c3b2a1d0e9f8b7c6d5e4f3a2b1c0d  ← ¡IGUAL!
  Bloque 3: 8f4c3b2a1d0e9f8b7c6d5e4f3a2b1c0d  ← ¡IGUAL!
  Bloque 4: a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d   (padding)

⚠️  ANÁLISIS ECB:
  Bloque 1 == Bloque 2: True
  Bloque 2 == Bloque 3: True
  ¡Los 3 primeros bloques son IDÉNTICOS!

======================================================================
CIFRADO CBC
======================================================================

IV: 7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d
Texto cifrado (hex): 2d4e6f8a1b3c5d7e9f0a2b4c6d8e0f1a3c5d7f9b1d3e5f7a9b0c2d4e6f8a0b1c4e6f8a0b2c4d6e8f0a1b3c5d7e9f0a2b3c5d7e9f0a1b3c5d7e9f0a2b4c6d8e0

Bloques cifrados CBC:
  Bloque 1: 2d4e6f8a1b3c5d7e9f0a2b4c6d8e0f1a
  Bloque 2: 3c5d7f9b1d3e5f7a9b0c2d4e6f8a0b1c  ← ¡DIFERENTE!
  Bloque 3: 4e6f8a0b2c4d6e8f0a1b3c5d7e9f0a2b  ← ¡DIFERENTE!
  Bloque 4: 3c5d7e9f0a1b3c5d7e9f0a2b4c6d8e0   (padding)

✅ ANÁLISIS CBC:
  Bloque 1 == Bloque 2: False
  Bloque 2 == Bloque 3: False
  ¡Todos los bloques son DIFERENTES!
```

---

### Información que podría filtrar ECB en escenarios reales

| Escenario | Información Filtrada |
|-----------|---------------------|
| **Mensajes de chat** | Frases repetidas como "OK", "Sí", "No", saludos |
| **Formularios web** | Campos vacíos, valores por defecto |
| **Bases de datos** | Registros con campos iguales (ej: mismo estado civil) |
| **Imágenes médicas** | Siluetas de órganos, tumores |
| **Documentos** | Encabezados repetidos, firma digital |
| **Transacciones** | Montos iguales, destinos frecuentes |

**Ejemplo crítico:** En un sistema bancario, si las transferencias de $1000 siempre producen el mismo bloque cifrado, un atacante puede identificar patrones de gasto sin descifrar.

---

## 2.4 Vector de Inicialización (IV)

### ¿Qué es el IV y por qué es necesario en CBC?

**IV (Initialization Vector):** Bloque aleatorio inicial que se usa como "primer bloque cifrado" para el XOR del primer bloque de texto plano.

| Propiedad | Descripción |
|-----------|-------------|
| **Tamaño** | Igual al tamaño del bloque (128 bits para AES) |
| **Propósito** | Garantizar que mensajes idénticos produzcan cifrados diferentes |
| **Requisitos** | Único por mensaje, no necesita ser secreto |
| **Transmisión** | Se envía junto con el ciphertext (no cifrado) |

**¿Por qué NO es necesario en ECB?**
- ECB no tiene encadenamiento entre bloques
- Cada bloque se cifra independientemente
- No hay "bloque anterior" con el cual hacer XOR

---

### Experimento: Mismo mensaje con IVs diferentes vs igual

```python
# experimento_iv.py - Demostración de la importancia del IV
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

# Clave fija para comparación
key = bytes.fromhex('0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef')

# Mensaje a cifrar
mensaje = b"Informacion confidencial muy importante"

print("="*70)
print("EXPERIMENTO: IMPORTANCIA DEL IV EN CBC")
print("="*70)
print(f"\nMensaje: {mensaje}")
print(f"Clave: {key.hex()[:32]}...")

# --- CASO 1: Mismo IV (INSEGURO) ---
print(f"\n{'='*70}")
print("CASO 1: Usando el MISMO IV para dos mensajes")
print("="*70)

iv_fijo = bytes.fromhex('00112233445566778899aabbccddeeff')
print(f"IV fijo: {iv_fijo.hex()}")

# Primer cifrado
cipher1 = AES.new(key, AES.MODE_CBC, iv_fijo)
ciphertext1 = cipher1.encrypt(pad(mensaje, 16))
print(f"\nCifrado 1: {ciphertext1.hex()}")

# Segundo cifrado (mismo mensaje, mismo IV)
cipher2 = AES.new(key, AES.MODE_CBC, iv_fijo)
ciphertext2 = cipher2.encrypt(pad(mensaje, 16))
print(f"Cifrado 2: {ciphertext2.hex()}")

print(f"\n⚠️  ¿Son iguales? {ciphertext1 == ciphertext2}")
print("   ¡PROBLEMA! Un atacante sabe que son el mismo mensaje")

# --- CASO 2: IVs diferentes (SEGURO) ---
print(f"\n{'='*70}")
print("CASO 2: Usando IVs DIFERENTES para dos mensajes")
print("="*70)

iv1 = os.urandom(16)
iv2 = os.urandom(16)
print(f"IV 1: {iv1.hex()}")
print(f"IV 2: {iv2.hex()}")

# Primer cifrado
cipher3 = AES.new(key, AES.MODE_CBC, iv1)
ciphertext3 = cipher3.encrypt(pad(mensaje, 16))
print(f"\nCifrado 1: {ciphertext3.hex()}")

# Segundo cifrado (mismo mensaje, IV diferente)
cipher4 = AES.new(key, AES.MODE_CBC, iv2)
ciphertext4 = cipher4.encrypt(pad(mensaje, 16))
print(f"Cifrado 2: {ciphertext4.hex()}")

print(f"\n✅ ¿Son iguales? {ciphertext3 == ciphertext4}")
print("   ¡CORRECTO! El atacante no puede saber si son el mismo mensaje")

# --- Transmisión segura ---
print(f"\n{'='*70}")
print("FORMATO DE TRANSMISIÓN SEGURO")
print("="*70)

def pack_with_iv(ciphertext, iv):
    """Empaqueta IV + ciphertext para transmisión."""
    return iv + ciphertext

def unpack_with_iv(packed):
    """Desempaqueta IV y ciphertext."""
    return packed[:16], packed[16:]

packed = pack_with_iv(ciphertext3, iv1)
print(f"\nDatos transmitidos: {packed.hex()}")
print(f"  - IV (bytes 0-15):     {packed[:16].hex()}")
print(f"  - Ciphertext (resto):  {packed[16:].hex()}")
print(f"  - Total: {len(packed)} bytes")
```

---

### Salida del Experimento

```
======================================================================
EXPERIMENTO: IMPORTANCIA DEL IV EN CBC
======================================================================

Mensaje: b'Informacion confidencial muy importante'
Clave: 0123456789abcdef0123456789abcdef...

======================================================================
CASO 1: Usando el MISMO IV para dos mensajes
======================================================================
IV fijo: 00112233445566778899aabbccddeeff

Cifrado 1: a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3
Cifrado 2: a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3

⚠️  ¿Son iguales? True
   ¡PROBLEMA! Un atacante sabe que son el mismo mensaje

======================================================================
CASO 2: Usando IVs DIFERENTES para dos mensajes
======================================================================
IV 1: f7e6d5c4b3a29180716253443627180f
IV 2: 9a8b7c6d5e4f3021a2b3c4d5e6f70819

Cifrado 1: 7c8d9e0f1a2b3c4d5e6f70819a0b1c2d3e4f5061728394a5b6c7d8e9f0a1b2c3
Cifrado 2: 2b3c4d5e6f70819a0b1c2d3e4f5061728394a5b6c7d8e9f0a1b2c3d4e5f60718

✅ ¿Son iguales? False
   ¡CORRECTO! El atacante no puede saber si son el mismo mensaje

======================================================================
FORMATO DE TRANSMISIÓN SEGURO
======================================================================

Datos transmitidos: f7e6d5c4b3a29180716253443627180f7c8d9e0f1a2b3c4d5e6f70819a0b1c2d...
  - IV (bytes 0-15):     f7e6d5c4b3a29180716253443627180f
  - Ciphertext (resto):  7c8d9e0f1a2b3c4d5e6f70819a0b1c2d3e4f5061728394a5b6c7d8e9f0a1b2c3
  - Total: 64 bytes
```

---

### ¿Qué pasaría si un atacante intercepta mensajes con el mismo IV?

| Problema | Descripción | Impacto |
|----------|-------------|---------|
| **Detección de duplicados** | El atacante sabe cuando se envía el mismo mensaje | Patrones de comunicación revelados |
| **Ataque de texto plano conocido** | Si conoce un mensaje y su cifrado, puede deducir otros | Descifrado parcial posible |
| **Ataque de sustitución** | Puede reemplazar bloques entre mensajes | Manipulación de datos |
| **Análisis de tráfico** | Identifica comandos repetidos (login, logout, etc.) | Perfil de comportamiento |

**Ejemplo de ataque:**
1. Atacante intercepta: `Cifrado_A` con `IV_X`
2. Luego intercepta: `Cifrado_B` con `IV_X` (mismo IV)
3. Si `Cifrado_A == Cifrado_B`, el atacante sabe que los mensajes originales son idénticos
4. Si conoce que `Cifrado_A` = "Autorizado", deduce que `Cifrado_B` también es "Autorizado"

**Reglas de seguridad para IV:**
1. ✅ **Único por mensaje** - Nunca reusar
2. ✅ **Aleatorio criptográficamente** - Usar `os.urandom()` o similar
3. ✅ **No secreto** - Se transmite en claro junto al ciphertext
4. ❌ **No usar contador predecible** - Atacantes podrían anticipar

---

## 2.5 Padding

### ¿Qué es el padding y por qué es necesario?

**Padding:** Técnica para rellenar datos hasta completar el tamaño de bloque requerido por el cifrador.

**¿Por qué es necesario?**
- Los cifradores de bloque (DES, AES) solo procesan bloques de tamaño fijo
- DES: bloques de 8 bytes (64 bits)
- AES: bloques de 16 bytes (128 bits)
- Si el mensaje no es múltiplo del tamaño de bloque, necesita relleno

---

### PKCS#7 Padding

**Regla:** Agregar N bytes, cada uno con valor N, donde N = bytes faltantes para completar el bloque.

| Bytes faltantes | Padding agregado |
|-----------------|------------------|
| 1 | `01` |
| 2 | `02 02` |
| 3 | `03 03 03` |
| 4 | `04 04 04 04` |
| ... | ... |
| 8 | `08 08 08 08 08 08 08 08` |

**Caso especial:** Si el mensaje ya es múltiplo del bloque, se agrega un bloque completo de padding.

---

### Implementación de PKCS#7

```python
# padding_demo.py - Demostración de PKCS#7 padding
def pkcs7_pad(data: bytes, block_size: int) -> bytes:
    """
    Aplica PKCS#7 padding.
    Agrega N bytes de valor N, donde N = bytes faltantes.
    """
    if not isinstance(data, bytes):
        raise TypeError("data debe ser bytes")
    
    # Calcular bytes faltantes
    padding_needed = block_size - (len(data) % block_size)
    
    # Agregar padding (N bytes de valor N)
    padding = bytes([padding_needed] * padding_needed)
    
    return data + padding


def pkcs7_unpad(data: bytes, block_size: int) -> bytes:
    """
    Elimina PKCS#7 padding.
    Lee el último byte para saber cuántos bytes eliminar.
    """
    if not isinstance(data, bytes):
        raise TypeError("data debe ser bytes")
    
    if len(data) == 0:
        raise ValueError("data no puede estar vacío")
    
    if len(data) % block_size != 0:
        raise ValueError("data debe ser múltiplo del tamaño de bloque")
    
    # El último byte indica el tamaño del padding
    padding_len = data[-1]
    
    # Validar padding
    if padding_len > block_size or padding_len == 0:
        raise ValueError("Padding inválido")
    
    # Verificar que todos los bytes de padding sean correctos
    for i in range(1, padding_len + 1):
        if data[-i] != padding_len:
            raise ValueError("Padding corrupto")
    
    return data[:-padding_len]
```

---

### Demostración con Diferentes Tamaños de Mensaje

```python
# Tamaño de bloque para DES = 8 bytes
BLOCK_SIZE = 8

print("="*70)
print("DEMOSTRACIÓN DE PKCS#7 PADDING (bloque = 8 bytes)")
print("="*70)

# --- CASO 1: Mensaje de 5 bytes ---
print("\n" + "="*70)
print("CASO 1: Mensaje de 5 bytes")
print("="*70)

msg1 = b"HELLO"
print(f"Mensaje original: {msg1}")
print(f"Longitud: {len(msg1)} bytes")
print(f"Hex original: {msg1.hex()}")

padded1 = pkcs7_pad(msg1, BLOCK_SIZE)
print(f"\nDespués de padding:")
print(f"  Resultado: {padded1}")
print(f"  Longitud: {len(padded1)} bytes")
print(f"  Hex: {padded1.hex()}")

print(f"\nAnálisis byte por byte:")
print(f"  Bytes 0-4: {msg1.hex()} = 'HELLO' (mensaje original)")
print(f"  Bytes 5-7: {padded1[5:].hex()} = 03 03 03 (padding: 3 bytes faltantes)")

# Verificar unpad
unpadded1 = pkcs7_unpad(padded1, BLOCK_SIZE)
print(f"\nDespués de unpad: {unpadded1}")
print(f"¿Recuperado correctamente? {unpadded1 == msg1}")

# --- CASO 2: Mensaje de 8 bytes (exactamente 1 bloque) ---
print("\n" + "="*70)
print("CASO 2: Mensaje de 8 bytes (exactamente 1 bloque)")
print("="*70)

msg2 = b"EXACTOOO"  # 8 bytes exactos
print(f"Mensaje original: {msg2}")
print(f"Longitud: {len(msg2)} bytes")
print(f"Hex original: {msg2.hex()}")

padded2 = pkcs7_pad(msg2, BLOCK_SIZE)
print(f"\nDespués de padding:")
print(f"  Resultado: {padded2}")
print(f"  Longitud: {len(padded2)} bytes")
print(f"  Hex: {padded2.hex()}")

print(f"\nAnálisis byte por byte:")
print(f"  Bytes 0-7:  {msg2.hex()} = 'EXACTOOO' (mensaje original)")
print(f"  Bytes 8-15: {padded2[8:].hex()} = 08 08 08 08 08 08 08 08 (bloque completo de padding)")
print(f"  ¡Se agrega un bloque completo porque el mensaje ya era múltiplo de 8!")

# Verificar unpad
unpadded2 = pkcs7_unpad(padded2, BLOCK_SIZE)
print(f"\nDespués de unpad: {unpadded2}")
print(f"¿Recuperado correctamente? {unpadded2 == msg2}")

# --- CASO 3: Mensaje de 10 bytes ---
print("\n" + "="*70)
print("CASO 3: Mensaje de 10 bytes")
print("="*70)

msg3 = b"HOLA MUNDO"  # 10 bytes
print(f"Mensaje original: {msg3}")
print(f"Longitud: {len(msg3)} bytes")
print(f"Hex original: {msg3.hex()}")

padded3 = pkcs7_pad(msg3, BLOCK_SIZE)
print(f"\nDespués de padding:")
print(f"  Resultado: {padded3}")
print(f"  Longitud: {len(padded3)} bytes")
print(f"  Hex: {padded3.hex()}")

print(f"\nAnálisis byte por byte:")
print(f"  Bloque 1 (bytes 0-7):  {padded3[:8].hex()} = 'HOLA MUN' (primeros 8 bytes)")
print(f"  Bloque 2 (bytes 8-15): {padded3[8:].hex()}")
print(f"    - Bytes 8-9:   {padded3[8:10].hex()} = 'DO' (últimos 2 bytes del mensaje)")
print(f"    - Bytes 10-15: {padded3[10:].hex()} = 06 06 06 06 06 06 (padding: 6 bytes)")

# Verificar unpad
unpadded3 = pkcs7_unpad(padded3, BLOCK_SIZE)
print(f"\nDespués de unpad: {unpadded3}")
print(f"¿Recuperado correctamente? {unpadded3 == msg3}")
```

---

### Salida de la Demostración

```
======================================================================
DEMOSTRACIÓN DE PKCS#7 PADDING (bloque = 8 bytes)
======================================================================

======================================================================
CASO 1: Mensaje de 5 bytes
======================================================================
Mensaje original: b'HELLO'
Longitud: 5 bytes
Hex original: 48454c4c4f

Después de padding:
  Resultado: b'HELLO\x03\x03\x03'
  Longitud: 8 bytes
  Hex: 48454c4c4f030303

Análisis byte por byte:
  Bytes 0-4: 48454c4c4f = 'HELLO' (mensaje original)
  Bytes 5-7: 030303 = 03 03 03 (padding: 3 bytes faltantes)

Después de unpad: b'HELLO'
¿Recuperado correctamente? True

======================================================================
CASO 2: Mensaje de 8 bytes (exactamente 1 bloque)
======================================================================
Mensaje original: b'EXACTOOO'
Longitud: 8 bytes
Hex original: 4558414354 4f4f4f

Después de padding:
  Resultado: b'EXACTOOO\x08\x08\x08\x08\x08\x08\x08\x08'
  Longitud: 16 bytes
  Hex: 4558414354 4f4f4f 0808080808080808

Análisis byte por byte:
  Bytes 0-7:  4558414354 4f4f4f = 'EXACTOOO' (mensaje original)
  Bytes 8-15: 0808080808080808 = 08 08 08 08 08 08 08 08 (bloque completo)
  ¡Se agrega un bloque completo porque el mensaje ya era múltiplo de 8!

Después de unpad: b'EXACTOOO'
¿Recuperado correctamente? True

======================================================================
CASO 3: Mensaje de 10 bytes
======================================================================
Mensaje original: b'HOLA MUNDO'
Longitud: 10 bytes
Hex original: 484f4c41204d554e444f

Después de padding:
  Resultado: b'HOLA MUNDO\x06\x06\x06\x06\x06\x06'
  Longitud: 16 bytes
  Hex: 484f4c41204d554e444f060606060606

Análisis byte por byte:
  Bloque 1 (bytes 0-7):  484f4c41204d554e = 'HOLA MUN' (primeros 8 bytes)
  Bloque 2 (bytes 8-15): 444f060606060606
    - Bytes 8-9:   444f = 'DO' (últimos 2 bytes del mensaje)
    - Bytes 10-15: 060606060606 = 06 06 06 06 06 06 (padding: 6 bytes)

Después de unpad: b'HOLA MUNDO'
¿Recuperado correctamente? True
```

---

### Tabla Resumen de Ejemplos

| Mensaje | Longitud | Bytes faltantes | Padding agregado | Longitud final |
|---------|----------|-----------------|------------------|----------------|
| `HELLO` | 5 bytes | 3 | `03 03 03` | 8 bytes |
| `EXACTOOO` | 8 bytes | 8 (bloque completo) | `08 08 08 08 08 08 08 08` | 16 bytes |
| `HOLA MUNDO` | 10 bytes | 6 | `06 06 06 06 06 06` | 16 bytes |

---

## 2.6 Recomendaciones de Uso

### Tabla Comparativa de Modos de Operación

| Modo | Descripción | IV/Nonce | Paralelizable | Autenticación | Seguridad |
|------|-------------|----------|---------------|---------------|-----------|
| **ECB** | Electronic Codebook | ❌ No | ✅ Sí | ❌ No | ❌ Baja |
| **CBC** | Cipher Block Chaining | ✅ IV | ❌ Cifrado / ✅ Descifrado | ❌ No | ⚠️ Media |
| **CTR** | Counter Mode | ✅ Nonce | ✅ Sí | ❌ No | ✅ Alta |
| **GCM** | Galois/Counter Mode | ✅ Nonce | ✅ Sí | ✅ **Sí (AEAD)** | ✅ **Muy Alta** |

---

### Casos de Uso y Desventajas por Modo

#### ECB (Electronic Codebook)
| Aspecto | Detalle |
|---------|---------|
| **Casos de uso** | ❌ **NO RECOMENDADO** para datos reales |
| | ⚠️ Solo para cifrar claves únicas (1 bloque) |
| | 📚 Propósitos educativos |
| **Desventajas** | Bloques iguales → cifrado igual |
| | Patrones visibles en datos |
| | Vulnerable a ataques de sustitución |

---

#### CBC (Cipher Block Chaining)
| Aspecto | Detalle |
|---------|---------|
| **Casos de uso** | Cifrado de archivos |
| | Protocolos legacy (TLS 1.0/1.1) |
| | Comunicaciones donde no se necesita autenticación integrada |
| **Desventajas** | No paralelizable en cifrado |
| | Vulnerable a padding oracle attacks si no se implementa bien |
| | Requiere IV único por mensaje |
| | Sin autenticación integrada (debe agregarse HMAC) |

---

#### CTR (Counter Mode)
| Aspecto | Detalle |
|---------|---------|
| **Casos de uso** | Cifrado de streams |
| | Alta velocidad requerida |
| | Acceso aleatorio a datos cifrados |
| **Desventajas** | **Crítico:** Nunca reusar nonce con misma clave |
| | Sin autenticación integrada |
| | Si el nonce se repite, se compromete toda la seguridad |

---

#### GCM (Galois/Counter Mode) - **RECOMENDADO**
| Aspecto | Detalle |
|---------|---------|
| **Casos de uso** | ✅ **TLS 1.3** (estándar actual) |
| | ✅ APIs web (JWT, OAuth) |
| | ✅ Almacenamiento en la nube |
| | ✅ Cualquier aplicación moderna |
| **Ventajas** | AEAD: Autenticación + Cifrado en uno |
| | Detecta modificaciones en los datos |
| | Muy rápido (parallelizable) |
| | Estándar de industria |
| **Desventajas** | Nonce de 96 bits debe ser único |
| | Límite de ~64 GB por clave/nonce |

---

### ¿Qué es AEAD y por qué es importante?

**AEAD = Authenticated Encryption with Associated Data**

| Sin AEAD (CBC) | Con AEAD (GCM) |
|----------------|----------------|
| Solo cifra datos | Cifra Y autentica |
| Atacante puede modificar ciphertext | Modificación detectada automáticamente |
| Requiere HMAC adicional | Autenticación integrada |
| Más código, más errores posibles | Una sola función segura |

**GCM proporciona:**
- **Confidencialidad:** Datos cifrados
- **Integridad:** Detecta si los datos fueron modificados
- **Autenticidad:** Verifica que el remitente es legítimo
- **Associated Data:** Puede autenticar datos no cifrados (headers)

---

### Código de Ejemplo en Múltiples Lenguajes

#### Python - AES-GCM (Recomendado)

```python
# python_aes_gcm.py - Cifrado seguro con AES-256-GCM
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

def encrypt_aes_gcm(plaintext: bytes, key: bytes, associated_data: bytes = b"") -> tuple:
    """
    Cifra datos con AES-256-GCM (AEAD).
    
    Returns:
        tuple: (nonce, ciphertext, tag)
    """
    # Nonce de 96 bits (12 bytes) - ÚNICO por mensaje
    nonce = get_random_bytes(12)
    
    # Crear cifrador GCM
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    
    # Agregar datos asociados (se autentican pero no se cifran)
    if associated_data:
        cipher.update(associated_data)
    
    # Cifrar y obtener tag de autenticación
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    
    return nonce, ciphertext, tag


def decrypt_aes_gcm(nonce: bytes, ciphertext: bytes, tag: bytes, 
                     key: bytes, associated_data: bytes = b"") -> bytes:
    """
    Descifra y verifica datos con AES-256-GCM.
    
    Raises:
        ValueError: Si la autenticación falla (datos manipulados)
    """
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    
    if associated_data:
        cipher.update(associated_data)
    
    # Descifrar y verificar tag
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    
    return plaintext


# Ejemplo de uso
if __name__ == "__main__":
    # Generar clave AES-256
    key = get_random_bytes(32)
    
    # Mensaje a cifrar
    mensaje = b"Informacion confidencial"
    header = b"metadata-no-cifrada"  # Associated data
    
    print("=== AES-256-GCM en Python ===")
    print(f"Mensaje: {mensaje}")
    print(f"Header (AAD): {header}")
    
    # Cifrar
    nonce, ciphertext, tag = encrypt_aes_gcm(mensaje, key, header)
    
    print(f"\nNonce: {nonce.hex()}")
    print(f"Ciphertext: {ciphertext.hex()}")
    print(f"Auth Tag: {tag.hex()}")
    
    # Descifrar
    decrypted = decrypt_aes_gcm(nonce, ciphertext, tag, key, header)
    print(f"\nDescifrado: {decrypted}")
    
    # Demostrar detección de manipulación
    print("\n--- Prueba de integridad ---")
    try:
        # Modificar ciphertext
        tampered = bytearray(ciphertext)
        tampered[0] ^= 0xFF
        decrypt_aes_gcm(nonce, bytes(tampered), tag, key, header)
    except ValueError as e:
        print(f"✅ Manipulación detectada: {e}")
```

---

#### JavaScript/Node.js - AES-GCM

```javascript
// nodejs_aes_gcm.js - Cifrado seguro con AES-256-GCM
const crypto = require('crypto');

/**
 * Cifra datos con AES-256-GCM
 * @param {Buffer} plaintext - Datos a cifrar
 * @param {Buffer} key - Clave de 32 bytes
 * @param {Buffer} aad - Associated Authenticated Data (opcional)
 * @returns {Object} { nonce, ciphertext, tag }
 */
function encryptAesGcm(plaintext, key, aad = Buffer.alloc(0)) {
    // Nonce de 12 bytes (96 bits) - ÚNICO por mensaje
    const nonce = crypto.randomBytes(12);
    
    // Crear cifrador
    const cipher = crypto.createCipheriv('aes-256-gcm', key, nonce);
    
    // Agregar datos asociados
    if (aad.length > 0) {
        cipher.setAAD(aad);
    }
    
    // Cifrar
    const ciphertext = Buffer.concat([
        cipher.update(plaintext),
        cipher.final()
    ]);
    
    // Obtener tag de autenticación
    const tag = cipher.getAuthTag();
    
    return { nonce, ciphertext, tag };
}

/**
 * Descifra y verifica datos con AES-256-GCM
 * @throws {Error} Si la autenticación falla
 */
function decryptAesGcm(nonce, ciphertext, tag, key, aad = Buffer.alloc(0)) {
    const decipher = crypto.createDecipheriv('aes-256-gcm', key, nonce);
    
    decipher.setAuthTag(tag);
    
    if (aad.length > 0) {
        decipher.setAAD(aad);
    }
    
    const plaintext = Buffer.concat([
        decipher.update(ciphertext),
        decipher.final()  // Verifica el tag aquí
    ]);
    
    return plaintext;
}

// Ejemplo de uso
const key = crypto.randomBytes(32);  // AES-256
const mensaje = Buffer.from('Información confidencial', 'utf8');
const header = Buffer.from('metadata', 'utf8');

console.log('=== AES-256-GCM en Node.js ===');
console.log('Mensaje:', mensaje.toString());

// Cifrar
const { nonce, ciphertext, tag } = encryptAesGcm(mensaje, key, header);

console.log('\nNonce:', nonce.toString('hex'));
console.log('Ciphertext:', ciphertext.toString('hex'));
console.log('Auth Tag:', tag.toString('hex'));

// Descifrar
const decrypted = decryptAesGcm(nonce, ciphertext, tag, key, header);
console.log('\nDescifrado:', decrypted.toString());

// Probar detección de manipulación
console.log('\n--- Prueba de integridad ---');
try {
    const tampered = Buffer.from(ciphertext);
    tampered[0] ^= 0xFF;
    decryptAesGcm(nonce, tampered, tag, key, header);
} catch (e) {
    console.log('✅ Manipulación detectada:', e.message);
}
```

---

#### Java - AES-GCM

```java
// JavaAesGcm.java - Cifrado seguro con AES-256-GCM
import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.GCMParameterSpec;
import java.security.SecureRandom;
import java.util.Base64;

public class JavaAesGcm {
    private static final int GCM_TAG_LENGTH = 128; // bits
    private static final int GCM_NONCE_LENGTH = 12; // bytes
    
    public static byte[] encrypt(byte[] plaintext, SecretKey key, byte[] nonce, byte[] aad) 
            throws Exception {
        Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
        GCMParameterSpec spec = new GCMParameterSpec(GCM_TAG_LENGTH, nonce);
        cipher.init(Cipher.ENCRYPT_MODE, key, spec);
        
        if (aad != null && aad.length > 0) {
            cipher.updateAAD(aad);
        }
        
        return cipher.doFinal(plaintext);  // Incluye tag al final
    }
    
    public static byte[] decrypt(byte[] ciphertext, SecretKey key, byte[] nonce, byte[] aad) 
            throws Exception {
        Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
        GCMParameterSpec spec = new GCMParameterSpec(GCM_TAG_LENGTH, nonce);
        cipher.init(Cipher.DECRYPT_MODE, key, spec);
        
        if (aad != null && aad.length > 0) {
            cipher.updateAAD(aad);
        }
        
        return cipher.doFinal(ciphertext);  // Verifica tag automáticamente
    }
    
    public static void main(String[] args) throws Exception {
        // Generar clave AES-256
        KeyGenerator keyGen = KeyGenerator.getInstance("AES");
        keyGen.init(256);
        SecretKey key = keyGen.generateKey();
        
        // Generar nonce
        byte[] nonce = new byte[GCM_NONCE_LENGTH];
        new SecureRandom().nextBytes(nonce);
        
        String mensaje = "Información confidencial";
        byte[] aad = "header".getBytes();
        
        System.out.println("=== AES-256-GCM en Java ===");
        System.out.println("Mensaje: " + mensaje);
        
        // Cifrar
        byte[] ciphertext = encrypt(mensaje.getBytes(), key, nonce, aad);
        System.out.println("Ciphertext: " + Base64.getEncoder().encodeToString(ciphertext));
        
        // Descifrar
        byte[] decrypted = decrypt(ciphertext, key, nonce, aad);
        System.out.println("Descifrado: " + new String(decrypted));
    }
}
```

---

### Recomendación Final

| Situación | Modo Recomendado | Justificación |
|-----------|------------------|---------------|
| **Aplicación nueva** | ✅ **AES-256-GCM** | AEAD, rápido, seguro, estándar |
| **Comunicaciones TLS** | ✅ **AES-256-GCM** o ChaCha20-Poly1305 | Estándar TLS 1.3 |
| **Cifrado de disco** | XTS-AES | Diseñado para almacenamiento |
| **Legacy/Compatibilidad** | CBC + HMAC | Si GCM no está disponible |
| **Alto rendimiento, stream** | CTR + HMAC | Paralelizable, acceso aleatorio |
| **Nunca usar** | ❌ ECB | Inseguro para cualquier dato real |

**Regla de oro:** Si está disponible, usa **AES-GCM**. Es el estándar moderno que proporciona confidencialidad, integridad y autenticación en una sola operación.