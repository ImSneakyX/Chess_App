import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QDialog
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal
from chessboard.board import Board
from chessboard.move import Move_White, Move_Black
from drag_drop import ChessSquare
from chessboard.game_engine import GameEngine
from ui.dialogs import Promote
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
        self.engine = GameEngine()
                
        self.setWindowTitle('Schach')
        self.setGeometry(750, 450, 300, 300)
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        self.brett = Board()
        self.start_pos = self.brett.start_position()

        self.grid = QGridLayout()
        self.grid.setSpacing(0)

        self.squares = {}

        for i in range(8):
            for j in range(8):
                button = ChessSquare(i, j, self.start_pos[i, j])
                button.move_made.connect(self.process_move)
                self.grid.addWidget(button, i, j)
                self.squares[(i, j)] = button


        centralWidget.setLayout(self.grid)



    def process_move(self, start_square, end_square, color):
        self.end_square = end_square

        t1 = time.time()

        self.engine.check_move(start_square, end_square)
        if self.engine.legal == True and self.engine.promotion == False:
            self.update_board()

        t2 = time.time()

        if self.engine.legal == True and self.engine.promotion == True:
            promote_dialog = Promote(color, self)

            promote_dialog.selected_piece.connect(self.process_promotion)
            
            promote_dialog.exec_()

        print(f'GUI Update: {t2-t1:.5f} sek')
            

    def process_promotion(self, object):
        self.engine.promote_pawns(object, self.end_square)
        self.update_board()


    def update_board(self):
        for i in range(8):
            for j in range(8):

                neue_figur = self.engine.position[(i,j)]
                alte_figur = self.squares[(i,j)].piece

                if alte_figur != neue_figur:
                    self.squares[(i,j)].piece = self.engine.position[(i,j)]
                    self.squares[(i,j)].set_piece()




        




def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    window = Launcher()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
