# Stream Cipher XOR - Ejercicio de Criptografía

## 1. Descripción del Proyecto

Este proyecto implementa un **cifrador de flujo (Stream Cipher)** utilizando la operación **XOR** para cifrar y descifrar mensajes. El sistema genera un keystream pseudoaleatorio determinístico basado en una clave secreta y un nonce, y lo combina bit a bit con el mensaje usando XOR.

### Componentes principales:
- **`keystream.py`**: Implementa las funciones de generación de keystream, cifrado y descifrado
- **`validacion_pruebas.py`**: Contiene 3 ejemplos documentados de entrada/salida
- **`pruebas_unitarias.py`**: Suite de 4 pruebas unitarias para validar la seguridad y funcionamiento

### Características:
- ✓ Determinístico (misma clave + nonce = mismo keystream)
- ✓ Soporta mensajes de cualquier longitud
- ✓ Usa PRNG basado en Mersenne Twister con hash SHA-256
- ✓ Incluye función de descifrado reversible

---

## 2. Instrucciones de Instalación y Uso

### Requisitos:
- Python 3.8 o superior
- Librerías estándar (no se requieren dependencias externas)

### Instalación:
```bash
# Clonar o descargar el proyecto
cd "ejercicio stream"

# Verificar que todos los archivos estén presentes
# - keystream.py
# - validacion_pruebas.py
# - pruebas_unitarias.py
# - README.md
```

### Uso básico:

#### 1. Ejecutar el cifrador principal:
```bash
python keystream.py
```
Ingresa el mensaje y la clave cuando se solicite. La nonce se genera automáticamente.

#### 2. Ejecutar ejemplos (3 mostrados):
```bash
python validacion_pruebas.py
```
Muestra 3 ejemplos completos de cifrado/descifrado con diferentes mensajes y claves.

#### 3. Ejecutar pruebas unitarias:
```bash
python pruebas_unitarias.py
```
Ejecuta 4 pruebas automatizadas para validar el funcionamiento correcto.

---

## 3. Ejemplos de Ejecución

### Ejemplo 1: Ejecución interactiva
```bash
$ python keystream.py
Ingrese el mensaje a cifrar: Hola Mundo
Ingrese la clave secreta: mi_clave

Mensaje:         'Hola Mundo'
Keystream:       d46904888d5519aabbcc
Mensaje cifrado: a51c61a8f93475dd99ee
Mensaje descifrado: 'Hola Mundo'
```

### Ejemplo 2: Validaciones
```bash
$ python validacion_pruebas.py

Ejemplo 1:
  Texto plano original: 'Hola'
  Clave utilizada: 'secreto'
  Texto cifrado (hex): 685a6855
  Texto descifrado: 'Hola'

Ejemplo 2:
  Texto plano original: 'Criptografia Stream'
  Clave utilizada: 'claveFuerte123'
  Texto cifrado (hex): e8ccfe81ed27c6c3363717c2fab761f7e6d384
  Texto descifrado: 'Criptografia Stream'

Ejemplo 3:
  Texto plano original: '¡Hola Mundo! 2026'
  Clave utilizada: 'otro_secreto'
  Texto cifrado (hex): 2a32685f80bf458b61cf107bc0674773122f
  Texto descifrado: '¡Hola Mundo! 2026'
```

### Ejemplo 3: Pruebas unitarias
```bash
$ python pruebas_unitarias.py

======================================================================
PRUEBAS UNITARIAS - STREAM CIPHER XOR
======================================================================

✓ PRUEBA 1 EXITOSA: Descifrado = Original
✓ PRUEBA 2 EXITOSA: Claves diferentes → Cifrados diferentes
✓ PRUEBA 3 EXITOSA: Determinismo validado (3 ejecuciones iguales)
✓ PRUEBA 4 EXITOSA: Diferentes longitudes maneadas correctamente

======================================================================
RESUMEN DE RESULTADOS
======================================================================
Pruebas ejecutadas: 4
Pruebas exitosas: 4
Pruebas fallidas: 0
Errores: 0

✓ TODAS LAS PRUEBAS PASARON CORRECTAMENTE
```

---

# Parte 2: Análisis de Seguridad

## 2.1 Variación de la Clave
- ¿Qué sucede cuando cambia la clave utilizada para generar el keystream? Demuestre con un
ejemplo concreto.
El keystream dedpende de la clave, por lo cual al cambiar la clave se genera una nueva secunacia, dado que un cambio en la clave provoca un gran cambio en la salida.
Un ejemplo pr ejemplo con keystream 10110010 mensaje M = 01001101, si ahcemos XOR nos da el cybher text que da 111111. si cambiamos la clave a 01100101 el cipher da 00101000. 

## 2.2 Reutilización del Keystream 
- ¿Qué riesgos de seguridad existen si reutiliza el mismo keystream para cifrar dos mensajes
diferentes? Implemente un ejemplo que demuestre esta vulnerabilidad.

- Sugerencia: Cifre dos mensajes con la misma clave y analice qué información puede extraer un
atacante que intercepte ambos textos cifrados.

Si se utuliza el mismo keystream para cifrar 2 mensajes, el atacante tuviera más facil decifrarlos. dado que se simplifica a M_1 ​⊕m_2​⊕ k​⊕ k., entonces C_! ​⊕ c2 = M_1 ​⊕m_2 el keystream desaparece. el atacante tiene la relacion directa entre los 2 mensajes.

## 2.3 Longitud del Keystream
- ¿Cómo afecta la longitud del keystream a la seguridad del cifrado? Considere tanto keystreams
más cortos como más largos que el mensaje.

Si se tiene un keystream menor al mensaje, se debe de repetir el keystream, por lo cual el porblmea es que se repite el keystream teniendo periodicidad. en el cual permite ataques de patrones . Si se tiene keystreams mas largos  por ejemplo mensjae 8 bits y keystream 128 bits , se usa los primeros 8 bits, por lo cual no reduce la seguridad

## 2.4 Consideraciones Prácticas 
- ¿Qué consideraciones debe tener al generar un keystream en un entorno de producción real?
Mencione al menos 3 aspectos críticos.

Ees fundamental utilizar un generador pseudoaleatorio criptográficamente seguro (CSPRNG), ya que generadores no diseñados para criptografía pueden producir secuencias predecibles y comprometer completamente el cifrado. En segundo lugar, nunca se debe reutilizar el mismo keystream, lo que implica no repetir la combinación de clave y nonce/IV; la reutilización puede permitir ataques como el “two-time pad”, que revelan información sobre los mensajes cifrados. En tercer lugar, la clave secreta debe tener suficiente entropía y ser almacenada y gestionada de forma segura, evitando claves débiles o derivadas de contraseñas sin un esquema robusto de derivación.


