import Juego
from Juego import Juego

juego = Juego()
juego.crear_juego()
while not juego.juego_terminado():
     juego.jugar_ronda()