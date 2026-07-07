import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QDialog, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QPen, QPainter, QPolygon, QBrush, QColor
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QPoint
from chessboard.board import Board
from drag_drop import ChessSquare
from chessboard.game_engine import GameEngine
from ui.dialogs import Promote, DialogWinMate, DialogLoseMate, DialogRemisPatt
import time
from math import sin, cos, pi, atan2


class ChessBoard(QWidget):

    move_signal = pyqtSignal(object)
    arrow_signal = pyqtSignal(list)
    delete_signal = pyqtSignal()
    table_signal = pyqtSignal(object, object, list, bool, bool, bool, bool, bool, str)
    def __init__(self, engine, parent = None):
        super().__init__(parent)

        self.engine = engine

        self.brett = Board()
        self.start_pos = self.brett.start_position()

        self.grid = QGridLayout()
        self.grid.setSpacing(0)
        self.grid.setContentsMargins(0, 0, 0, 0)

        self.squares = {}
        self.arrows = []
        self.last_start = None
        self.last_end = None

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
            

    def process_move(self, move):
        t1 = time.time()
        self.end_square = move.end_square
        self.engine.check_move(move)

        if self.engine.legal == True and self.engine.promotion == False:
            self.update_board(move)
            


        elif self.engine.legal == True and self.engine.promotion == True:

            promote_dialog = Promote(self.engine.position.boardstate[move.end_square].color, self.width() // 8, self)

            promote_dialog.selected_piece.connect(lambda promotion_piece: self.process_promotion(promotion_piece, move))
            local_point = QPoint(0, 0)
            global_pos = self.squares[move.end_square].mapToGlobal(local_point)
            if self.engine.position.boardstate[move.end_square].color == 'w':

                promote_dialog.move(global_pos.x(), global_pos.y())
            else:
                promote_dialog.move(global_pos.x(), global_pos.y() - 3 * (self.height() // 8))
            promote_dialog.exec_()
            


        t2 = time.time()

        print(f'GUI Update: {t2 - t1:.5f} sek')




    def update_board(self, move, promotion_piece = None):
        for i in range(8):
            for j in range(8):
                neue_figur = self.engine.position.boardstate[(i,j)]
                alte_figur = self.squares[(i,j)].piece

                if alte_figur.color != neue_figur.color:
                    self.squares[(i,j)].piece = self.engine.position.boardstate[(i,j)]
                    self.squares[(i,j)].set_piece()

        if self.last_start:
            self.squares[self.last_start].setProperty('highlight_last_move', False)
            self.squares[self.last_start].style().unpolish(self.squares[self.last_start])
            self.squares[self.last_start].style().polish(self.squares[self.last_start])
        if self.last_end:
            self.squares[self.last_end].setProperty('highlight_last_move', False)
            self.squares[self.last_end].style().unpolish(self.squares[self.last_end])
            self.squares[self.last_end].style().polish(self.squares[self.last_end])
        

        self.squares[move.start_square].setProperty('highlight_last_move', True)
        self.squares[move.end_square].setProperty('highlight_last_move', True)

        self.squares[move.start_square].style().unpolish(self.squares[move.start_square])
        self.squares[move.start_square].style().polish(self.squares[move.start_square])

        self.squares[move.end_square].style().unpolish(self.squares[move.end_square])
        self.squares[move.end_square].style().polish(self.squares[move.end_square])

        self.last_start = move.start_square
        self.last_end = move.end_square

        if move.promotion_piece:
            promotion_piece_signal = move.promotion_piece
        else:
            promotion_piece_signal = promotion_piece


        piece_moved = self.engine.position.boardstate[move.end_square]
        self.table_signal.emit(move, piece_moved, self.engine.disambiguation(piece_moved, move.end_square), self.engine.capture, self.engine.check, self.engine.castle_short, 
            self.engine.castle_long, self.engine.mate, promotion_piece_signal)

        if self.engine.mate == False and self.engine.stalemate == False:
            self.move_signal.emit(self.engine.position)



    def process_promotion(self, promotion_piece, move):
        self.engine.promote_pawns(promotion_piece, self.end_square)
        self.engine.check_for_mate()
        self.update_board(move, promotion_piece)



    def board_reset(self):
        for i in range(8):
            for j in range(8):
                neue_figur = self.engine.position.boardstate[(i,j)]
                alte_figur = self.squares[(i,j)].piece

                if alte_figur != neue_figur:
                    self.squares[(i,j)].piece = self.engine.position.boardstate[(i,j)]
                    self.squares[(i,j)].set_piece()
                    
        if self.last_start:
            self.squares[self.last_start].setProperty('highlight_last_move', False)
            self.squares[self.last_start].style().unpolish(self.squares[self.last_start])
            self.squares[self.last_start].style().polish(self.squares[self.last_start])
        if self.last_end:
            self.squares[self.last_end].setProperty('highlight_last_move', False)
            self.squares[self.last_end].style().unpolish(self.squares[self.last_end])
            self.squares[self.last_end].style().polish(self.squares[self.last_end])

        self.move_signal.emit(self.engine.position)





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
    

class EvalBar(QWidget):

    def __init__(self, width, height, parent = None):
        super().__init__(parent)
        
        self.width = width
        self.height = height
        self.eval = 0



    def setEval(self, value):
        self.eval = value
        self.update()



    def paintEvent(self, event):
        
        h = int(self.height // 2 - self.eval * self.height // 8)
        painter = QPainter(self)
        font = painter.font()
        font.setPixelSize(max(10, self.height // 45))
        painter.setFont(font)
        painter.fillRect(0, 0, self.width, h, QColor('black'))
        painter.fillRect(0, h, self.width, self.height-h, QColor('white'))
        if self.eval >= 0:
            painter.setPen(QColor('black'))
            painter.drawText(0, 11 * self.height // 12, self.width, self.height // 12, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom, str(self.eval))
        else:
            painter.setPen(QColor('white'))
            painter.drawText(0, 0, self.width, self.height // 12, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop, str(self.eval))



            

class MoveTable(QTableWidget):

    def __init__(self, moves, parent = None):
        super().__init__(parent)

        self.moves = moves

        self.setStyleSheet(''' MoveTable {background-color: #f0f2f0;} ''')
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(['White', 'Black'])
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        rows = (len(self.moves) + 1) // 2
        self.setRowCount(rows)

        for i in range(rows):

            white = 2*i
            black = 2*i + 1

            if white < len(self.moves):
                self.setItem(i, 0, QTableWidgetItem(self.moves[white]))

            if black < len(self.moves):
                self.setItem(i, 1, QTableWidgetItem(self.moves[black]))

        self.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):

        pass


    def add_move(self, move, piece_moved, disambiguation, capture, check, castling_short, castling_long, mate, promotion_piece):

        new_move = self.move_to_san(move, piece_moved, disambiguation, capture, check, castling_short, castling_long, mate, promotion_piece)
        self.moves.append(new_move)

        index = len(self.moves) - 1
        row = index // 2
        if row >= self.rowCount():
            self.insertRow(row)

        column = index % 2
        self.setItem(row, column, QTableWidgetItem(new_move))

    def move_to_san(self, move, piece_moved, disambiguation, capture, check, castling_short, castling_long, mate, promotion_piece):

        notation = [[0]*8 for _ in range(8)]

        rows = '12345678'
        cols = 'abcdefgh'
        row_start = move.start_square[0]
        col_start = move.start_square[1]

        for row in range(8):
            for col in range(8):
                notation[row][col] = f'{cols[col]}{rows[7-row]}'

        if castling_short:
            san_move = '0-0'
        elif castling_long:
            san_move = '0-0-0'

        else: 
  
            if len(disambiguation) <= 1:
                disambiguation_string = ''
            elif len(disambiguation) > 1:
                for r, c in disambiguation:
                    same_row = ''
                    same_col = ''
                    if move.start_square != (r, c):
                        print(r, row_start)
                        if row_start == r:
                            same_row = notation[row_start][0]
                            same_row = same_row[0]
                            
                            print('2')
                        elif col_start == c:
                            same_col = notation[0][col_start]
                            same_col = same_col[1]

                            print('3')

                    disambiguation_string = f'{same_row}{same_col}'

            if capture:
                capture_string = 'x'
            else:
                capture_string = ''

            if piece_moved.name == 'Pawn' and capture:
                pawn_origin = notation[row_start][col_start]
                piece_letter = f'{pawn_origin[0]}'
            elif piece_moved.name == 'Pawn':
                piece_letter = ''
            elif piece_moved.name == 'Knight':
                piece_letter = 'N'
            elif piece_moved.name == 'Bishop':
                piece_letter = 'B'
            elif piece_moved.name == 'Rook':
                piece_letter = 'R'
            elif piece_moved.name == 'Queen':
                piece_letter = 'Q'
            elif piece_moved.name == 'King':
                piece_letter = 'K'

            if promotion_piece:
                promotion_string = f'={promotion_piece}'
                if capture:
                    pawn_origin = notation[row_start][col_start]
                    piece_letter = f'{pawn_origin[0]}'
                else:
                    piece_letter = ''

            else: 
                promotion_string = ''
            if check and not mate:
                check_string = '+'
            else: 
                check_string = ''
 
            san_move = ''.join((piece_letter, disambiguation_string, capture_string, notation[move.end_square[0]][move.end_square[1]], promotion_string, check_string))

        if mate:
            mate_string = '#'
        else:
            mate_string = ''
        san_move = ''.join((san_move, mate_string))

        return san_move
    
  

    
        