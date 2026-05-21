import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Schach')
        self.setGeometry(1200, 650, 100, 100)
        self.initUI()

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
                    button.setStyleSheet('background-color: #c282b4;')
                
                grid.addWidget(button, i, j)

        central_widget.setLayout(grid)
        



def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
