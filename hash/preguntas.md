# Respuestas

## 1. Cambios entre los dos hashes SHA-256

Los dos valores SHA-256 obtenidos fueron:

- `MediSoft-v2.1.0` -> `64942401fe64ac1182bd88326ba7ca57a23ea5d0475653dea996ac15e8e74996`
- `medisoft-v2.1.0` -> `ec8d163da33b9832c33fbb2d7cba98f5a7087aa6cbdecc04eb32810b1f1f895e`

Al aplicar `XOR` entre ambos hashes y contar los bits en `1`, cambiaron **120 bits de 256**, es decir, **46.875 %** del hash.

Esto demuestra la propiedad de **efecto avalancha**: un cambio minimo en la entrada, como cambiar una letra mayuscula por minuscula, produce un cambio grande y aparentemente aleatorio en el hash resultante.

## 2. Por que MD5 es inseguro para integridad de archivos

MD5 genera un hash de **128 bits**. Eso significa que su espacio de salida es mas pequeno que el de algoritmos modernos como SHA-256, que produce **256 bits**.

Para integridad de archivos, lo importante es la **resistencia a colisiones**: que sea muy dificil encontrar dos archivos distintos con el mismo hash. En un hash ideal de 128 bits, la dificultad teorica de colision es aproximadamente `2^64` intentos por la paradoja del cumpleanos, que hoy es insuficiente para considerarlo seguro frente a ataques modernos.

Ademas, MD5 no solo es corto, sino que tambien esta **criptograficamente roto**: existen colisiones practicas conocidas. Por eso, un atacante podria fabricar dos archivos diferentes con el mismo MD5, haciendo que ya no sea confiable para verificar integridad.
