"""
Pruebas Unitarias para Stream Cipher XOR

Este módulo contiene 4 pruebas unitarias que validan:
1. El descifrado recupera exactamente el mensaje original
2. Diferentes claves producen diferentes textos cifrados
3. La misma clave produce el mismo texto cifrado (determinismo)
4. El cifrado maneja correctamente mensajes de diferentes longitudes
"""

import unittest
import sys
import os

# Importar funciones del archivo keystream.py
sys.path.insert(0, os.path.dirname(__file__))
from keystream import cifrar, descifrar


class PruebasStreamCipherXOR(unittest.TestCase):
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.mensaje_base = "mensaje de prueba"
        self.clave_base = "clave_secreta"
        self.nonce_base = "2026-02-17"
    
    def test_1_descifrado_recupera_mensaje_original(self):
        """
        PRUEBA 1: El descifrado recupera exactamente el mensaje original
        """
        mensaje_original = "Hola Mundo"
        clave = "mi_clave"
        nonce = "nonce_test"
        
        # Cifrar
        cifrado = cifrar(mensaje_original, clave, nonce)
        
        # Descifrar
        descifrado = descifrar(cifrado, clave, nonce)
        
        # Validación
        self.assertEqual(descifrado, mensaje_original, 
                        f"El descifrado '{descifrado}' no coincide con el original '{mensaje_original}'")
        print("✓ PRUEBA 1 EXITOSA: Descifrado = Original")
    
    def test_2_diferentes_claves_generan_diferentes_cifrados(self):
        """
        PRUEBA 2: Diferentes claves producen diferentes textos cifrados
        
        Se cifra el mismo mensaje con dos claves diferentes y se verifica que
        los resultados sean distintos.
        """
        mensaje = "test"
        clave1 = "clave_uno"
        clave2 = "clave_dos"
        nonce = "nonce_test"
        
        # Cifrar con clave 1
        cifrado1 = cifrar(mensaje, clave1, nonce)
        
        # Cifrar con clave 2
        cifrado2 = cifrar(mensaje, clave2, nonce)
        
        # Validación: deben ser diferentes
        self.assertNotEqual(cifrado1, cifrado2,
                           f"Clave diferente debería producir cifrado diferente")
        print("✓ PRUEBA 2 EXITOSA: Claves diferentes → Cifrados diferentes")
    
    def test_3_misma_clave_produce_mismo_cifrado_determinismo(self):
        """
        PRUEBA 3: La misma clave produce el mismo texto cifrado (determinismo)
        
        Se cifra el mismo mensaje con la misma clave y nonce tres veces,
        verificando que los resultados sean idénticos cada vez.
        """
        mensaje = "determinismo"
        clave = "clave_fija"
        nonce = "nonce_fija"
        
        # Cifrar 3 veces
        cifrado1 = cifrar(mensaje, clave, nonce)
        cifrado2 = cifrar(mensaje, clave, nonce)
        cifrado3 = cifrar(mensaje, clave, nonce)
        
        # Validación: todos deben ser iguales
        self.assertEqual(cifrado1, cifrado2,
                        "Cifrado 1 y 2 deberían ser idénticos")
        self.assertEqual(cifrado2, cifrado3,
                        "Cifrado 2 y 3 deberían ser idénticos")
        self.assertEqual(cifrado1, cifrado3,
                        "Cifrado 1 y 3 deberían ser idénticos")
        print("✓ PRUEBA 3 EXITOSA: Determinismo validado (3 ejecuciones iguales)")
    
    def test_4_maneja_diferentes_longitudes_de_mensaje(self):
        """
        PRUEBA 4: El cifrado maneja correctamente mensajes de diferentes longitudes
        
        Se prueban mensajes de diferente longitud (1, 50, 100, 500 caracteres)
        verificando que se cifren, descifren correctamente y se recupere el original.
        """
        clave = "clave_test"
        nonce = "nonce_test"
        
        # Lista de longitudes a probar
        longitudes = [
            ("a", 1),                           # 1 carácter
            ("a" * 50, 50),                     # 50 caracteres
            ("Mensaje largo " * 7, 100),        # ~100 caracteres
            ("Lorem ipsum dolor sit amet " * 20, 500)  # ~500 caracteres
        ]
        
        resultados = []
        
        for mensaje, longitud in longitudes:
            # Cifrar
            cifrado = cifrar(mensaje, clave, nonce)
            
            # Descifrar
            descifrado = descifrar(cifrado, clave, nonce)
            
            # Validar que coincida exactamente
            self.assertEqual(descifrado, mensaje,
                           f"Mensaje de {longitud} caracteres no se recuperó correctamente")
            
            resultados.append(f"  - {longitud} caracteres: OK")
        
        print("✓ PRUEBA 4 EXITOSA: Diferentes longitudes maneadas correctamente")
        for resultado in resultados:
            print(resultado)


def run_tests():
    """Ejecuta todas las pruebas"""
    print("\n" + "=" * 70)
    print("PRUEBAS UNITARIAS - STREAM CIPHER XOR")
    print("=" * 70 + "\n")
    
    # Crear suite de pruebas
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(PruebasStreamCipherXOR)
    
    # Ejecutar pruebas
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resumen final
    print("\n" + "=" * 70)
    print("RESUMEN DE RESULTADOS")
    print("=" * 70)
    print(f"Pruebas ejecutadas: {result.testsRun}")
    print(f"Pruebas exitosas: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Pruebas fallidas: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    print("=" * 70 + "\n")
    
    if result.wasSuccessful():
        print("✓ TODAS LAS PRUEBAS PASARON CORRECTAMENTE\n")
    else:
        print("✗ ALGUNAS PRUEBAS FALLARON\n")


if __name__ == "__main__":
    run_tests()
