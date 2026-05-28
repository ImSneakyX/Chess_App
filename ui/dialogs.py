import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QDialog
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('test')
        self.setGeometry(750, 450, 300, 300)
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        button1 = QPushButton('Mate')
        button2 = QPushButton('Stalemate')
        layout = QHBoxLayout()
        layout.addWidget(button1)
        layout.addWidget(button2)
        centralWidget.setLayout(layout)
        button1.clicked.connect(self.show_dialog)
        button2.clicked.connect(self.show_dialog)


    def show_dialog(self):
        d = Dialog_Mate(self)
        d.exec_()

class Dialog_Mate(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(400, 400)
        self.setStyleSheet('background-color: #3d3c39; border-radius: 20px;')

        label_top = QLabel(self)
        label_top.setStyleSheet('background-color: #696762;')
        label_top.setGeometry(0, 0, 400, 100)

        self.button1 = QPushButton('ok', self)
        self.button1.move(140, 160)

        label_trophy = QLabel(label_top)
        label_trophy.setGeometry(20, 20, 60, 60)
        pixmap = QPixmap(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Images', 'trophy.png'))
        pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label_trophy.setPixmap(pixmap)

        


        





if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())