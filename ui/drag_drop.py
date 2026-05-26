import sys
import os
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QLabel, QMainWindow, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal
from PyQt5.QtGui import QDrag, QPixmap


class ChessSquare(QPushButton):
    def __init__(self, row, col, piece):
        self.piece = None
        self.row = row 
        self.col = col
        self.setFixedSize(64, 64)

        if (row + col) % 2 == 0:
            self.setStyleSheet('background-color: #d7dbe0;')
        else:
            self.setStyleSheet('background-color: #8c6e5a;')
        

    def set_piece(self, piece):
        self.piece = piece 
        pixmap = QPixmap(f'{piece.name}_{piece.color}' )
        


