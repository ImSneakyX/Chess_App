import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QDialog
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPen, QPainter
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QPoint
from chessboard.board import Board
from chessboard.move import Move_White, Move_Black
from drag_drop import ChessSquare
from chessboard.game_engine import GameEngine
from ui.board_gui import ChessBoard
from ui.dialogs import Promote, DialogWinMate, DialogLoseMate, DialogRemisPatt
import time


class Launcher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Launcher')
        self.setGeometry(750, 450, 300, 300)
        self.game_launcher()

    def game_launcher(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        button1 = QPushButton('Freies-Spiel starten', self)
        button1.setMinimumHeight(100)
        button2 = QPushButton('Spiel gegen Computer starten', self)
        button2.setMinimumHeight(100)
        button3 = QPushButton('Eröffnungsdatenbank', self)
        button3.setMinimumHeight(100)

        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)
        button1.clicked.connect(self.game)
        central_widget.setLayout(layout)

    def game(self):
        self.window = ChessGame()
        self.window.show()
        self.hide()

class ChessGame(QMainWindow):
    def __init__(self):
        super().__init__()
                
        self.setWindowTitle('Schach')
        self.setGeometry(750, 450, 500, 500)
        centralWidget = ChessBoard()
        self.setCentralWidget(centralWidget)






        




def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    window = Launcher()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
