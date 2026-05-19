import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('My cool first GUI')
        self.setGeometry(0, 0, 500, 500)
        self.setWindowIcon(QIcon('/Users/paul/Schach_App/Images/pawn.png'))

        label = QLabel('Hello', self)
        label.setFont(QFont('Arial', 30))
        label.setGeometry(0, 0, 500, 100)
        label.setStyleSheet('color: #03fcd3;' 'background-color: #384d49;')
        label.setAlignment(Qt.AlignCenter)

        label1 = QLabel(self)
        label1.setGeometry(100, 100, 250, 250)
        pixmap = QPixmap('/Users/paul/Schach_App/Images/pawn.png')
        label1.setPixmap(pixmap)
        label1.setScaledContents(True)
        label1.setGeometry((self.width() - label1.width()) //2, (self.height() - label1.height()) //2, label1.width(), label1.height())
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
