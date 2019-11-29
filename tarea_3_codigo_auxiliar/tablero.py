# Esta clase represnta el tablero
class Tablero(object):

    def __init__(self, original=None, altura=6, ancho=7):

        if (original):
            self.tablero = [list(columna) for columna in original.tablero]
            self.numeroMovimientos = original.numeroMovimientos
            self.altura = original.altura
            self.ancho = original.ancho
            return

        # crear tablero nuevo
        else:
            self.altura = altura
            self.ancho = ancho
            self.tablero = [[] for x in range(self.ancho)]
            self.numeroMovimientos = 0
            return

    # colocar una ficha en la columna definida
    #    0 - Jugador 1 ficha
    #    1 - Jugador 2 ficha
    def realizarMovimiento(self, columna):
        ficha = self.numeroMovimientos % 2
        self.numeroMovimientos += 1
        self.tablero[columna].append(ficha)

    # chequea si el tablero es terminal y retorna:
    #   -1 if the game is not over yet
    #    0 if it's a draw
    #    1 if Jugador 1 is the winner
    #    2 if Jugador 2 is the winner
    def esMeta(self):
        for i in range(0, self.ancho):
            for j in range(0, self.altura):
                try:
                    if self.tablero[i][j] == self.tablero[i + 1][j] == self.tablero[i + 2][j] == self.tablero[i + 3][j]:
                        return self.tablero[i][j] + 1
                except IndexError:
                    pass

                try:
                    if self.tablero[i][j] == self.tablero[i][j + 1] == self.tablero[i][j + 2] == self.tablero[i][j + 3]:
                        return self.tablero[i][j] + 1
                except IndexError:
                    pass

                try:
                    if not j + 3 > self.altura and self.tablero[i][j] == self.tablero[i + 1][j + 1] == self.tablero[i + 2][
                        j + 2] == self.tablero[i + 3][j + 3]:
                        return self.tablero[i][j] + 1
                except IndexError:
                    pass

                try:
                    if not j - 3 < 0 and self.tablero[i][j] == self.tablero[i + 1][j - 1] == self.tablero[i + 2][j - 2] == \
                            self.tablero[i + 3][j - 3]:
                        return self.tablero[i][j] + 1
                except IndexError:
                    pass
        if self.estaLleno():
            return 0
        return -1

    # devuelve True cuando el tablero esta lleno
    def estaLleno(self):
        return self.numeroMovimientos == self.ancho * self.altura

    # devuelve heurística para un tablero
    def heuristica(self):
        h = 0
        estado = self.tablero
        for i in range(0, self.ancho):
            for j in range(0, self.altura):
                # chequear rachas horizontal
                try:
                    # jugador 1
                    if estado[i][j] == estado[i + 1][j] == 0:
                        h += 10
                    if estado[i][j] == estado[i + 1][j] == estado[i + 2][j] == 0:
                        h += 100
                    if estado[i][j] == estado[i + 1][j] == estado[i + 2][j] == estado[i + 3][j] == 0:
                        h += 10000

                    # jugador 2
                    if estado[i][j] == estado[i + 1][j] == 1:
                        h -= 10
                    if estado[i][j] == estado[i + 1][j] == estado[i + 2][j] == 1:
                        h -= 100
                    if estado[i][j] == estado[i + 1][j] == estado[i + 2][j] == estado[i + 3][j] == 1:
                        h -= 10000
                except IndexError:
                    pass

                # chequear rachas verticales
                try:
                    # jugador 1
                    if estado[i][j] == estado[i][j + 1] == 0:
                        h += 10
                    if estado[i][j] == estado[i][j + 1] == estado[i][j + 2] == 0:
                        h += 100
                    if estado[i][j] == estado[i][j + 1] == estado[i][j + 2] == estado[i][j + 3] == 0:
                        h += 10000

                    # jugador 2
                    if estado[i][j] == estado[i][j + 1] == 1:
                        h -= 10
                    if estado[i][j] == estado[i][j + 1] == estado[i][j + 2] == 1:
                        h -= 100
                    if estado[i][j] == estado[i][j + 1] == estado[i][j + 2] == estado[i][j + 3] == 1:
                        h -= 10000
                except IndexError:
                    pass

                # chequear rachas en diagonal positiva
                try:
                    # jugador 1
                    if not j + 3 > self.altura and estado[i][j] == estado[i + 1][j + 1] == 0:
                        h += 10
                    if not j + 3 > self.altura and estado[i][j] == estado[i + 1][j + 1] == estado[i + 2][j + 2] == 0:
                        h += 100
                    if not j + 3 > self.altura and estado[i][j] == estado[i + 1][j + 1] == estado[i + 2][j + 2] \
                            == estado[i + 3][j + 3] == 0:
                        h += 10000

                    # jugador 2
                    if not j + 3 > self.altura and estado[i][j] == estado[i + 1][j + 1] == 1:
                        h -= 10
                    if not j + 3 > self.altura and estado[i][j] == estado[i + 1][j + 1] == estado[i + 2][j + 2] == 1:
                        h -= 100
                    if not j + 3 > self.altura and estado[i][j] == estado[i + 1][j + 1] == estado[i + 2][j + 2] \
                            == estado[i + 3][j + 3] == 1:
                        h -= 10000
                except IndexError:
                    pass

                # chequear rachas en diagonal negativa
                try:
                    # jugador 1
                    if not j - 3 < 0 and estado[i][j] == estado[i + 1][j - 1] == 0:
                        h += 10
                    if not j - 3 < 0 and estado[i][j] == estado[i + 1][j - 1] == estado[i + 2][j - 2] == 0:
                        h += 100
                    if not j - 3 < 0 and estado[i][j] == estado[i + 1][j - 1] == estado[i + 2][j - 2] \
                            == estado[i + 3][j - 3] == 0:
                        h += 10000

                    # jugador 2
                    if not j - 3 < 0 and estado[i][j] == estado[i + 1][j - 1] == 1:
                        h -= 10
                    if not j - 3 < 0 and estado[i][j] == estado[i + 1][j - 1] == estado[i + 2][j - 2] == 1:
                        h -= 100
                    if not j - 3 < 0 and estado[i][j] == estado[i + 1][j - 1] == estado[i + 2][j - 2] \
                            == estado[i + 3][j - 3] == 1:
                        h -= 10000
                except IndexError:
                    pass
        return h

    def print(self):
        print("")
        print("+" + "---+" * self.ancho)
        for numeroFila in range(self.altura - 1, -1, -1):
            fila = "|"
            for numeroColumna in range(self.ancho):
                if len(self.tablero[numeroColumna]) > numeroFila:
                    fila += " " + ('1' if self.tablero[numeroColumna][numeroFila] else '0') + " |"
                else:
                    fila += "   |"
            print(fila)
            print("+" + "---+" * self.ancho)
