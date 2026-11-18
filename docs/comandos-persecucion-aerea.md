# Comandos de la persecución aérea

Prototipo v1.0 build **20261118-145200**, 18 de noviembre de 2026. Funciona con **Goku y Vegeta controlados por un jugador, a velocidad normal**. Las ROM anteriores a la persecución no incluyen ↑ + C tras lanzar. No hay todavía un comando equivalente anunciado para los otros nueve personajes o para turbo.

Todas las flechas de esta tabla suponen que miras **a la derecha**. Invierte izquierda/derecha al mirar al otro lado; tras el lanzamiento comprueba hacia dónde mira tu personaje.

| Paso o ataque | Entrada | Condición |
| --- | --- | --- |
| Agarrar y lanzar | → + A, muy cerca | Agarre original. |
| Perseguir al lanzado | ↑ + C | Al finalizar TU lanzamiento, con el rival aún en el aire; cuesta 16 de ki. |
| Primer golpe aéreo | A | Cuando alcanzas al rival; puedes orientar el movimiento hacia él. |
| Segundo golpe aéreo | B después de conectar A | Son dos pulsaciones separadas, no A+B a la vez. Como máximo dos básicos en esta fase. |
| Goku: Kamehameha | ← ↙ ↓ ↘ → + A | Introducir durante el enlace tras el básico. |
| Goku: Super Kamehameha | ← ↙ ↓ ↘ →, ← ↙ ↓ ↘ → + A | Mantiene el doble medio círculo elegido por Alex. |
| Goku: Meteor | ← ↙ ↓ ↘ →, ← ↙ ↓ ↘ → + A+B | Introducir tras el básico durante la caída; la ROM conserva el comando hasta aterrizar. |
| Vegeta: Final Flash | ↓ ↙ ← → + A | Comando que ya conserva Vegeta; no se ha convertido al esquema de Goku. |
| Vegeta: Meteor | → ↘ ↓ ↙ ← → + B | Comando original y requisitos nativos, incluida vida baja. Pruebas grabadas con 42 HP y ki cargado. |
| Cambio de lado anterior | → ← → + C | Cerca del rival. Es independiente de ↑ + C tras lanzar. |

El Meteor se inicia **al llegar al suelo** y conserva su secuencia original. No se ejecuta solo: debes introducir su comando. Una persecución por cadena, sin repetir automáticamente al mantener A. La comodidad con mando, la amplitud de los buffers y el equilibrio siguen pendientes de validar. En las pruebas finales de Final Flash se usan tres fotogramas por dirección: una entrada más extrema de dos fotogramas falló en un caso de P2.

[Vídeo de Meteor, cambios y pruebas](air-pursuit-meteor.md).
