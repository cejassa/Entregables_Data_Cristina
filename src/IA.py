from enum import Enum
import Tablero
from Tablero import Tablero

# ENUMERACIONES PARA EL ESTADO DE LA IA 

class IA:

    class Estado_IA(Enum):
        BUSCANDO_POSICION_ALEATORIA = 1
        BUSCANDO_ORIENTACION = 2
        SIGUIENDO_ORIENTACION = 3

    orientaciones = ['N', 'S', 'E', 'O']

    def __init__(self):
            self.estado_ia = IA.Estado_IA.BUSCANDO_POSICION_ALEATORIA # Por defecto, lo primero que hace es buscar una posición
            self.orientaciones_ia = IA.orientaciones.copy() # Creamos la variable aparte porque iremos borrando las que ya utilice y no queremos borrar las generales
            self.ultimo_disparo_ia = [] # Para que recuerde el último punto para su próximo disparo
            self.disparo_inicial_ia = [] # Para cuando tenga que cambiar la dirección hacia la opuesta, sepa de donde partir
            self.orientacion_actual_ia = None

    def disparo(self, tablero_local, tablero_maquina, fila, columna):
        if tablero_maquina.posicion_igual_a_valor(Tablero.agua, fila, columna):
            tablero_local.establecer_valor_a_posicion(Tablero.agua_tocada, fila, columna)
            tablero_maquina.establecer_valor_a_posicion(Tablero.agua_tocada, fila, columna)
            print("AGUA - [", fila + 1, ",", columna + 1, "]")

        elif tablero_maquina.posicion_igual_a_valor(Tablero.barco_no_tocado, fila, columna):
            tablero_local.establecer_valor_a_posicion(Tablero.barco_tocado, fila, columna)
            tablero_maquina.establecer_valor_a_posicion(Tablero.barco_tocado, fila, columna)
            print("TOCADO O HUNDIDO - [", fila + 1, ",", columna + 1, "]")

    def disparar_maquina(self, tablero_maquina, tablero_local):
        if self.estado_ia == IA.Estado_IA.BUSCANDO_POSICION_ALEATORIA:
            fila = tablero_maquina.fila_aleatoria()
            columna = tablero_maquina.columna_aleatoria()

            if tablero_maquina.posicion_igual_a_valor(Tablero.barco_tocado, fila, columna) or tablero_maquina.posicion_igual_a_valor(Tablero.agua_tocada, fila, columna): # Si ya hay un barco tocado, busca otra coordenada de disparo
                return self.disparar_maquina(tablero_maquina, tablero_local)
            else:
                valor_anterior = tablero_maquina.valor(fila, columna) # para comprobar después que no volvemos a disparar a una coordenada que ya hayamos acertado
                self.disparo(tablero_maquina, tablero_local, fila, columna)
                self.ultimo_disparo_ia = [fila, columna]
                valor_nuevo = tablero_maquina.valor(fila, columna)

                # TO-DO: Añadir a este if que si el maximo de la lista de longitud de barcos enemigos es igual a 1, llame a disparar_maquina y se quede en BUSCANDO_POSICION_ALEATORIA
                if tablero_maquina.posicion_igual_a_valor(Tablero.barco_tocado, fila, columna) and valor_anterior != valor_nuevo :
                    self.estado_ia = IA.Estado_IA.BUSCANDO_ORIENTACION
                    self.disparo_inicial_ia = self.ultimo_disparo_ia # Empezamos buscando desde la posición del último disparo
                    return True

        elif self.estado_ia == IA.Estado_IA.BUSCANDO_ORIENTACION:
            if len(self.orientaciones_ia) == 0:
                self.orientaciones_ia = IA.orientaciones.copy()
                self.orientacion_actual_ia = None
                self.estado_ia = IA.Estado_IA.BUSCANDO_POSICION_ALEATORIA
                return self.disparar_maquina(tablero_maquina, tablero_local)
            else:
                self.orientacion_actual_ia = self.orientaciones_ia.pop() # Quita el último elemento de la lista de orientaciones y lo asigna a la orientación actual

                fila = self.ultimo_disparo_ia[0]
                columna = self.ultimo_disparo_ia[1]

                if self.orientacion_actual_ia == 'N':
                    fila = fila - 1
                elif self.orientacion_actual_ia == 'S':
                    fila = fila + 1
                elif self.orientacion_actual_ia == 'E':
                    columna = columna + 1
                elif self.orientacion_actual_ia == 'O':
                    columna = columna - 1

                if tablero_maquina.fila_valida(fila) and tablero_maquina.columna_valida(columna):
                    valor_anterior = tablero_maquina.valor(fila, columna) # que caracter tiene el tablero en esa posición antes de realizar el disparo
                    if valor_anterior != Tablero.agua:
                        return self.disparar_maquina(tablero_maquina, tablero_local)
                    else:
                        self.disparo(tablero_maquina, tablero_local, fila, columna)
                        valor_nuevo = tablero_maquina.valor(fila, columna) # caracter después del disparo

                        if tablero_maquina.posicion_igual_a_valor(Tablero.barco_tocado, fila, columna) and valor_anterior != valor_nuevo :
                            self.estado_ia = IA.Estado_IA.SIGUIENDO_ORIENTACION
                            self.ultimo_disparo_ia = [fila, columna]
                            self.orientaciones_ia = IA.orientaciones.copy()
                            return True

                else:
                    return self.disparar_maquina(tablero_maquina, tablero_local)

        elif self.estado_ia == IA.Estado_IA.SIGUIENDO_ORIENTACION:

            fila = self.ultimo_disparo_ia[0]
            columna = self.ultimo_disparo_ia[1]

            if self.orientacion_actual_ia == 'N':
                fila = fila - 1
            elif self.orientacion_actual_ia == 'S':
                fila = fila + 1
            elif self.orientacion_actual_ia == 'E':
                columna = columna + 1
            elif self.orientacion_actual_ia == 'O':
                columna = columna - 1

            if tablero_maquina.fila_valida(fila) and tablero_maquina.columna_valida(columna):
                
                valor_anterior = tablero_maquina.valor(fila, columna)
                if valor_anterior == Tablero.barco_tocado:
                    
                    if self.orientacion_actual_ia == 'N':
                        self.orientacion_actual_ia = 'S'
                    elif self.orientacion_actual_ia == 'S':
                        self.orientacion_actual_ia = 'N'
                    elif self.orientacion_actual_ia == 'E':
                        self.orientacion_actual_ia = 'O'
                    elif self.orientacion_actual_ia == 'O':
                        self.orientacion_actual_ia = 'E'

                    self.ultimo_disparo_ia = self.disparo_inicial_ia
                    return self.disparar_maquina(tablero_maquina, tablero_local)

                else:
                    self.disparo(tablero_maquina, tablero_local, fila, columna)
                    valor_nuevo = tablero_maquina.valor(fila, columna)
                    if tablero_maquina.posicion_igual_a_valor(Tablero.barco_tocado, fila, columna) and valor_anterior != valor_nuevo :
                        self.ultimo_disparo_ia = [fila, columna]
                        return True
                    elif tablero_maquina.posicion_igual_a_valor(Tablero.barco_tocado, fila, columna) and valor_anterior == valor_nuevo :
                        pass
                    else: # agua
                        
                        if self.orientacion_actual_ia == 'N':
                            self.orientacion_actual_ia = 'S'
                            fila = self.disparo_inicial_ia[0] + 1

                        elif self.orientacion_actual_ia == 'S':
                            self.orientacion_actual_ia = 'N'
                            fila = self.disparo_inicial_ia[0] - 1

                        elif self.orientacion_actual_ia == 'E':
                            self.orientacion_actual_ia = 'O'
                            columna = self.disparo_inicial_ia[1] - 1

                        elif self.orientacion_actual_ia == 'O':
                            columna = self.disparo_inicial_ia[1] + 1
                            self.orientacion_actual_ia = 'E'

                        self.ultimo_disparo_ia = self.disparo_inicial_ia

                        # si el proximo turno está fuera del tablero, avisa de que vaya a posicion aleatoria
                        if not tablero_local.fila_valida(fila) or not tablero_local.columna_valida(columna) or tablero_maquina.valor(fila, columna) == Tablero.barco_tocado:
                            self.estado_ia = IA.Estado_IA.BUSCANDO_POSICION_ALEATORIA
                            self.orientacion_actual_ia = None
                            self.orientaciones_ia = IA.orientaciones.copy()
                        elif tablero_maquina.valor(fila, columna) == Tablero.agua_tocada:
                            valor = Tablero.barco_tocado

                            while valor == Tablero.barco_tocado and tablero_local.fila_valida(fila) and tablero_local.columna_valida(columna):
                                if self.orientacion_actual_ia == 'N':
                                    fila = fila + 1

                                elif self.orientacion_actual_ia == 'S':
                                    fila = fila - 1 

                                elif self.orientacion_actual_ia == 'E':
                                    columna = columna - 1 

                                elif self.orientacion_actual_ia == 'O':
                                    columna = columna + 1
                                
                                if tablero_local.fila_valida(fila) and tablero_local.columna_valida(columna):
                                    valor = tablero_maquina.valor(fila, columna)
                            
                            if(valor == Tablero.agua_tocada):
                                self.estado_ia = IA.Estado_IA.BUSCANDO_POSICION_ALEATORIA
                                self.orientacion_actual_ia = None
                                self.orientaciones_ia = IA.orientaciones.copy()

            else: # no es válida la fila o la columna
                fila = self.disparo_inicial_ia[0]
                columna = self.disparo_inicial_ia[1]
                valor = Tablero.barco_tocado

                while valor == Tablero.barco_tocado and tablero_local.fila_valida(fila) and tablero_local.columna_valida(columna):
                    if self.orientacion_actual_ia == 'N':
                        fila = fila + 1

                    elif self.orientacion_actual_ia == 'S':
                        fila = fila - 1 

                    elif self.orientacion_actual_ia == 'E':
                        columna = columna - 1 

                    elif self.orientacion_actual_ia == 'O':
                        columna = columna + 1

                    if tablero_local.fila_valida(fila) and tablero_local.columna_valida(columna):
                        valor = tablero_maquina.valor(fila, columna)

                if not tablero_local.fila_valida(fila) or not tablero_local.columna_valida(columna) or tablero_maquina.valor(fila, columna) == Tablero.agua_tocada:
                    self.estado_ia = IA.Estado_IA.BUSCANDO_POSICION_ALEATORIA
                    self.orientacion_actual_ia = None
                    self.orientaciones_ia = IA.orientaciones.copy()
                    return self.disparar_maquina(tablero_maquina, tablero_local)
                else:
                    valor_anterior = tablero_maquina.valor(fila, columna) 
                    self.disparo(tablero_maquina, tablero_local, fila, columna)
                    valor_nuevo = tablero_maquina.valor(fila, columna)

                    if tablero_maquina.posicion_igual_a_valor(Tablero.barco_tocado, fila, columna) and valor_anterior != valor_nuevo :
                        self.ultimo_disparo_ia = [fila, columna]
                        if self.orientacion_actual_ia == 'N':
                            self.orientacion_actual_ia = 'S'
                        elif self.orientacion_actual_ia == 'S':
                            self.orientacion_actual_ia = 'N'
                        elif self.orientacion_actual_ia == 'E':
                            self.orientacion_actual_ia = 'O'
                        elif self.orientacion_actual_ia == 'O':
                            self.orientacion_actual_ia = 'E'
                        return True

        return False
