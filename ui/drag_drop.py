import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QLabel, QMainWindow, QVBoxLayout, QPushButton, QGridLayout
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal, QSize, QPoint
from PyQt5.QtGui import QDrag, QPixmap, QIcon, QPainter, QPen
from chessboard.board import Board
from chessboard.move import Move_White, Move_Black


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('test')
        self.setGeometry(750, 450, 300, 300)
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        self.brett = Board()
        self.start_pos = self.brett.start_position()
        self.boardstate = self.start_pos

        self.grid = QGridLayout()
        self.grid.setSpacing(0)

        for i in range(8):
            for j in range(8):
                button = ChessSquare(i, j, self.start_pos[i, j])
                self.grid.addWidget(button, i, j)


        centralWidget.setLayout(self.grid)
        




class ChessSquare(QPushButton):
    move_made = pyqtSignal(tuple, tuple, str)
    clear_highlight = pyqtSignal()
    def __init__(self, row, col, piece = None, parent = None):
        super().__init__(parent)
        self.piece = piece
        self.row = row 
        self.col = col
        self.square = (row, col)

        self.start_right_click = None
        self.arrows = []
 
        self.setFixedSize(64, 64)
        self.setIconSize(QSize(60, 60))
        self.setAcceptDrops(True)
        self.setFlat(True)
        self.setFocusPolicy(Qt.NoFocus)
   

        if (row + col) % 2 == 0:
            self.setStyleSheet('''ChessSquare {background-color: #d7dbe0; border: none;}
                               
                               ChessSquare[highlight='true'] {background: #bd4242;}
                               ''')
        else:
            self.setStyleSheet('''ChessSquare {background-color: #8c6e5a; border: none;}
                               ChessSquare[highlight='true'] {background: #bf2c2c;}
                               ''')
        self.set_piece()

        

    def set_piece(self):
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if self.piece is None or self.piece.value == 0:
            self.setIcon(QIcon())
            return
        image_path = os.path.join(base_path, 'Images', f'{self.piece.name}_{self.piece.color}.png')
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(120, 120, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        pixmap.setDevicePixelRatio(2.0)
        icon = QIcon(pixmap)
        self.setIcon(icon)



    def mousePressEvent(self, e):


        if e.button() == Qt.LeftButton:
            self.clear_highlight.emit()
 
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
                self.set_piece()
    


    def mouseReleaseEvent(self, e):
        widget = QApplication.widgetAt(e.globalPos())
        if e.button() == Qt.RightButton:
            if self.square == widget.square:
                self.setProperty('highlight', True)
                self.style().unpolish(self)
                self.style().polish(self)

            else:
                self.arrows.append((self.square, widget.square))
                self.update()


        
    def paintEvent(self, event):
        super().paintEvent(event)

        pen = QPen()
        pen.setWidth(5)
        painter = QPainter(self)
        painter.setPen(pen)

        for start, end in self.arrows:
            self.draw_arrow(start, end, painter)




    def draw_arrow(self, start_square, end_square, painter):

        p1 = self.get_center(start_square)
        p2 = self.get_center(end_square)
        print('it works')

        print(p1, p2)

        painter.drawLine(p1, p2)

    def get_center(self, square):
        
        row, col = square

        x = row * self.width() + self.width() // 2
        y = col * self.height() + self.height() // 2

        return QPoint(x, y)


        



    def dragEnterEvent(self, e):  
        e.accept()



    def dropEvent(self, e):

        source_widget = e.source()
        self.move_made.emit(source_widget.square, self.square, source_widget.piece.color)

        e.accept()


        
    
if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


        




