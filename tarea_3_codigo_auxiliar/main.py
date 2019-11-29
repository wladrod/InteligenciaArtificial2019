"""
Código basado en: Introduction to Artificial Intelligence (COMPSCI 270), Spring 2019 

Implementación de la ventana principal y el menú.
"""

import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QSpinBox,
                             QHBoxLayout, QVBoxLayout, QApplication, QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from juego import Juego


class Menu(QWidget):
    """Menú principal.

    Parámetros
    ----------
    padre : QWidget
        El objeto de la ventana principal. Se utilizará para enviar una señal al menú principal..

    """
    def __init__(self, padre):
        super(Menu, self).__init__(padre)

        # DISEÑO PRINCIPAL
        vbox = QVBoxLayout()
        vbox.addStretch(1)

        # ENCABEZADO
        intart2019 = QLabel('Inteligencia Artificial')
        intart2019.setAlignment(Qt.AlignCenter)
        intart2019.setFont(QFont('Times', 24, QFont.Bold))
        vbox.addWidget(intart2019)
        tarea3 = QLabel('Tarea 3: Conectar Cuatro')
        tarea3.setAlignment(Qt.AlignCenter)
        tarea3.setFont(QFont('Times', 18))
        vbox.addWidget(tarea3)
        vbox.addStretch(1)

        # JUGADORES
        jugadores_hbox = QHBoxLayout()
        jugadores_hbox.addStretch(4)

        # Jugador 1 Opciones
        jugador1 = QComboBox()
        jugador1.addItems(['Humano', 'Aleatorio', 'IA-Minimax', 'IA-AlphaBeta'])
        jugador1_etiqueta = QLabel('Jugador 1: ')
        jugador1_etiqueta.setBuddy(jugador1)
        jugadores_hbox.addWidget(jugador1_etiqueta)
        jugadores_hbox.addWidget(jugador1)

        jugadores_hbox.addStretch(1)

        # Jugador 2 Opciones
        jugador2 = QComboBox()
        jugador2.addItems(['Humano', 'Aleatorio', 'IA-Minimax', 'IA-AlphaBeta'])
        jugador2_etiqueta = QLabel('Jugador 2: ')
        jugador2_etiqueta.setBuddy(jugador2)
        jugadores_hbox.addWidget(jugador2_etiqueta)
        jugadores_hbox.addWidget(jugador2)

        jugadores_hbox.addStretch(4)

        vbox.addLayout(jugadores_hbox)
        vbox.addStretch(1)

        # PROFUNDIDAD
        profundidad_encabezado = QLabel('IA Dificultad (Límite Profundidad)')
        profundidad_encabezado.setAlignment(Qt.AlignCenter)
        profundidad_encabezado.setFont(QFont('Times', 15))
        vbox.addWidget(profundidad_encabezado)
        profundidad_hbox = QHBoxLayout()
        profundidad_hbox.addStretch(5)
        profundidad1 = QSpinBox()
        profundidad1.setMinimum(1)
        profundidad1.setMaximum(16)
        profundidad1_etiqueta = QLabel('Jugador 1: ')
        profundidad1_etiqueta.setBuddy(profundidad1_etiqueta)
        profundidad_hbox.addWidget(profundidad1_etiqueta)
        profundidad_hbox.addWidget(profundidad1)
        profundidad_hbox.addStretch(1)
        profundidad2 = QSpinBox()
        profundidad2.setMinimum(1)
        profundidad2.setMaximum(16)
        profundidad2_etiqueta = QLabel('Jugador 2: ')
        profundidad2_etiqueta.setBuddy(profundidad2_etiqueta)
        profundidad_hbox.addWidget(profundidad2_etiqueta)
        profundidad_hbox.addWidget(profundidad2)
        profundidad_hbox.addStretch(5)
        vbox.addLayout(profundidad_hbox)
        vbox.addStretch(1)

        # TAMAÑO TABLERO
        tablero_hbox = QHBoxLayout()
        tablero_hbox.addStretch(4)

        # Altura Opciones
        altura = QSpinBox()
        altura.setMinimum(6)
        altura.setMaximum(16)
        altura_etiqueta = QLabel('Altura: ')
        altura_etiqueta.setBuddy(altura)
        tablero_hbox.addWidget(altura_etiqueta)
        tablero_hbox.addWidget(altura)

        tablero_hbox.addStretch(1)

        # Ancho Opciones
        ancho = QSpinBox()
        ancho.setMinimum(7)
        ancho.setMaximum(16)
        ancho_etiqueta = QLabel('Ancho: ')
        ancho_etiqueta.setBuddy(ancho)
        tablero_hbox.addWidget(ancho_etiqueta)
        tablero_hbox.addWidget(ancho)

        tablero_hbox.addStretch(4)
        vbox.addLayout(tablero_hbox)

        vbox.addStretch(1)

        # INICIO
        inicio_hbox = QHBoxLayout()
        inicio_hbox.addStretch(1)
        inicio = QPushButton('Iniciar')
        inicio.clicked.connect(lambda: padre.inicio(jugador1.currentText(), jugador2.currentText(), profundidad1.value(),
                                                   profundidad2.value(), altura.value(), ancho.value()))
        inicio_hbox.addWidget(inicio)
        inicio_hbox.addStretch(1)
        vbox.addLayout(inicio_hbox)
        vbox.addStretch(3)

        self.setLayout(vbox)


class VentanaPrincipal(QWidget):
    """Widget principal de la aplicación que maneja las transiciones entre el menú principal
     y el juego..
    """
    def __init__(self):
        super(VentanaPrincipal, self).__init__()

        self.resize(512, 512)
        self.setWindowTitle('Inteligencia Artificial - Tarea 3 - Conectar-Cuatro')

        layout = QVBoxLayout()
        layout.addWidget(Menu(self))
        self.setLayout(layout)

    def limpiar(self):
        """Elimina los widgets adjuntos a la ventana principal.
        """
        for i in reversed(range(self.layout().count())):
            self.layout().itemAt(i).widget().deleteLater()

    def inicio(self, jugador1_nombre, jugador2_nombre, profundidad1_limite, profundidad2_limite, altura, ancho):
        """Crea un juego usando los parámetros.

        Parameters
        ----------
        jugador1_nombre : str
            El nombre del primer jugador. Debe ser uno de 'Humano', 'Aleatorio', 'IA-Minimax', 'IA-AlphaBeta'.

        jugador2_nombre : str
            El nombre del segundo jugador. Debe ser uno de 'Humano', 'Aleatorio', 'IA-Minimax', 'IA-AlphaBeta'.

        profundidad1_limite : int
            La máxima profundidad de búsqueda a ser usada en el algoritmo Minimax por la primera IA.

        profundidad2_limite : int
             La máxima profundidad de búsqueda a ser usada en el algoritmo Minimax por la segunda IA.

        altura : int
            La altura del tablero. Debe ser mayor o igual que 4.

        ancho : int
            El ancho del tablero. Debe ser mayor o igual que 4.
        """
        self.limpiar()
        self.layout().addWidget(Juego(self, jugador1_nombre, jugador2_nombre, profundidad1_limite, profundidad2_limite, altura, ancho))

    def nuevojuego(self):
        """Crea el menú principal.
        """
        self.clear()
        self.layout().addWidget(Menu(self))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    w = VentanaPrincipal()
    w.show()

    sys.exit(app.exec_())
