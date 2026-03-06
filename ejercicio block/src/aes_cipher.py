"""
aes_cipher.py - Implementacion de AES-256 con modos ECB y CBC.

AES-256:
- Tamano de bloque: 128 bits (16 bytes)
- Tamano de clave: 256 bits (32 bytes)
- 14 rondas de cifrado

Modos de operacion:
- ECB (Electronic Codebook): Cada bloque se cifra independientemente
  - NO usa IV
  - Patrones repetidos en el plaintext producen patrones en el ciphertext
  
- CBC (Cipher Block Chaining): Cada bloque depende del anterior
  - Usa IV de 128 bits (unico por mensaje)
  - El IV se transmite junto con el ciphertext
  - Mas seguro que ECB

Padding: Utiliza Crypto.Util.Padding (PKCS#7)

Cifrado de imagenes:
- Se mantiene el header intacto (54 bytes para BMP-like structure)
- Solo se cifran los datos de pixeles
- Permite comparar visualmente ECB vs CBC
"""
import os
import sys

# Configurar path para imports
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

EJERCICIO_BLOCK_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if EJERCICIO_BLOCK_DIR not in sys.path:
    sys.path.insert(0, EJERCICIO_BLOCK_DIR)

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from PIL import Image
import io


# --- CONSTANTES ---
AES_BLOCK_SIZE = 16  # 128 bits
AES_KEY_SIZE = 32    # 256 bits
IMAGE_HEADER_SIZE = 54  # Tamano tipico de header BMP (puede variar para PNG)


# --- FUNCIONES DE GENERACION DE CLAVES E IV ---

def generate_aes_key():
    """Genera una clave AES-256 aleatoria (32 bytes)."""
    return os.urandom(AES_KEY_SIZE)


def generate_iv():
    """Genera un IV aleatorio de 128 bits para modo CBC."""
    return os.urandom(AES_BLOCK_SIZE)


# --- FUNCIONES AES ECB ---

def aes_ecb_encrypt(plaintext: bytes, key: bytes) -> bytes:
    """
    Cifra datos usando AES-256 en modo ECB.
    
    Args:
        plaintext: Datos a cifrar (bytes)
        key: Clave de 32 bytes
        
    Returns:
        bytes: Datos cifrados
    """
    # Aplicar padding PKCS#7
    padded_data = pad(plaintext, AES_BLOCK_SIZE, style='pkcs7')
    
    # Crear cifrador AES en modo ECB
    cipher = AES.new(key, AES.MODE_ECB)
    
    # Cifrar
    ciphertext = cipher.encrypt(padded_data)
    
    return ciphertext


def aes_ecb_decrypt(ciphertext: bytes, key: bytes) -> bytes:
    """
    Descifra datos usando AES-256 en modo ECB.
    
    Args:
        ciphertext: Datos cifrados (bytes)
        key: Clave de 32 bytes
        
    Returns:
        bytes: Datos descifrados sin padding
    """
    # Crear cifrador AES en modo ECB
    cipher = AES.new(key, AES.MODE_ECB)
    
    # Descifrar
    padded_data = cipher.decrypt(ciphertext)
    
    # Quitar padding
    plaintext = unpad(padded_data, AES_BLOCK_SIZE, style='pkcs7')
    
    return plaintext


# --- FUNCIONES AES CBC ---

def aes_cbc_encrypt(plaintext: bytes, key: bytes, iv: bytes = None) -> tuple:
    """
    Cifra datos usando AES-256 en modo CBC.
    
    Args:
        plaintext: Datos a cifrar (bytes)
        key: Clave de 32 bytes
        iv: IV de 16 bytes (si None, se genera automaticamente)
        
    Returns:
        tuple: (ciphertext, iv)
    """
    # Generar IV si no se proporciona
    if iv is None:
        iv = generate_iv()
    
    # Aplicar padding PKCS#7
    padded_data = pad(plaintext, AES_BLOCK_SIZE, style='pkcs7')
    
    # Crear cifrador AES en modo CBC
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Cifrar
    ciphertext = cipher.encrypt(padded_data)
    
    return ciphertext, iv


def aes_cbc_decrypt(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    """
    Descifra datos usando AES-256 en modo CBC.
    
    Args:
        ciphertext: Datos cifrados (bytes)
        key: Clave de 32 bytes
        iv: IV de 16 bytes
        
    Returns:
        bytes: Datos descifrados sin padding
    """
    # Crear cifrador AES en modo CBC
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Descifrar
    padded_data = cipher.decrypt(ciphertext)
    
    # Quitar padding
    plaintext = unpad(padded_data, AES_BLOCK_SIZE, style='pkcs7')
    
    return plaintext


# --- FUNCIONES PARA EMPAQUETAR IV CON CIPHERTEXT ---

def pack_ciphertext_with_iv(ciphertext: bytes, iv: bytes) -> bytes:
    """
    Empaqueta el IV junto con el ciphertext para transmision.
    Formato: IV (16 bytes) + Ciphertext
    
    Args:
        ciphertext: Texto cifrado
        iv: IV de 16 bytes
        
    Returns:
        bytes: IV + Ciphertext
    """
    return iv + ciphertext


def unpack_ciphertext_with_iv(packed_data: bytes) -> tuple:
    """
    Desempaqueta el IV y el ciphertext.
    
    Args:
        packed_data: IV (16 bytes) + Ciphertext
        
    Returns:
        tuple: (ciphertext, iv)
    """
    iv = packed_data[:AES_BLOCK_SIZE]
    ciphertext = packed_data[AES_BLOCK_SIZE:]
    return ciphertext, iv


# --- FUNCIONES DE CIFRADO DE IMAGENES ---

def convert_to_bmp(input_path: str, output_path: str = None):
    """
    Convierte una imagen a formato BMP (sin compresion, 24-bit).
    
    Args:
        input_path: Ruta de la imagen original
        output_path: Ruta para guardar BMP (si None, retorna bytes)
        
    Returns:
        bytes o str: Datos BMP o ruta del archivo guardado
    """
    img = Image.open(input_path)
    # Convertir a RGB si tiene canal alpha
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    
    if output_path:
        img.save(output_path, 'BMP')
        return output_path
    else:
        # Retornar bytes
        buffer = io.BytesIO()
        img.save(buffer, 'BMP')
        return buffer.getvalue()


def get_bmp_header_size(bmp_data: bytes) -> int:
    """
    Obtiene el offset a los datos de pixeles desde el header BMP.
    El offset esta en los bytes 10-13 (little-endian).
    """
    return int.from_bytes(bmp_data[10:14], 'little')


def encrypt_image_ecb(input_path: str, output_path: str, key: bytes):
    """
    Cifra una imagen usando AES-256 ECB manteniendo el header BMP intacto.
    Convierte automaticamente PNG/otros formatos a BMP.
    
    Args:
        input_path: Ruta de la imagen original
        output_path: Ruta para guardar la imagen cifrada (.bmp)
        key: Clave AES-256 de 32 bytes
    """
    # Convertir a BMP primero
    bmp_data = convert_to_bmp(input_path)
    
    # Obtener el offset real del header BMP
    header_size = get_bmp_header_size(bmp_data)
    
    # Separar header y datos de pixeles
    header = bmp_data[:header_size]
    pixel_data = bmp_data[header_size:]
    
    print(f"Imagen original: {len(bmp_data)} bytes")
    print(f"Header BMP: {header_size} bytes (preservado)")
    print(f"Datos de pixeles: {len(pixel_data)} bytes")
    
    # Cifrar los datos de pixeles bloque por bloque
    cipher = AES.new(key, AES.MODE_ECB)
    
    # Cifrar en bloques de 16 bytes, mantener tamano original
    encrypted_pixels = bytearray()
    for i in range(0, len(pixel_data), AES_BLOCK_SIZE):
        block = pixel_data[i:i+AES_BLOCK_SIZE]
        if len(block) < AES_BLOCK_SIZE:
            # Ultimo bloque incompleto - padding temporal
            block = block + bytes(AES_BLOCK_SIZE - len(block))
            encrypted_block = cipher.encrypt(block)
            # Truncar al tamano original del bloque
            encrypted_pixels.extend(encrypted_block[:len(pixel_data) - i])
        else:
            encrypted_block = cipher.encrypt(block)
            encrypted_pixels.extend(encrypted_block)
    
    # Combinar header + pixeles cifrados
    encrypted_image = header + bytes(encrypted_pixels)
    
    with open(output_path, 'wb') as f:
        f.write(encrypted_image)
    
    print(f"Imagen cifrada (ECB) guardada en: {output_path}")
    return encrypted_image


def encrypt_image_cbc(input_path: str, output_path: str, key: bytes, iv: bytes = None):
    """
    Cifra una imagen usando AES-256 CBC manteniendo el header BMP intacto.
    Convierte automaticamente PNG/otros formatos a BMP.
    
    Args:
        input_path: Ruta de la imagen original
        output_path: Ruta para guardar la imagen cifrada (.bmp)
        key: Clave AES-256 de 32 bytes
        iv: IV de 16 bytes (si None, se genera)
        
    Returns:
        tuple: (encrypted_image, iv)
    """
    if iv is None:
        iv = generate_iv()
    
    # Convertir a BMP primero
    bmp_data = convert_to_bmp(input_path)
    
    # Obtener el offset real del header BMP
    header_size = get_bmp_header_size(bmp_data)
    
    # Separar header y datos de pixeles
    header = bmp_data[:header_size]
    pixel_data = bmp_data[header_size:]
    
    print(f"Imagen original: {len(bmp_data)} bytes")
    print(f"Header BMP: {header_size} bytes (preservado)")
    print(f"Datos de pixeles: {len(pixel_data)} bytes")
    print(f"IV: {iv.hex()}")
    
    # Cifrar los datos de pixeles
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Cifrar en bloques, mantener tamano original
    encrypted_pixels = bytearray()
    prev_block = iv
    
    for i in range(0, len(pixel_data), AES_BLOCK_SIZE):
        block = pixel_data[i:i+AES_BLOCK_SIZE]
        if len(block) < AES_BLOCK_SIZE:
            # Ultimo bloque incompleto - padding temporal
            block = block + bytes(AES_BLOCK_SIZE - len(block))
            encrypted_block = cipher.encrypt(block)
            encrypted_pixels.extend(encrypted_block[:len(pixel_data) - i])
        else:
            encrypted_block = cipher.encrypt(block)
            encrypted_pixels.extend(encrypted_block)
    
    # Combinar header + pixeles cifrados
    encrypted_image = header + bytes(encrypted_pixels)
    
    with open(output_path, 'wb') as f:
        f.write(encrypted_image)
    
    print(f"Imagen cifrada (CBC) guardada en: {output_path}")
    return encrypted_image, iv


def decrypt_image(input_path: str, output_path: str, key: bytes, mode: str, iv: bytes = None):
    """
    Descifra una imagen BMP cifrada con AES.
    
    Args:
        input_path: Ruta de la imagen cifrada (.bmp)
        output_path: Ruta para guardar la imagen descifrada
        key: Clave AES-256 de 32 bytes
        mode: 'ecb' o 'cbc'
        iv: IV de 16 bytes (requerido solo para CBC)
    """
    with open(input_path, 'rb') as f:
        image_data = f.read()
    
    # Obtener el offset real del header BMP
    header_size = get_bmp_header_size(image_data)
    
    header = image_data[:header_size]
    encrypted_pixels = image_data[header_size:]
    
    if mode.lower() == 'ecb':
        cipher = AES.new(key, AES.MODE_ECB)
    else:
        cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Descifrar en bloques
    decrypted_pixels = bytearray()
    for i in range(0, len(encrypted_pixels), AES_BLOCK_SIZE):
        block = encrypted_pixels[i:i+AES_BLOCK_SIZE]
        if len(block) < AES_BLOCK_SIZE:
            block = block + bytes(AES_BLOCK_SIZE - len(block))
            decrypted_block = cipher.decrypt(block)
            decrypted_pixels.extend(decrypted_block[:len(encrypted_pixels) - i])
        else:
            decrypted_block = cipher.decrypt(block)
            decrypted_pixels.extend(decrypted_block)
    
    decrypted_image = header + bytes(decrypted_pixels)
    
    with open(output_path, 'wb') as f:
        f.write(decrypted_image)
    
    print(f"Imagen descifrada guardada en: {output_path}")
    return decrypted_image


# --- MAIN ---

if __name__ == "__main__":
    print("=" * 70)
    print("AES-256 - CIFRADO DE TEXTO Y IMAGENES")
    print("=" * 70)
    
    # Generar clave AES-256
    key = generate_aes_key()
    print(f"\nClave AES-256 (hex): {key.hex()}")
    print(f"Tamano de clave: {len(key)} bytes ({len(key)*8} bits)")
    
    # --- PRUEBA CON TEXTO ---
    print(f"\n{'='*70}")
    print("PRUEBA DE CIFRADO DE TEXTO")
    print("=" * 70)
    
    mensaje = b"Mensaje de prueba para AES-256 en modos ECB y CBC!"
    print(f"Mensaje original: {mensaje}")
    print(f"Tamano: {len(mensaje)} bytes")
    
    # ECB
    print(f"\n--- Modo ECB ---")
    ciphertext_ecb = aes_ecb_encrypt(mensaje, key)
    print(f"Ciphertext (hex): {ciphertext_ecb.hex()}")
    print(f"Tamano cifrado: {len(ciphertext_ecb)} bytes")
    
    decrypted_ecb = aes_ecb_decrypt(ciphertext_ecb, key)
    print(f"Descifrado: {decrypted_ecb}")
    print(f"Verificacion: {'OK' if decrypted_ecb == mensaje else 'FALLO'}")
    
    # CBC
    print(f"\n--- Modo CBC ---")
    ciphertext_cbc, iv = aes_cbc_encrypt(mensaje, key)
    print(f"IV (hex): {iv.hex()}")
    print(f"Ciphertext (hex): {ciphertext_cbc.hex()}")
    print(f"Tamano cifrado: {len(ciphertext_cbc)} bytes")
    
    # Empaquetar para transmision
    packed = pack_ciphertext_with_iv(ciphertext_cbc, iv)
    print(f"\nDatos empaquetados para transmision: {len(packed)} bytes")
    print(f"  - IV: 16 bytes")
    print(f"  - Ciphertext: {len(ciphertext_cbc)} bytes")
    
    # Desempaquetar (simular receptor)
    received_ciphertext, received_iv = unpack_ciphertext_with_iv(packed)
    decrypted_cbc = aes_cbc_decrypt(received_ciphertext, key, received_iv)
    print(f"Descifrado: {decrypted_cbc}")
    print(f"Verificacion: {'OK' if decrypted_cbc == mensaje else 'FALLO'}")
    
    # --- CIFRADO DE IMAGEN ---
    print(f"\n{'='*70}")
    print("CIFRADO DE IMAGEN (ECB vs CBC)")
    print("=" * 70)
    
    # Rutas de imagenes
    images_dir = os.path.join(os.path.dirname(__file__), '..', 'images')
    input_image = os.path.join(images_dir, 'pic.png')
    output_ecb = os.path.join(images_dir, 'aes_ecb.bmp')
    output_cbc = os.path.join(images_dir, 'aes_cbc.bmp')
    
    if os.path.exists(input_image):
        print(f"\nImagen de entrada: {input_image}")
        print("(Se convierte automaticamente a BMP para visualizar patrones)")
        
        print(f"\n--- Cifrando con ECB ---")
        encrypt_image_ecb(input_image, output_ecb, key)
        
        print(f"\n--- Cifrando con CBC ---")
        encrypted_cbc, iv_img = encrypt_image_cbc(input_image, output_cbc, key)
        
        print(f"\n{'='*70}")
        print("COMPARACION ECB vs CBC")
        print("=" * 70)
        print("ECB: Patrones repetidos en la imagen original producen patrones visibles")
        print("     en la imagen cifrada (NO recomendado para datos con patrones)")
        print("CBC: Los patrones se difuminan debido al encadenamiento con IV")
        print("     (MAS seguro para la mayoria de aplicaciones)")
        print(f"\nImagenes generadas:")
        print(f"  - ECB: {output_ecb}")
        print(f"  - CBC: {output_cbc}")
    else:
        print(f"\nImagen no encontrada: {input_image}")
        print("Saltando cifrado de imagen...")
    
    print(f"\n{'='*70}")
    print("RESUMEN")
    print("=" * 70)
    print(f"Algoritmo: AES-256")
    print(f"Tamano de bloque: {AES_BLOCK_SIZE} bytes ({AES_BLOCK_SIZE*8} bits)")
    print(f"Tamano de clave: {AES_KEY_SIZE} bytes ({AES_KEY_SIZE*8} bits)")
    print(f"Modos implementados: ECB, CBC")
