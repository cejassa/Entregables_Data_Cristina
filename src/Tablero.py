import numpy as np
from random import randint

class Tablero:
    agua = ' '
    agua_tocada = '-'
    barco_no_tocado = 'O'
    barco_tocado = 'X'

    def __init__(self, num_filas, num_columnas):
        self.num_filas = num_filas
        self.num_columnas = num_columnas
        self.matriz = np.full((num_filas, num_columnas), Tablero.agua)
    
    # FUNCIÓN PARA QUE ME IMPRIMA EL TABLERO CON ÍNDICES DE NÚMEROS
    def imprimir(self):
        print("  ", *range(1, self.num_columnas+1), sep="   ")
        for fila in range(1, self.num_filas+1):
            if fila == 10:
                print(fila, self.matriz[fila-1])
            else:
                print(fila, "", self.matriz[fila-1])

    # FUNCIÓN PARA GENERAR FILA Y COLUMNA ALEATORIA
    def fila_aleatoria(self):
        return randint(0, self.num_filas - 1)
    def columna_aleatoria(self):
        return randint(0, self.num_columnas - 1)

    # FUNCIÓN PARA COMPROBAR SI FILA Y COLUMNA SON VÁLIDAS 
    def fila_valida(self, fila):
        return (fila >= 0 and fila < self.num_filas)
    def fila_valida_manual(self, fila):
        return (fila > 0 and fila <= self.num_filas)
    def columna_valida(self, columna):
        return (columna >= 0 and columna < self.num_columnas)
    def columna_valida_manual(self, columna):
        return (columna > 0 and columna <= self.num_columnas)

    # FUNCIÓN PARA COMPROBAR SI EN UN PUNTO DEL TABLERO (O EN UN RANGO) HAY UN VALOR ESPECÍFICO
    def posicion_igual_a_valor(self, valor, fila, columna):
        return self.matriz[fila][columna] == valor
    def rango_igual_a_valor(self, valor, min_fila, max_fila, min_columna, max_columna):
        for fila in range(min_fila, max_fila + 1):
            for columna in range(min_columna, max_columna + 1):
                if not self.posicion_igual_a_valor(valor, fila, columna):
                    return False 
        return True 

    # FUNCIÓN PARA ESTABLECER UN VALOR A UNA POSICIÓN ESPECÍFICA (O A UN RANGO) DEL TABLERO
    def establecer_valor_a_posicion(self, valor, fila, columna):
        self.matriz[fila][columna] = valor
    def establecer_valor_a_rango_posicion(self, valor, min_fila, max_fila, min_columna, max_columna):
        self.matriz[np.arange(min_fila, max_fila+1), np.arange(min_columna, max_columna+1)] = valor

    # Valor de un punto en concreto
    def valor(self, fila, columna):
        return self.matriz[fila][columna]

    