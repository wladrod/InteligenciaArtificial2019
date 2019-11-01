# Código adaptado(traducido) del siguiente sitio:

# Sample code from https://www.redblobgames.com/pathfinding/a-star/
# Copyright 2014 Red Blob Games <redblobgames@gmail.com>
#
# Feel free to use this code in your own projects, including commercial projects
# License: Apache v2.0 <http://www.apache.org/licenses/LICENSE-2.0.html>


class GrafoSimple:

    def __init__(self):
        self.aristas = {}

    def vecinos(self, id):
        return self.aristas[id]


grafo_ejemplo = GrafoSimple()
grafo_ejemplo.aristas = {
    'A': ['B'],
    'B': ['A', 'C', 'D'],
    'C': ['A'],
    'D': ['E', 'A'],
    'E': ['B']
}

import collections


class Cola:

    def __init__(self):
        self.elementos = collections.deque()

    def vacia(self):
        return len(self.elementos) == 0

    def agregar(self, x):
        self.elementos.append(x)

    def obtener(self):
        return self.elementos.popleft()


class Pila:

    def __init__(self):
        self.elementos = collections.deque()

    def vacia(self):
        return len(self.elementos) == 0

    def agregar(self, x):
        self.elementos.append(x)

    def obtener(self):
        return self.elementos.pop()


# funciones de utilidad para manejar cuadriculas
def de_id_ancho(id, ancho):
    return (id % ancho, id // ancho)


def dibujar_celda(grafo, id, estilo, ancho):
    r = "."
    if 'numero' in estilo and id in estilo['numero']:
        r = "%d" % estilo['numero'][id]
    if 'apunta_a' in estilo and estilo['apunta_a'].get(id, None) is not None:
        (x1, y1) = id
        (x2, y2) = estilo['apunta_a'][id]
        if x2 == x1 + 1: r = ">"
        if x2 == x1 - 1: r = "<"
        if y2 == y1 + 1: r = "v"
        if y2 == y1 - 1: r = "^"
    if 'inicio' in estilo and id == estilo['inicio']:
        r = "A"
    if 'meta' in estilo and id == estilo['meta']:
        r = "Z"
    if 'camino' in estilo and id in estilo['camino']:
        r = "@"
    if id in grafo.paredes:
        r = "#" * ancho
    return r


def dibujar_cuadricula(grafo, ancho=2, **estilo):
    for y in range(grafo.altura):
        for x in range(grafo.ancho):
            print("%%-%ds" % ancho % dibujar_celda(grafo, (x, y), estilo, ancho), end="")
        print()


DIAGRAMA1_PAREDES = [de_id_ancho(id, ancho=30) for id in [21,22,51,52,81,82,93,94,111,112,123,124,133,134,141,142,153,154,163,164,171,172,173,174,175,183,184,193,194,201,202,203,204,205,213,214,223,224,243,244,253,254,273,274,283,284,303,304,313,314,333,334,343,344,373,374,403,404,433,434]]


class RejillaCuadrada:
    def __init__(self, ancho, altura):
        self.ancho = ancho
        self.altura = altura
        self.paredes = []

    def en_limites(self, id):
        (x, y) = id
        return 0 <= x < self.ancho and 0 <= y < self.altura

    def pasable(self, id):
        return id not in self.paredes

    def vecinos(self, id):
        (x, y) = id
        resultados = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        if (x + y) % 2 == 0: resultados.reverse()  # estetica
        resultados = filter(self.en_limites, resultados)
        resultados = filter(self.pasable, resultados)
        return resultados


class RejillaConPesos(RejillaCuadrada):
    def __init__(self, ancho, altura):
        super().__init__(ancho, altura)
        self.pesos = {}

    def costo(self, desde_nodo, a_nodo):
        return self.pesos.get(a_nodo, 1)


diagrama4 = RejillaConPesos(10, 10)
diagrama4.paredes = [(1, 7), (1, 8), (2, 7), (2, 8), (3, 7), (3, 8)]
diagrama4.pesos = {loc: 5 for loc in [(3, 4), (3, 5), (4, 1), (4, 2),
                                       (4, 3), (4, 4), (4, 5), (4, 6),
                                       (4, 7), (4, 8), (5, 1), (5, 2),
                                       (5, 3), (5, 4), (5, 5), (5, 6),
                                       (5, 7), (5, 8), (6, 2), (6, 3),
                                       (6, 4), (6, 5), (6, 6), (6, 7),
                                       (7, 3), (7, 4), (7, 5)]}

import heapq


class ColaPrioridad:
    def __init__(self):
        self.elementos = []

    def vacia(self):
        return len(self.elementos) == 0

    def agregar(self, item, prioridad):
        heapq.heappush(self.elementos, (prioridad, item))

    def obtener(self):
        return heapq.heappop(self.elementos)[1]


def busqueda_dijkstra(grafo, inicio, meta):
    frontera = ColaPrioridad()
    frontera.agregar(inicio, 0)
    vino_de = {}
    costo_hasta_ahora = {}
    vino_de[inicio] = None
    costo_hasta_ahora[inicio] = 0

    while not frontera.vacia():
        actual = frontera.obtener()

        if actual == meta:
            break

        for proximo in grafo.vecinos(actual):
            nuevo_costo = costo_hasta_ahora[actual] + grafo.cost(actual, proximo)
            if proximo not in costo_hasta_ahora or nuevo_costo < costo_hasta_ahora[proximo]:
                costo_hasta_ahora[proximo] = nuevo_costo
                prioridad = nuevo_costo
                frontera.agregar(proximo, prioridad)
                vino_de[proximo] = actual

    return vino_de, costo_hasta_ahora


def reconstruir_camino(vino_de, inicio, meta):
    actual = meta
    camino = []
    while actual != inicio:
        camino.append(actual)
        actual = vino_de[actual]
    camino.append(inicio)  # opcional
    camino.reverse()  # opcional
    return camino


def heuristica(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def busqueda_a_estrella(grafo, inicio, meta):
    frontera = ColaPrioridad()
    frontera.agregar(inicio, 0)
    vino_de = {}
    costo_hasta_ahora = {}
    vino_de[inicio] = None
    costo_hasta_ahora[inicio] = 0

    while not frontera.vacia():
        actual = frontera.obtener()

        if actual == meta:
            break

        for proximo in grafo.vecinos(actual):
            nuevo_costo = costo_hasta_ahora[actual] + grafo.cost(actual, proximo)
            if proximo not in costo_hasta_ahora or nuevo_costo < costo_hasta_ahora[proximo]:
                costo_hasta_ahora[proximo] = nuevo_costo
                prioridad = nuevo_costo + heuristica(meta, proximo)
                frontera.agregar(proximo, prioridad)
                vino_de[proximo] = actual

    return vino_de, costo_hasta_ahora
