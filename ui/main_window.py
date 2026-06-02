import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QDialog
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt
from chessboard.board import Board
from chessboard.move import Move_White, Move_Black
from drag_drop import ChessSquare


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
        self.setGeometry(750, 450, 300, 300)
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        self.brett = Board()
        self.start_pos = self.brett.start_position()

        self.grid = QGridLayout()
        self.grid.setSpacing(0)

        for i in range(8):
            for j in range(8):
                button = ChessSquare(i, j, self.start_pos[i, j])
                self.grid.addWidget(button, i, j)


        centralWidget.setLayout(self.grid)

    def start_game(self):
        while self.game == 0:
            self.make_move_white()
            if self.game == 0:
                self.make_move_black()
            else: 
                break
    def make_move_white(self):

        x = Move_White(self.position, start_square, end_square, self.start_pos)
        if x.mate == True:
            print('Schachmatt, Weiß gewinnt!')
            self.game = 1
            return self.game
        if x.stalemate == True:
            print('Patt!')
            self.game = 1
            return self.game
        if x.legal == True:
            self.position = x.pos_new #wird wieder zu Brett umgewandelt
        else: 
            self.make_move_white()

    def make_move_black(self):
        start_square = input(f'Black, make a move! Select the square with the piece that you want to move: ')
        end_square = input(f'and select the square you want to put the piece on: ')
        for row, i in enumerate(self.brett.notation):
            for col, j in enumerate(i):
                if  self.brett.notation[row, col] == start_square:
                        start_square = tuple((row, col))
                if  self.brett.notation[row, col] == end_square:
                        end_square = tuple((row, col))

        if isinstance(start_square, str):
            if isinstance(end_square, str):
                print(f"Both selected squares don't exist! Please select exisitng squares")
                return self.make_move_black()
            else:
                print(f"Selected start square doesn't exist! Please select an exisiting square")
                return self.make_move_black()
        if isinstance(end_square, str) and not isinstance(start_square, str):
            print(f"Selected end square doesn't exist! Please select an exisitng square")
            return self.make_move_black()


        x = Move_Black(self.position, start_square, end_square, self.start_pos)
        if x.mate == True:
            print('Schachmatt, Schwarz gewinnt!')
            self.game = 1
            return self.game
        if x.stalemate == True:
            print('Patt!')
            self.game = 1
            return self.game
        if x.legal == True:
             self.position = x.pos_new
             self.vision = x.vision
        else:
             self.make_move_black()

    def show_mate(self):
        d = QDialog()
        b1 = QPushButton('Erneut spielen', d)



        d.exec_()

        




def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    window = Launcher()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
