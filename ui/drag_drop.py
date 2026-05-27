import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QLabel, QMainWindow, QVBoxLayout, QPushButton, QGridLayout
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal, QSize
from PyQt5.QtGui import QDrag, QPixmap, QIcon
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

        self.grid = QGridLayout()
        self.grid.setSpacing(0)

        for i in range(8):
            for j in range(8):
                button = ChessSquare(i, j, self.start_pos[i, j])
                self.grid.addWidget(button, i, j)


        centralWidget.setLayout(self.grid)




class ChessSquare(QPushButton):
    def __init__(self, row, col, piece = None):
        super().__init__()
        self.piece = piece
        self.row = row 
        self.col = col
        self.label = QLabel()
        self.setFixedSize(64, 64)
        self.setIconSize(QSize(60, 60))
        self.setAcceptDrops(True)
   

        if (row + col) % 2 == 0:
            self.setStyleSheet('background-color: #d7dbe0; border: none;')
        else:
            self.setStyleSheet('background-color: #8c6e5a; border: none;')

        self.set_piece()

        

    def set_piece(self):
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if self.piece is None or self.piece.value == 0:
            self.setIcon(QIcon())
            return
        image_path = os.path.join(base_path, 'Images', f'{self.piece.name}_{self.piece.color}.png')
        icon = QIcon(image_path)
        self.setIcon(icon)

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.LeftButton:
            if self.piece is not None and self.piece.value != 0:
                base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                drag = QDrag(self)
                mime = QMimeData()
                drag.setMimeData(mime)

                image_path = os.path.join(base_path, 'Images', f'{self.piece.name}_{self.piece.color}.png')
                pixmap = QPixmap(image_path)

                pixmap = pixmap.scaled(120, 120, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
                pixmap.setDevicePixelRatio(2.0)

                drag.setPixmap(pixmap)
                drag.setHotSpot(e.pos())

                self.setIcon(QIcon())



                drag.exec_(Qt.MoveAction)

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):

        source_widget = e.source()
        self.piece = source_widget.piece
        source_widget.piece = None
        self.set_piece()



        e.accept()


        
    
if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


        




