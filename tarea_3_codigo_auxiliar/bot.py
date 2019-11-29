# Nombre:
# C.I:

# En este archivo debe implementar las siguientes funciones:
#
# 1) def generarHijos(self) - una función que genera los hijos del tablero
#    La lista de los hijos generados debe tener un formato específico.
#    Para cada hijo, el formato es (movimiento para generar este hijo, objeto hijo).
#
# 2) def miniMax(self, tablero, profundidad, jugador) - una función auxiliar
#    que implementa el algoritmo minimax.
#
# 3) def alfaBeta(self, tablero, profundidad, jugador, alfa, beta) - una función
#    auxiliar que implementa el algoritmo de poda alfa beta.


import math
from tablero import Tablero
import random


# Esta es la clase principal para tus bots de IA.
class Bot:

    def __init__(self, limiteProfundidad, esJugadorUno):

        self.esJugadorUno = esJugadorUno
        self.limiteProfundidad = limiteProfundidad

    # devolver una lista de hijos y movimientos que los generan
    def generarHijos(self, tablero):
        hijos = []
        # iterar sobre cada columna
            # si una columna no está llena:
                # 1) hacer una copia del tablero (SUGERENCIA: nuevo_tablero = Tablero(tablero))
                # 2) hacer un movimiento en la columna i, generando así un hijo
                #    (SUGERENCIA: necesita usar la función hacerMovimiento() de la clase Tablero)
                # 3) agregar una tupla (movimiento, hijo_tablero) a la lista
        #
        # NOTA: esta lista debe estar en orden (i.e. [[0, hijo_0], [1, hijo_1], ...])
        #
        #######################################################################
        #######################################################################
        #######################################################################
        #
        # TODO: agrega tu código aquí

        return hijos

# En esta clase, debe implementar el algoritmo minimax
class minMaxBot(Bot):

    def __init__(self, limiteProfundidad, esJugadorUno):
        super().__init__(limiteProfundidad, esJugadorUno)

    # devolver la columna óptima para moverse
    def encontrarMovimiento(self, tablero):
        puntaje, movimiento = self.miniMax(tablero, self.limiteProfundidad, self.esJugadorUno)
        return movimiento

    # encontrarMovimiento función auxiliar - minimax
    def miniMax(self, tablero, profundidad, jugador):
        # esta función devuelve una tupla (puntaje, movimiento)
        # 1) si el tablero está en un estado final (0,1 o 2), devuelva heurística.
        #    No nos importa devolver un movimiento, por lo que podemos devolver -1.
        # 2) si profundidad es 0, devuelve la heurística.
        #    No nos importa devolver un movimiento, por lo que podemos devolver -1.
        # 3) implementar algoritmo miniMax
        #
        # Para verificar si el estado es terminal, use la función esMeta()
        # de la clase Tablero: tablero.esMeta()
        #
        # Para obtener la heurística del tablero, use la función heuristica()
        # de la clase Tablero: tablero.heuristica()
        #
        # Recuerde seguir la regla: positivo es bueno para el Jugador 1,
        # negativo es bueno para el Jugador 2.
        #
        # Tendrás que generar hijos para el tablero,
        # y recursivamente llamar miniMax().
        # Esto debe hacerse en orden (p.ej. col. 0, 1, etc.)
        #
        # Puedes usar -math.inf para infinito negativo
        # y math.inf para infinito positivo.
        #
        #######################################################################
        #######################################################################
        #######################################################################
        #
        # TODO: agrega tu código aquí

        return (0,0)  # Esto es solo un ejemplo. Reemplace esto con su (mejorPuntaje, mejorMovimiento)


# En esta clase, debe implementar el algoritmo de poda alfa beta
class alfaBetaBot(Bot):

    def __init__(self, limiteProfundidad, esJugadorUno):
        super().__init__(limiteProfundidad, esJugadorUno)

    # devuelve la columna óptima para moverse
    def encontrarMovimiento(self, tablero):
        puntaje, movimiento = self.alfaBeta(tablero, self.limiteProfundidad, self.esJugadorUno, -math.inf, math.inf)
        return movimiento

    # encontrarMovimiento función auxiliar - poda alfa beta
    def alfaBeta(self, tablero, profundidad, jugador, alfa, beta):
         # esta función devuelve una tupla (puntaje, movimiento)
        # 1) si el tablero está en un estado final (0,1 o 2), devuelva heurística.
        #    No nos importa devolver un movimiento, por lo que podemos devolver -1.
        # 2) si profundidad es 0, devuelve la heurística.
        #    No nos importa devolver un movimiento, por lo que podemos devolver -1.
        # 3) implementar algoritmo miniMax
        #
        # Para verificar si el estado es terminal, use la función esMeta()
        # de la clase Tablero: tablero.esMeta()
        #
        # Para obtener la heurística del tablero, use la función heuristica()
        # de la clase Tablero: tablero.heuristica()
        #
        # Recuerde seguir la regla: positivo es bueno para el Jugador 1,
        # negativo es bueno para el Jugador 2.
        #
        # Tendrás que generar hijos para el tablero,
        # y recursivamente llamar alfaBeta().
        # Esto debe hacerse en orden (p.ej. col. 0, 1, etc.)
        #
        # Puedes usar -math.inf para infinito negativo
        # y math.inf para infinito positivo.
        #
        # Puede usar las funciones max(x, y) y min(x, y) para encontrar
        # máximo/mínimo de dos valores.
        #
        # Su código debe podar nodos subóptimos.
        #
        #######################################################################
        #######################################################################
        #######################################################################
        #
        # TODO: agrega tu código aquí

        return (0,0)  # Esto es solo un ejemplo. Reemplace esto con su (mejorPuntaje, mejorMovimiento)



#  bot Aleatorio
class aleatorioBot(Bot):

    def __init__(self, limiteProfundidad, esJugadorUno):
        super().__init__(limiteProfundidad, esJugadorUno)

    # devolver una columna aleatoria para moverse
    def encontrarMovimiento(self, tablero):
        movimiento = random.randint(0, tablero.width - 1)
        while len(tablero.tablero[movimiento]) == tablero.altura:
            movimiento = random.randint(0, tablero.ancho - 1)
        return movimiento

# human jugador
class JugadorHumano:

    def __init__(self, limiteProfundidad, esJugadorUno):
        pass

    def encontrarMovimiento(self, tablero):
        pass
