import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt
from chessboard.board import Board


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Schach-App')
        self.setGeometry(750, 450, 300, 300)
        self.buttons = {}

        #Game Logic
        self.brett = Board()
        self.start_pos = self.brett.start_position()

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
        button1.clicked.connect(self.initUI)
        central_widget.setLayout(layout)



    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        grid = QGridLayout()
        grid.setSpacing(0)

        for i in range(8):
            for j in range(8):
                button = QPushButton()
                button.setFixedSize(64, 64)
                if (i + j) % 2 == 0:
                    button.setStyleSheet('background-color: #d7dbe0;')
                else: 
                    button.setStyleSheet('background-color: #8c6e5a;')
                button.clicked.connect(lambda _, row = i, col = j: self.button_clicked(row, col))
                self.buttons[(i, j)] = button
                grid.addWidget(button, i, j)

        central_widget.setLayout(grid)
        
        
    def button_clicked(self, row, col):

        print(f'Das ist das Feld ({row}, {col})')



def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
