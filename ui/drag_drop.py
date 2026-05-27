import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QLabel, QMainWindow, QVBoxLayout, QPushButton, QGridLayout
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal, QSize
from PyQt5.QtGui import QDrag, QPixmap, QIcon
from chessboard.pieces import Pawn, Bishop, Knight, Queen, King, Rook
from chessboard.board import Board


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('test')
        self.setGeometry(750, 450, 300, 300)
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        #Game Logic
        self.brett = Board()
        self.start_pos = self.brett.start_position()

        grid = QGridLayout()
        grid.setSpacing(0)

        for i in range(8):
            for j in range(8):
                button = ChessSquare(i, j, self.start_pos[i, j])
                grid.addWidget(button)


        centralWidget.setLayout(grid)
        self.setAcceptDrops(True)
    
    def dragEnterEvent(self, e):
        e.accept()



class ChessSquare(QPushButton):
    def __init__(self, row, col, piece = None):
        super().__init__()
        self.piece = piece
        self.row = row 
        self.col = col
        self.label = QLabel()
        self.setFixedSize(64, 64)
        self.setIconSize(QSize(48, 48))

        if (row + col) % 2 == 0:
            self.setStyleSheet('background-color: #d7dbe0;')
        else:
            self.setStyleSheet('background-color: #8c6e5a;')

        self.set_piece()

        

    def set_piece(self):
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon = QIcon(os.path.join(base_path, 'Images', f'{self.piece.name}_{self.piece.color}.png'))
        self.setIcon(icon)

    def MouseMoveEvent(self, e):
        if e.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)
            drag.exec_(Qt.MoveAction)

        
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


        




