import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QDialog
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPen, QPainter, QPolygon
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QPoint
from chessboard.board import Board
from chessboard.move import Move_White, Move_Black
from drag_drop import ChessSquare
from chessboard.game_engine import GameEngine
from ui.dialogs import Promote, DialogWinMate, DialogLoseMate, DialogRemisPatt
import time


class ChessBoard(QWidget):
    
    arrow_signal = pyqtSignal(list)
    def __init__(self, parent = None):
        super().__init__(parent)

        self.engine = GameEngine()

        self.brett = Board()
        self.start_pos = self.brett.start_position()

        self.grid = QGridLayout()
        self.grid.setSpacing(0)
        self.grid.setContentsMargins(0, 0, 0, 0)

        self.squares = {}
        self.arrows = []

        for i in range(8):
            for j in range(8):
                button = ChessSquare(i, j, self.start_pos[i, j], self)
                button.move_made.connect(self.process_move)
                button.clear_highlight.connect(self.clear)
                button.arrows_signal.connect(self.get_arrows)
                self.grid.addWidget(button, i, j)
                self.squares[(i, j)] = button


        self.setLayout(self.grid)


    def clear(self):

        for sq in self.squares.values():
            sq.setProperty('highlight', False)
            sq.style().unpolish(sq)
            sq.style().polish(sq)
            

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

        if self.engine.mate == True:
            if self.engine.white_to_move == True:
                mate_dialog_win = DialogWinMate(self)
                QTimer.singleShot(1500, lambda: mate_dialog_win.exec_())
            else:
                mate_dialog_lose = DialogLoseMate(self)
                QTimer.singleShot(1500, lambda: mate_dialog_lose.exec_())


        if self.engine.stalemate == True:
            dialog_stalemate = DialogRemisPatt(self)
            QTimer.singleShot(1500, lambda: dialog_stalemate.exec_())
            


        
            

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

    def get_arrows(self, arrows):

        self.arrows = arrows
        self.arrow_signal.emit(self.arrows)



    
    
class ArrowOverlay(QWidget):
    def __init__(self, arrows, square_size, parent = None):
        super().__init__(parent)

        self.arrows = arrows
        self.square_size = square_size
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

    def paintEvent(self, event):
        super().paintEvent(event)

        pen = QPen(Qt.yellow)
        pen.setWidth(5)
        painter = QPainter(self)
        painter.setPen(pen)

        
    

        for start, end in self.arrows:
            self.draw_arrow(start, end, painter)

    def draw_arrow(self, start_square, end_square, painter):

        p1 = self.get_center(start_square)
        p2 = self.get_center(end_square)
        p3 = self.get_corners()
        p4 = self.get_corners()
        p5 = self.get_corners()
        painter.drawLine(p1, p2)

        corners = [p2, p3, p4]
        tip = QPolygon(corners)
        painter.drawPolygon(tip)


    def get_center(self, square):
        
        row, col = square

        x = col * self.square_size.width() + self.square_size.width() // 2
        y = row * self.square_size.height() + self.square_size.height() // 2

        return QPoint(x, y)
    
    def get_corners():
        pass