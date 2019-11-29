"""Implementación de la ventana de juego.

"""
from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QToolButton,
                             QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

from bot import aleatorioBot, alfaBetaBot, minMaxBot, JugadorHumano
from tablero import Tablero

from functools import partial
import sip
import copy


class Juego(QWidget):
    """Ventana del Juego.

    Parámetros
    ----------
    padre : QWidget
        El objeto de la ventana principal. Se usará para enviar una señal al menú principal.

    jugador1_nombre : str
        El nombre del primer jugador. Debería ser uno de 'Humano', 'Aleatorio', 'IA-Minimax', 'IA-AlphaBeta'.

    jugador2_nombre : str
        El nombre del segundo jugador. Debería ser uno de 'Humano', 'Aleatorio', 'IA-Minimax', 'IA-AlphaBeta'.

    profundidad1_limite : int
        La máxima profundidda de búsqueda para ser utilizada en el algoritmo Minimax por la primera IA.

    profundidad2_limite : int
        La máxima profundidda de búsqueda para ser utilizada en el algoritmo Minimax por la segunda IA.

    altura : int
        La altura del tablero. Debe ser mayor o igual que 4.

    ancho : int
        El ancho del tablero. Debe ser mayor o igual que 4.

    """

    jugadores = {
        'Humano': JugadorHumano,
        'Random': aleatorioBot,
        'AI-Minimax': minMaxBot,
        'AI-AlphaBeta': alfaBetaBot
    }
    """Mapeo de nombres jugador a clases."""

    def __init__(self, padre, jugador1_nombre, jugador2_nombre, profundidad1_limite, profundidad2_limite, altura, ancho):
        super(Juego, self).__init__(padre)

        # Construir los jugadores.
        self.jugador1 = Juego.jugadores[jugador1_nombre](profundidad1_limite, True)
        self.jugador2 = Juego.jugadores[jugador2_nombre](profundidad2_limite, False)
        self.turno = self.jugador1

        self.encabezado = QLabel()
        self.botones = []
        self.tablero = Tablero(altura=altura, ancho=ancho)

        self.tablero_widget = QWidget()
        self.fijar_iu(padre)

        # Disparar el próximo movimiento de la  IA.
        # Demora requerida para actualizar la IGU.
        QTimer.singleShot(10, self.proximo)

    def proximo(self):
        """Llamadas al método encontrarMovimiento del jugador. Si el jugador es humano, lo ignorará.
        """
        movimiento = self.turno.encontrarMovimiento(copy.deepcopy(self.tablero))
        if movimiento is not None:  # Si el movimiento ha sido realizado por una IA.
            self.hacer_movimiento(movimiento)

    def actualizar_tablero(self):
        """Actualiza el tablero de juego.
        """

        # Limpia el viejo tablero. Se requiere de sip para la eliminación inmediata.
        if self.tablero_widget.layout():
            sip.delete(self.tablero_widget.layout())

        # El contenedor del tablero.
        tablero_vbox = QVBoxLayout()

        # Agregue los discos de arriba hacia abajo.
        for i in reversed(range(self.tablero.altura)):
            row_hbox = QHBoxLayout()  # El cotenedor de filas
            row_hbox.addStretch(1)
            for j in range(self.tablero.ancho):  # Por cada columna
                btn = QToolButton()
                btn.setDisabled(True)
                if i < len(self.tablero.tablero[j]):
                    if self.tablero.tablero[j][i]:  # Si pertenece al segundo jugador
                        color = '#F00F0F'
                    else:  # Si pertenece al primer jugador
                        color = '#0F0FF0'
                else:  # Si es un espacio vacío
                    color = 'white'
                btn.setStyleSheet('''
                    QToolButton{
                        height: 32px;
                        width: 32px;
                        border-style: solid;
                        border-color: grey;
                        border-width: 1px;
                        border-radius: 16px;
                        background-color : ''' + color + ''';
                    }
                ''')
                row_hbox.addWidget(btn)
                row_hbox.addStretch(1)
            tablero_vbox.addLayout(row_hbox)
        self.tablero_widget.setLayout(tablero_vbox)

    def actualizar_encabezado(self):
        """Actualiza el encabezado. It is called before each turno.
        """
        is_over = self.tablero.esMeta()
        if is_over == -1:  # If the game continues
            if self.turno is self.jugador1:
                self.encabezado.setText('Turno Jugador 1')
                self.encabezado.setStyleSheet('color: #0F0FF0')
            else:
                self.encabezado.setText('Turno Jugador 2')
                self.encabezado.setStyleSheet('color: #F00F0F')
        elif is_over == 0:  # If it is draw
            self.encabezado.setText('Empate!')
            self.encabezado.setStyleSheet('color: black')
        else:  # If one of the jugadores wins
            if self.turno is self.jugador2:
                self.encabezado.setText('Jugador 1 gana!')
                self.encabezado.setStyleSheet('color: #0F0FF0')
            else:
                self.encabezado.setText('Jugador 2 gana!')
                self.encabezado.setStyleSheet('color: #F00F0F')
        return is_over

    def actualizar_botones(self):
        """Cambia el color de los botones (flechas hacia abajo) después de cada turno.
        """
        color = '#0F0FF0' if self.turno is self.jugador1 else '#F00F0F'
        for btn in self.botones:
            btn.setArrowType(Qt.DownArrow)
            btn.setStyleSheet('''
                QToolButton{
                    height: 30px;
                    width: 30px;
                    color : ''' + color + ''';
                }
            ''')

    def hacer_movimiento(self, movimiento):
        """Deja caer un disco en la columna elegida (movimiento); y actualiza el tablero, el encabezado y los botones en consecuencia.

        Parámetros
        ----------
        movimiento : int
            La columna seleccionada por el jugador o la AI.
        """
        # Si el movimiento es ilegal o el juego terminó, ignore el movimiento.
        if len(self.tablero.tablero[movimiento]) == self.tablero.altura or self.tablero.esMeta() > -1:
            return
        self.tablero.realizarMovimiento(movimiento)
        # Actualizar el turno.
        self.turno = self.jugador2 if self.turno is self.jugador1 else self.jugador1
        self.actualizar_botones()
        self.actualizar_tablero()

        # Próximo movimiento.
        if self.actualizar_encabezado() == -1:
            QTimer.singleShot(10, self.proximo)

    def fijar_iu(self, padre):
        """Inicializa la ventana del juego.

        Parámetros
        ----------
        padre : QWidget
            El objeto de la ventana principal. Se utilizará para enviar una señal al menú principal..

        """
        # El diseǹo principal.
        vbox = QVBoxLayout()
        vbox.addStretch(1)

        # ENCABEZADO
        self.encabezado.setAlignment(Qt.AlignCenter)
        self.encabezado.setFont(QFont('Times', 18))
        vbox.addWidget(self.encabezado)
        self.actualizar_encabezado()

        vbox.addStretch(1)

        # TABLERO
        botones_hbox = QHBoxLayout()
        botones_hbox.addStretch(1)

        for i in range(self.tablero.ancho):
            btn = QToolButton()
            btn.setArrowType(Qt.DownArrow)
            btn.clicked.connect(partial(self.hacer_movimiento, i))
            self.botones.append(btn)
            botones_hbox.addWidget(btn)
        self.actualizar_botones()

        botones_hbox.addStretch(1)
        vbox.addLayout(botones_hbox)

        tablero_hbox = QHBoxLayout()
        tablero_hbox.addStretch(1)
        self.actualizar_tablero()
        tablero_hbox.addWidget(self.tablero_widget)
        tablero_hbox.addStretch(1)
        vbox.addLayout(tablero_hbox)

        vbox.addStretch(1)

        # NUEVO JUEGO
        nuevojuego_hbox = QHBoxLayout()
        nuevojuego_hbox.addStretch(1)
        nuevojuego = QPushButton('Nuevo Juego')
        nuevojuego.clicked.connect(padre.nuevojuego)
        nuevojuego_hbox.addWidget(nuevojuego)
        nuevojuego_hbox.addStretch(1)
        vbox.addLayout(nuevojuego_hbox)
        vbox.addStretch(3)

        self.setLayout(vbox)
