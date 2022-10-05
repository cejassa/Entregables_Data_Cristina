import Tablero
from Tablero import Tablero
import random
from random import choice
import Barco
from Barco import Barco
import numpy as np
import IA
from IA import IA


class Juego:
    filas = 10
    columnas = 10
    longitudes = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
    orientaciones = ['N', 'S', 'E', 'O']

    def __init__(self):
        self.tablero_local_barcos = Tablero(Juego.filas, Juego.columnas)
        self.tablero_local_disparos = Tablero(Juego.filas, Juego.columnas)
        self.tablero_enemigo_barcos = Tablero(Juego.filas, Juego.columnas)
        self.tablero_enemigo_disparos = Tablero(Juego.filas, Juego.columnas)
        self.barcos_jugador_local = [] # Ir metiendo los barcos que creamos nosotros
        self.barcos_maquina = [] # Ir metiendo los barcos que va creando la máquina
        self.turno_jugador = True # Por defecto, para que empiece siempre el jugador
        self.forzar_salir = False # Por defecto, para que hasta que no se dé la condición True no salga del juego
        self.IA = IA()

    def crear_juego(self):
        Juego.mostrar_mensaje_bienvenida()
        self.crear_barcos()
        print("\nTablero de barcos jugador local: ")
        self.tablero_local_barcos.imprimir()
        print()
        Juego.mensaje_post_colocacion()
        print("\nTablero de disparos jugador local: ")
        self.tablero_local_disparos.imprimir()

    # Función para que empiece a disparar el jugador o la máquina
    def jugar_ronda(self):
        if self.turno_jugador:
            print("Turno del jugador: \n")
            self.forzar_salir = self.disparar_o_salir(self.tablero_local_disparos, self.tablero_enemigo_barcos) # La función devuelve True si insertamos el numero 2
            if(self.forzar_salir == False):
                self.tablero_local_disparos.imprimir()
        else:
            print("Turno de la máquina: \n")
            while self.IA.disparar_maquina(self.tablero_enemigo_disparos, self.tablero_local_barcos):
                # Borramos los barcos destruidos del jugador local
                barcos_jugador_local_copia = self.barcos_jugador_local.copy()
                for barco in barcos_jugador_local_copia:
                    if self.tablero_local_barcos.rango_igual_a_valor(Tablero.barco_tocado, barco.min_fila, barco.max_fila, barco.min_columna, barco.max_columna):
                        self.barcos_jugador_local.remove(barco)
                if self.juego_terminado():
                    break
            self.tablero_enemigo_disparos.imprimir()

        # Borramos los barcos destruidos del jugador local
        barcos_jugador_local_copia = self.barcos_jugador_local.copy()
        for barco in barcos_jugador_local_copia:
            if self.tablero_local_barcos.rango_igual_a_valor(Tablero.barco_tocado, barco.min_fila, barco.max_fila, barco.min_columna, barco.max_columna):
                self.barcos_jugador_local.remove(barco)

        # Borramos los barcos destruidos de la maquina
        barcos_maquina_copia = self.barcos_maquina.copy()
        for barco in barcos_maquina_copia:
            if self.tablero_enemigo_barcos.rango_igual_a_valor(Tablero.barco_tocado, barco.min_fila, barco.max_fila, barco.min_columna, barco.max_columna):
                self.barcos_maquina.remove(barco)

        if len(self.barcos_jugador_local) == 0:
            print("¡Lo siento! La máquina siempre gana, MUAHAHA!")
        elif len(self.barcos_maquina) == 0:
            print("¡Enhorabuena! Has ganado la partida.")

        self.turno_jugador = not self.turno_jugador

    def juego_terminado(self):
        return self.forzar_salir == True or len(self.barcos_jugador_local) == 0 or len(self.barcos_maquina) == 0


    def mostrar_mensaje_bienvenida():
        mensaje_inicial = """

¡Bienvenido!

Vas a jugar al juego de "Hundir la flota". Ten en cuenta que:
1. Hay dos jugadores: la máquina y tú.
2. Vas a colocar 10 barcos de diferentes longitudes en un tablero, y tu rival hará lo mismo con los suyos.
3. Por turnos, tienes que ir disparando a los barcos de tu rival, si aciertas, podrás continuar disparando.
4. El jugador que hunda todos los barcos del contrincante ganará la partida.
¡SUERTE!

    """
    
        print(mensaje_inicial)

    # FUNCIÓN PARA CREAR LOS BARCOS TANTO ALEATORIAMENTE COMO DE MANERA MANUAL
    def crear_barcos(self):
        opcion = False

        # Barcos del jugador local
        while opcion == False:
            opcion_1 = input("¿Quieres crear tus barcos aleatoriamente? Ingresa 'si' o 'no': ")

            if opcion_1.lower() == "si":
                self.crear_barcos_aleatorios(self.tablero_local_barcos, self.barcos_jugador_local)

            elif opcion_1.lower() =="no":
                self.crear_barcos_manuales(self.tablero_local_barcos, self.barcos_jugador_local)
            else:
                input("Opción incorrecta, por favor ingresa 'si' o 'no': ")
                continue

            opcion = True
        
        # Barcos de la máquina
        self.crear_barcos_aleatorios(self.tablero_enemigo_barcos, self.barcos_maquina)

    # FUNCIÓN PARA CREAR LOS BARCOS ALEATORIAMENTE, DE ARGUMENTOS: TABLERO AL QUE AÑADIRLO Y LA LISTA DE BARCOS DONDE METERLOS
    def crear_barcos_aleatorios(self, tablero, barcos):
        for l in Juego.longitudes:
            barco = self.generar_barco(tablero, l)
            barcos.append(barco)
            self.colocar_barco(tablero, barco)

    # FUNCIÓN PARA GENERAR EL BARCO DENTRO DEL TABLERO RESPETANDO LAS POSICIONES VÁLIDAS
    def generar_barco(self, tablero, longitud):
        posicion_valida = False # por defecto False para que si me da True continúe creando el barco

        min_fila = 0
        max_fila = 0
        min_columna = 0
        max_columna = 0

        while posicion_valida == False:
            fila = tablero.fila_aleatoria()
            columna = tablero.columna_aleatoria()
            orientacion = Juego.generar_orientacion()

            # Para ver si hay fallos hacemos lo siguiente, si no hay fallos hemos generado una buena posición:
            if orientacion == "O":
                min_fila = max_fila = fila
                min_columna = columna-(longitud - 1)
                max_columna = columna
                if tablero.columna_valida(min_columna) == False: # le digo la posición final para ver si queda dentro del tablero
                    continue
            
            if orientacion == "N":
                min_fila = fila-(longitud - 1)
                max_fila = fila
                min_columna = max_columna = columna
                if tablero.fila_valida(min_fila) == False:
                    continue

            if orientacion == "S":
                max_fila = fila+(longitud - 1)
                min_fila = fila
                max_columna = min_columna = columna
                if tablero.fila_valida(max_fila) == False:
                    continue
            
            if orientacion == "E":
                max_columna = columna+(longitud - 1)
                min_columna = columna
                max_fila = min_fila = fila
                if tablero.columna_valida(max_columna) == False:
                    continue
            
            # Si no hay agua en ese punto volver a empezar el bucle
            if not tablero.rango_igual_a_valor(Tablero.agua, min_fila, max_fila, min_columna, max_columna):
                continue

            posicion_valida = True # Condición de parada del while
        return Barco(min_fila, max_fila, min_columna, max_columna)

    # FUNCIÓN PARA GENERAR UNA ORIENTACIÓN ALEATORIA
    def generar_orientacion():
        return random.choice(Juego.orientaciones)

    # FUNCIÓN PARA COLOCAR EL BARCO EN EL TABLERO CORRESPONDIENTE A TRAVÉS DE UN RANGO
    def colocar_barco(self, tablero, barco):
        tablero.establecer_valor_a_rango_posicion(Tablero.barco_no_tocado, barco.min_fila, barco.max_fila, barco.min_columna, barco.max_columna)

    # FUNCIÓN PARA CREAR EL BARCO CON COORDENADAS MANUALES DENTRO DE LOS LÍMITES DEL TABLERO
    def crear_barcos_manuales(self, tablero, barcos):  
        longitudes_disponibles = Juego.longitudes.copy()

        while len(longitudes_disponibles) > 0:

            long_barco = -1
            while long_barco not in longitudes_disponibles:
                long_barco = int(input("Introduce la longitud de tu barco, recuerda que estas son las longitudes disponibles: " + str(longitudes_disponibles) + " "))
                if(long_barco not in longitudes_disponibles):
                    print("Longitud invalida, por favor introduce alguna de las siguientes longitudes disponibles: ", longitudes_disponibles)

            posicion_valida = False
            while posicion_valida == False:

                pregunta_fila = ""
                pregunta_columna = ""

                if long_barco == 1:
                    pregunta_fila = "¿En qué fila quieres colocar tu barco? "
                    pregunta_columna = "¿En qué columna quieres colocar tu barco? "
                else:
                    pregunta_fila = "¿En qué fila quieres empezar a colocar tu barco? "
                    pregunta_columna = "¿En qué columna quieres empezar a colocar tu barco? "

                fila = int(input(pregunta_fila))
                if tablero.fila_valida(fila-1) == False:
                    print("La fila introducida es inválida, por favor, introduce una entre 1 y ", Juego.filas)
                    continue

                columna = int(input(pregunta_columna))
                if tablero.columna_valida(columna-1) == False:
                    print("La columna introducida es inválida, por favor, introduce una entre 1 y ", Juego.columnas)
                    continue

                if long_barco == 1:
                    min_fila = fila -1
                    max_fila = fila -1
                    min_columna = columna -1 
                    max_columna = columna -1
                else:
                    min_fila = 0
                    max_fila = 0
                    min_columna = 0
                    max_columna = 0
                    orientacion_manual = input("¿Qué orientación va a tomar tu barco? Introduce 'N' (norte), 'S' (sur), 'E' (este), u 'O' (oeste) ").upper()

                    if orientacion_manual == 'N':
                        min_fila = (fila -(long_barco - 1)) -1
                        max_fila = fila -1
                        min_columna = max_columna = columna -1
                        if tablero.fila_valida(min_fila-1) == False:
                            print("La combinación de coordenadas, orientación y longitud no son válidas.")
                            continue
                    
                    if orientacion_manual == 'S':
                        max_fila = (fila +(long_barco - 1)) - 1
                        min_fila = fila -1
                        max_columna = min_columna = columna -1
                        if tablero.fila_valida(max_fila-1) == False:
                            print("La combinación de coordenadas, orientación y longitud no son válidas.")
                            continue

                    if orientacion_manual == 'E':
                        max_columna = (columna +(long_barco - 1)) -1
                        min_columna = columna -1
                        max_fila = min_fila = fila -1
                        if tablero.columna_valida(max_columna-1) == False:
                            print("La combinación de coordenadas, orientación y longitud no son válidas.")
                            continue

                    if orientacion_manual == 'O':
                        min_fila = max_fila = fila -1
                        min_columna = (columna -(long_barco - 1)) -1
                        max_columna = columna -1
                        if tablero.columna_valida(min_columna-1) == False: 
                            print("La combinación de coordenadas, orientación y longitud no son válidas.")
                            continue
                    
                    # Si en el rango del barco hay algo diferente a agua, vuelve a empezar el bucle
                    if not tablero.rango_igual_a_valor(Tablero.agua, min_fila, max_fila, min_columna, max_columna):
                        print("La combinación de coordenadas, orientación y longitud no son válidas.")
                        continue
                
                longitudes_disponibles.remove(long_barco) # Para ver las longitudes de los barcos que nos quedan
                posicion_valida = True # Fin del bucle

                barco_manual = Barco(min_fila, max_fila, min_columna, max_columna)
                barcos.append(barco_manual)
                self.colocar_barco(tablero, barco_manual)
                self.tablero_local_barcos.imprimir()
        
    def mensaje_post_colocacion():
    
        mensaje_2 = """

¡GENIAL!

Ya has creado tu tablero con todos tus barcos. Es hora de comenzar la partida.
¿Estás preparado para disparar?

    """

        print(mensaje_2)


    def disparar_o_salir(self, tablero_local, tablero_maquina):
        opcion_valida = False
        decision = -1
        while opcion_valida == False:
            try:
                if decision == 1:
                    tablero_local.imprimir()

                decision = int(input("Para disparar ingresa '1', para salir del juego ingresa '2': "))
                if decision == 1:
                    posicion_valida = False
                    while posicion_valida == False:
                        fila = int(input("¿A qué fila quieres disparar? ")) - 1
                        columna = int(input("¿A qué columna quieres disparar? ")) - 1
                        posicion_valida = tablero_local.fila_valida(fila) and tablero_local.columna_valida(columna)
                        if posicion_valida == False:
                            print("Por favor, introduce una posición válida.")
                    
                    valor_anterior = tablero_maquina.valor(fila, columna) # Último valor del disparo de la ronda anterior
                    self.disparo(tablero_local, tablero_maquina, fila, columna)
                    valor_nuevo = tablero_maquina.valor(fila, columna) # Nuevo valor, que será el valor anterior en el próximo turno
                    if tablero_local.posicion_igual_a_valor(Tablero.barco_tocado, fila, columna) and valor_anterior != valor_nuevo :
                        continue # Si hemos tocado un barco y no es de un disparo que hayamos hecho previamente, continúa disparando

                elif decision == 2:
                    print("Has finalizado la partida.")
                    return True # Sale del juego porque devuelve True a la variable "forzar_salir" de la función jugar_ronda

                else:
                    print("El número introducido no es correcto. Por favor, ingresa 1 para disparar o 2 para salir. ")
                    continue

            except ValueError:
                print("Parece que ha habido un error, probemos de nuevo. ")
                continue

            opcion_valida = True
            
        return False


    def disparo(self, tablero_local, tablero_maquina, fila, columna):
        if tablero_maquina.posicion_igual_a_valor(Tablero.agua, fila, columna):
            tablero_local.establecer_valor_a_posicion(Tablero.agua_tocada, fila, columna)
            tablero_maquina.establecer_valor_a_posicion(Tablero.agua_tocada, fila, columna)
            print("AGUA - [", fila + 1, ",", columna + 1, "]")

        elif tablero_maquina.posicion_igual_a_valor(Tablero.barco_no_tocado, fila, columna):
            tablero_local.establecer_valor_a_posicion(Tablero.barco_tocado, fila, columna)
            tablero_maquina.establecer_valor_a_posicion(Tablero.barco_tocado, fila, columna)
            print("TOCADO O HUNDIDO - [", fila + 1, ",", columna + 1, "]")

        

            