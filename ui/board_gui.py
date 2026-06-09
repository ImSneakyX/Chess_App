import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QDialog
from PyQt5.QtGui import QPen, QPainter, QPolygon, QBrush, QColor
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QPoint
from chessboard.board import Board
from drag_drop import ChessSquare
from chessboard.game_engine import GameEngine
from ui.dialogs import Promote, DialogWinMate, DialogLoseMate, DialogRemisPatt
import time
from math import sin, cos, pi, atan2


class ChessBoard(QWidget):
    
    arrow_signal = pyqtSignal(list)
    delete_signal = pyqtSignal()
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

        self.delete_signal.emit()
            

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
    def __init__(self, arrows, parent = None):
        super().__init__(parent)

        self.arrows = arrows
        self.square_size = self.parent().width()/8
        self.setAttribute(Qt.WA_TransparentForMouseEvents)



    def paintEvent(self, event):
        super().paintEvent(event)
        self.square_size = self.parent().width()/8

        brush = QBrush(QColor('#326e42'))
        painter = QPainter(self)
        painter.setBrush(brush)
        painter.setRenderHint(QPainter.Antialiasing)
    

        for start, end in self.arrows:
            self.draw_arrow(start, end, painter)

    def draw_arrow(self, start_square, end_square, painter):

        p1 = self.get_center(start_square)
        p2 = self.get_center(end_square)

        dy = p1.y() - p2.y()
        dx = p1.x() -p2.x()
        angle = atan2(dy, dx)

        p3 = self.get_corners(p2, angle, self.square_size / 2, -pi/8)
        p4 = self.get_corners(p2, angle, self.square_size / 4, 0)
        p5 = self.get_corners(p2, angle, self.square_size / 2, pi/8)



        p2_modified = QPoint(int(p2.x() + (self.square_size / 4) * cos(angle)), int(p2.y() + (self.square_size / 4) * sin(angle)))

        pen_line = QPen(QColor('#326e42'))
        pen_line.setWidth(6)
        painter.setPen(pen_line)

        painter.drawLine(p1, p2_modified)

        corners = [p2, p3, p4, p5]
        tip = QPolygon(corners)

        pen_tip = QPen(QColor('#326e42'))
        pen_tip.setWidth(2)
        painter.setPen(pen_tip)

        painter.drawPolygon(tip)


    def get_center(self, square):
        
        row, col = square

        x = col * self.square_size + self.square_size // 2
        y = row * self.square_size + self.square_size // 2

        return QPoint(int(x), int(y))
    
    def get_corners(self, end_point, angle, radius, phase_shift):
    

        return QPoint(int(end_point.x() + radius * cos(angle + phase_shift)), int(end_point.y() + radius * sin(angle + phase_shift)))