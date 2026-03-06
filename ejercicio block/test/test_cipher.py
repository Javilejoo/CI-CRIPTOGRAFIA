"""
test_cipher.py - Pruebas de los cifradores DES, 3DES y AES.
Ejecuta cada cifrador y verifica su funcionamiento.
"""
import sys
import os
import subprocess

# Configurar paths
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
EJERCICIO_BLOCK_DIR = os.path.abspath(os.path.join(TEST_DIR, '..'))
SRC_DIR = os.path.join(EJERCICIO_BLOCK_DIR, 'src')

# Obtener el ejecutable de Python del entorno actual
PYTHON_EXE = sys.executable


def run_cipher(script_name: str, description: str):
    """
    Ejecuta un script de cifrado y muestra su salida.
    
    Args:
        script_name: Nombre del archivo .py a ejecutar
        description: Descripcion del cifrador
    """
    script_path = os.path.join(SRC_DIR, script_name)
    
    print(f"\n{'#'*80}")
    print(f"# {description}")
    print(f"# Script: {script_name}")
    print(f"{'#'*80}\n")
    
    if not os.path.exists(script_path):
        print(f"ERROR: No se encontro el archivo {script_path}")
        return False
    
    try:
        # Ejecutar el script y capturar la salida
        result = subprocess.run(
            [PYTHON_EXE, script_path],
            capture_output=True,
            text=True,
            cwd=SRC_DIR,
            timeout=120
        )
        
        # Mostrar stdout
        if result.stdout:
            print(result.stdout)
        
        # Mostrar stderr si hay errores
        if result.stderr:
            print(f"\n--- STDERR ---")
            print(result.stderr)
        
        # Verificar codigo de retorno
        if result.returncode == 0:
            print(f"\n[OK] {script_name} ejecutado correctamente")
            return True
        else:
            print(f"\n[ERROR] {script_name} termino con codigo {result.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"\n[ERROR] {script_name} excedio el tiempo limite de ejecucion")
        return False
    except Exception as e:
        print(f"\n[ERROR] Error al ejecutar {script_name}: {e}")
        return False


def main():
    """Ejecuta todos los cifradores y muestra un resumen."""
    print("="*80)
    print("TEST DE CIFRADORES - DES, 3DES y AES")
    print("="*80)
    print(f"Directorio de tests: {TEST_DIR}")
    print(f"Directorio de src: {SRC_DIR}")
    print(f"Python: {PYTHON_EXE}")
    
    results = {}
    
    # 1. DES Cipher
    results['DES'] = run_cipher(
        'des_cipher.py',
        'DES (Data Encryption Standard) - 64-bit key, 16 rounds'
    )
    
    # 2. Triple DES Cipher
    results['3DES'] = run_cipher(
        'tripledes_cipher.py',
        'Triple DES (3DES-EDE) - 112-bit key, 48 rounds, CBC mode'
    )
    
    # 3. AES Cipher
    results['AES'] = run_cipher(
        'aes_cipher.py',
        'AES-256 - 256-bit key, ECB/CBC modes, Image encryption'
    )
    
    # Resumen final
    print(f"\n{'='*80}")
    print("RESUMEN DE PRUEBAS")
    print("="*80)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for cipher, status in results.items():
        status_str = "[OK]" if status else "[FAIL]"
        print(f"  {status_str} {cipher}")
    
    print(f"\nResultado: {passed}/{total} cifradores ejecutados correctamente")
    
    if passed == total:
        print("\n*** TODAS LAS PRUEBAS PASARON ***")
        return 0
    else:
        print("\n*** ALGUNAS PRUEBAS FALLARON ***")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
