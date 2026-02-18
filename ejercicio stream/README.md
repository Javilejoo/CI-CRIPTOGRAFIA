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


