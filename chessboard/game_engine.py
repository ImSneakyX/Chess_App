import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chessboard.move import Move_White, Move_Black
from chessboard.board import Board
from chessboard.pieces import Rook, King, Queen, Knight, Bishop, Pawn, Empty
from PyQt5.QtCore import pyqtSignal
import numpy as np

class GameEngine:
    position_update = pyqtSignal(tuple)
    def __init__(self):
        self.white_to_move = True
        self.legal = None
        self.promotion = None
        
        self.mate = None
        self.stalemate = None

        self.brett = Board()
        self.start_pos = self.brett.start_position()
        self.position = self.brett.start_position()

    def check_move(self, start_square, end_square):
        if self.white_to_move == True:
            x = Move_White(self.position, start_square, end_square, self.start_pos) 
            if x.legal == True:
                self.legal = True
            else:
                self.legal = False

            if x.promotion == True:
                self.promotion = True
            else: 
                self.promotion = False

            self.mate = x.mate
            self.stalemate = x.stalemate

        else:
            x = Move_Black(self.position, start_square, end_square, self.start_pos)
            if x.legal == True:
                self.legal = True
            else:
                self.legal = False

            if x.promotion == True:
                self.promotion = True

            else: 
                self.promotion = False

            self.mate = x.mate
            self.stalemate = x.stalemate

        if x.legal == True:
            self.position = x.pos_new
            self.white_to_move = not self.white_to_move
            self.position_update.emit((self.position, self.white_to_move))


    def promote_pawns(self, piece, square_of_promotion):

        self.position[square_of_promotion] = piece


        if self.white_to_move == True:
            start_king = self.find_piece(self.start_boardstate, King, 'w')[0]
            start_rook_l = self.find_piece(self.start_boardstate, Rook, 'w', 'l')[0]
            start_rook_r = self.find_piece(self.start_boardstate, Rook, 'w', 'r')[0]
            self.vision = self.visions_black(self.boardstate)
            for i in range(8):
                for j in range(8):

                    if isinstance(self.boardstate[i, j], Rook):
                        if self.boardstate[i, j].color == 'w' and self.boardstate[i, j].side == 'l':
                            rook_l = self.boardstate[i, j]
                        elif self.boardstate[i, j].color == 'w' and self.boardstate[i, j].side == 'r':
                            rook_r = self.boardstate[i, j]
                    
                    elif isinstance(self.boardstate[i, j], King):
                        if self.boardstate[i, j].color == 'w':
                            king = self.boardstate[i, j]
                        
        else: 
            start_king = self.find_piece(self.start_boardstate, King, 'b')[0]
            start_rook_l = self.find_piece(self.start_boardstate, Rook, 'b', 'l')[0]
            start_rook_r = self.find_piece(self.start_boardstate, Rook, 'b', 'r')[0]
            self.vision = self.visions_white(self.boardstate)
            for i in range(8):
                for j in range(8):

                    if isinstance(self.boardstate[i, j], Rook):
                        if self.boardstate[i, j].color == 'b' and self.boardstate[i, j].side == 'l':
                            rook_l = self.boardstate[i, j]
                        elif self.boardstate[i, j].color == 'b' and self.boardstate[i, j].side == 'r':
                            rook_r = self.boardstate[i, j]

                    elif isinstance(self.boardstate[i, j], King):
                        if self.boardstate[i, j].color == 'b':
                            king = self.boardstate[i, j]

        self.castling(self.boardstate, rook_l.moved, rook_r.moved, king.moved, start_king, start_rook_l, start_rook_r, self.vision)

    def find_piece(self, boardstate, piece, color, side = None):
        square = []
        for row, i in enumerate(boardstate):
            for col, j in enumerate(i):
                if isinstance(boardstate[(row, col)], piece): 
                    if boardstate[(row, col)].color == color:
                        if piece == Rook:
                            if boardstate[(row, col)].side == side:
                                square.append((row, col))
                        else: 
                            square.append((row, col))
        return square
        

            
class MoveGenerator:

    def __init__(self, position):

        self.position = position

    def get_pseudo_legal_moves(self):
        pseudo_moves = []
        if self.position.white_to_move == True:
            for i in range(8):
                for j in range(8):
                    if self.position.boardstate[i, j].color == 'w':
                        moves, moves_vision = self.position.boardstate[i, j].get_legal_moves(self.position.boardstate, (i, j), None)
                        for m in moves: 
                            pseudo_moves.append(((i, j), m))
        
        elif self.position.white_to_move == False:
                for i in range(8):
                    for j in range(8):
                        if self.position.boardstate[i, j].color == 'b':
                            moves, moves_vision = self.position.boardstate[i, j].get_legal_moves(self.position.boardstate, (i, j), None)
                            for m in moves: 
                                pseudo_moves.append(((i, j), m))

        return pseudo_moves
    

    def find_piece(self, boardstate, piece, color, side = None):
        square = []
        for row, i in enumerate(boardstate):
            for col, j in enumerate(i):
                if isinstance(boardstate[(row, col)], piece): 
                    if boardstate[(row, col)].color == color:
                        if piece == Rook:
                            if boardstate[(row, col)].side == side:
                                square.append((row, col))
                        else: 
                            square.append((row, col))
        return square
    
    def visions_black(self, boardstate):
        self.vision_black = np.zeros((8, 8), dtype = 'bool')
        for row, i in enumerate(boardstate):
            for col, j in enumerate(i):
                if boardstate[(row, col)].color == 'b' and isinstance(boardstate[(row, col)], (Knight, Rook, Queen, Bishop)):
                    moves, moves_for_vision = boardstate[(row, col)].get_legal_moves(boardstate, (row, col), None)
                    for x, y in moves: 
                        self.vision_black[(x, y)] = True
                    for x, y in moves_for_vision:
                        self.vision_black[(x, y)] = True
                if boardstate[(row, col)].color == 'b' and isinstance(boardstate[(row, col)], Pawn):
                    if 0 <= col - 1 < 8 and 0 <= row + 1 < 8:
                        self.vision_black[(row + 1, col - 1)] = True
                    if 0 <= col + 1 < 8 and 0 <= row + 1 < 8:
                        self.vision_black[(row + 1, col + 1)] = True
                if boardstate[(row, col)].color == 'b' and isinstance(boardstate[(row, col)], King):
                    offsets = [(1, 1), (1, 0), (1, -1), (0,-1), (-1,-1), (-1,0), (-1,1), (0, 1)]
                    for x, y in offsets:
                        new_row, new_col = row + x, col + y
                        if 0 <= new_row <8 and 0 <= new_col <8:
                            self.vision_black[(new_row, new_col)] = True
        return self.vision_black
    
    def visions_white(self, boardstate):
        self.vision_white = np.zeros((8, 8), dtype = 'bool')
        for row, i in enumerate(boardstate):
            for col, j in enumerate(i):
                if boardstate[(row, col)].color == 'w' and isinstance(boardstate[(row, col)], (Rook, Knight, Bishop, Queen)):
                    moves, moves_for_vision = boardstate[(row, col)].get_legal_moves(boardstate, (row, col), None)
                    for x, y in moves: 
                        self.vision_white[(x, y)] = True
                    for x, y in moves_for_vision:
                        self.vision_white[(x, y)] = True
                if boardstate[(row, col)].color == 'w' and isinstance(boardstate[(row, col)], Pawn):
                    if 0 <= col - 1 < 8 and 0 <= row - 1 < 8:
                        self.vision_white[(row - 1, col - 1)] = True
                    if 0 <= col + 1 < 8 and 0 <= row - 1 < 8:
                        self.vision_white[(row - 1, col + 1)] = True
                if boardstate[(row, col)].color == 'w' and isinstance(boardstate[(row, col)], King):
                    offsets = [(1, 1), (1, 0), (1, -1), (0,-1), (-1,-1), (-1,0), (-1,1), (0, 1)]
                    for x, y in offsets:
                        new_row, new_col = row + x, col + y
                        if 0 <= new_row <8 and 0 <= new_col <8:
                            self.vision_white[(new_row, new_col)] = True
        return self.vision_white
    
    def generate_legal_moves(self):
        if self.position.white_to_move == True:
            moves = self.get_pseudo_legal_moves(self.position)
            for move in moves:
                child = self.position.make_move(move)
                king_pos = self.find_piece(child.boardstate, King, 'w')[0]
                self.visions_black(child.boardstate)
                if self.vision_black[king_pos] == False:
                    self.legal = True 

                else:
                    self.legal = False

        if self.position.white_to_move == False:
            moves = self.get_pseudo_legal_moves(self.position)
            for move in moves:
                child = self.position.make_move(move)
                king_pos = self.find_piece(child.boardstate, King, 'b')[0]
                self.visions_black(child.boardstate)
                if self.vision_black[king_pos] == False:
                    self.legal = True 

                else:
                    self.legal = False
                        


                    