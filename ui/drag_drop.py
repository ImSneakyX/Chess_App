import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QLabel, QMainWindow, QVBoxLayout, QPushButton, QGridLayout, QSizePolicy
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal, QSize, QPoint
from PyQt5.QtGui import QDrag, QPixmap, QIcon, QPainter, QPen
from chessboard.board import Board
from chess_engine.new_move import Move


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
    move_made = pyqtSignal(object)
    clear_highlight = pyqtSignal()
    arrows_signal = pyqtSignal(list)
    def __init__(self, row, col, piece = None, parent = None):
        super().__init__(parent)
        self.piece = piece
        self.row = row 
        self.col = col
        self.square = (row, col)
        

        self.start_right_click = None
        self.arrows = []
        
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setIconSize(QSize(int(self.width() * (15/16)), int(self.height() * (15/16))))
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

                pixmap = pixmap.scaled(2 * self.iconSize().width(), 2 * self.iconSize().width(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
                pixmap.setDevicePixelRatio(2.0)

                drag.setPixmap(pixmap)
                drag.setHotSpot(e.pos())

                self.setIcon(QIcon())



                drag.exec_(Qt.MoveAction)
                self.set_piece()
    


    def mouseReleaseEvent(self, e):
        widget = QApplication.widgetAt(e.globalPos())
        if e.button() == Qt.RightButton:
            if isinstance(widget, ChessSquare):
                if self.square == widget.square:
                    self.setProperty('highlight', True)
                    self.style().unpolish(self)
                    self.style().polish(self)

                else:
                    self.arrows.append((self.square, widget.square))
                    self.arrows_signal.emit(self.arrows)
                    self.arrows.clear()

    def dragEnterEvent(self, e):  
        e.accept()



    def dropEvent(self, e):

        source_widget = e.source()
        move = Move(source_widget.square, self.square)
        self.move_made.emit(move)

        e.accept()

    def resizeEvent(self, e):

        super().resizeEvent(e)

        side = min(self.width(), self.height())
        self.setIconSize(QSize(int(side * (15/16)), int(side * (15/16))))

        
    
if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


        




