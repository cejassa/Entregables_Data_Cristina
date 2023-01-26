# HUNDIR LA FLOTA

![image](https://user-images.githubusercontent.com/110189994/213908259-0cbe1f95-e530-45d7-bc57-82c17a10ed6a.png)


Es el primer proyecto que nos lanzaron en The Bridge, tras estar dos semanas introduciéndonos en Python y una de sus librerías más importantes: **Numpy**.

Para su realización se crearon las diferentes clases:
- **Clase Tablero:**
  · Aparecen 4 tableros, 2 para el jugador local y 2 para la IA, es decir, 4 matrices numpy
  · Los tableros quedan impresos con los índices de los números
  
- **Clase Barco:**
  · Los barcos son arrays numpy que toma como referencia el valor mínimo y máximo de la fila, y el mínimo y máximo de la columna
  
- **Clase IA:**
  · La IA busca posición aleatoria dentro del tablero, y si encuentra barco, prueba las diferentes opciones de su alrededor. Si la opción es correcta, continúa disparando en esa dirección hasta que sea agua, y, en ese caso, para el próximo turno disparará en la dirección opuesta hasta hundir el barco.
  
- **Clase Juego:**
  · Contiene los actores que intervienen en el juego y va reproduciendo el guión y el timing.
  
El juego se irá ejecutando iterativamente en un **bucle while** hasta que uno de los dos jugadores se quede sin barco.

¡Te invito a que intentes ganarle la partida a esta IA!

