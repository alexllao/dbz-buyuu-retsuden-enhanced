# Namek: prueba de árbol en primer plano

[Ver 23 segundos de actual y propuesta](../assets/media/namek-foreground/Namek-arbol-prueba-en-movimiento-v1.mp4).

El usuario quiere un detalle cercano a la cámara, como la palmera de Street Fighter, aplicado a Namek. Se propone un árbol namekiano con tronco estrecho y copa azul, que entra y sale del encuadre al desplazarse la cámara.

![Árbol durante el desplazamiento](../assets/concepts/namek-foreground/Namek-arbol-scroll-captura-v1.png)

**Estado: maqueta visual, pendiente de validar. El árbol no está integrado en la ROM.** Las dos pasadas usan la misma grabación de HUD HITS v3: paseo, básicos y cambio de lado, con sonido original y sin acelerar. En la segunda se superpone el árbol transparente generado con la herramienta de imágenes. El scroll se sigue por comparación de los píxeles del fondo y se amplifica 1,15 veces para simular un plano más cercano. No se ha probado todavía un nuevo plano nativo ni su coste gráfico.

El HUD permanece despejado. La prueba es de suelo: no valida vuelo, movimiento de copa, sombras, colisiones nuevas ni funcionamiento en consola original. La selección de paletas de Namek continúa pendiente y no se cambia con esta prueba.

[Comparación estática anterior](../assets/concepts/namek-foreground/Namek-arbol-antes-despues-v1.png) · [Prompt del árbol](../research/namek-foreground/prompt-arbol-transparente-v1.txt) · [Registro del montaje](../evidence/namek-foreground/manifest.json).
