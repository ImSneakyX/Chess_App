import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chessboard.move import Move_White, Move_Black
from chessboard.board import Board
from chessboard.new_pieces import Rook, King, Queen, Knight, Bishop, Pawn, Empty
from PyQt5.QtCore import pyqtSignal
import numpy as np

class GameEngine:
    position_update = pyqtSignal(object)
    def __init__(self, position):

        self.position = position
        self.legal = None
        self.promotion = None
        
        self.mate = None
        self.stalemate = None
        self.board = Board()
        self.start_pos = self.board.start_position()



    def check_move(self, start_square, end_square):
        if self.position.white_to_move == True:
            x = Move_White(self.position.boardstate, start_square, end_square, self.start_pos) 
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
            x = Move_Black(self.position.boardstate, start_square, end_square, self.start_pos)
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
            self.position.boardstate = x.pos_new
            self.position.white_to_move = not self.position.white_to_move
            self.position_update.emit(self.position)


    def promote_pawns(self, piece, square_of_promotion):

        self.position[square_of_promotion] = piece


        
        

            
class MoveGenerator:

    def __init__(self, position):

        self.position = position

    def get_pseudo_legal_moves(self):
        pseudo_moves = []
        if self.position.white_to_move == True:
            for i in range(8):
                for j in range(8):
                    if self.position.boardstate[i, j].color == 'w':
                        if not isinstance(self.position.boardstate[i, j], King):
                            moves, moves_vision = self.position.boardstate[i, j].get_legal_moves(self.position.boardstate, (i, j))
                            for m in moves: 
                                pseudo_moves.append(((i, j), m))
                        else:
                            if self.position.white_castle_g:
                                    self.visions_black(self.position.boardstate)
                                    if all(isinstance(square, Empty) for square in self.position.boardstate[7, 5:7]) == True and self.vision_black[7, 4:7].any() == False:
                                        white_castling_g = True

                                    else:
                                        white_castling_g = False
                            

                            if self.position.white_castle_c:
                                    self.visions_black(self.position.boardstate)
                                    if all(isinstance(square, Empty) for square in self.position.boardstate[7, 1:4]) == True and self.vision_black[7, 2:5].any() == False:
                                        white_castling_c = True
                                    else:
                                        white_castling_c = False

                            moves, moves_vision = self.position.boardstate[i, j].get_legal_moves(self.position.boardstate, (i, j), white_castling_c, white_castling_g)
                            for m in moves: 
                                pseudo_moves.append(((i, j), m))

        
        elif self.position.white_to_move == False:
                for i in range(8):
                    for j in range(8):
                        if self.position.boardstate[i, j].color == 'b':
                            if not isinstance(self.position.boardstate[i, j], King):
                                moves, moves_vision = self.position.boardstate[i, j].get_legal_moves(self.position.boardstate, (i, j))
                                for m in moves: 
                                    pseudo_moves.append(((i, j), m))
                            else:
                                if self.position.black_castle_g:
                                    self.visions_white(self.position.boardstate)
                                    if all(isinstance(square, Empty) for square in self.position.boardstate[0, 5:7]) == True and self.vision_white[0, 4:7].any() == False:
                                        black_castling_g = True

                                    else:
                                        black_castling_g = False
                            

                                if self.position.black_castle_c:
                                    self.visions_white(self.position.boardstate)
                                    if all(isinstance(square, Empty) for square in self.position.boardstate[0, 1:4]) == True and self.vision_white[0, 2:5].any() == False:
                                        black_castling_c = True

                                    else:
                                        black_castling_c = False

                                moves, moves_vision = self.position.boardstate[i, j].get_legal_moves(self.position.boardstate, (i, j), black_castling_c, black_castling_g)
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
        legal_moves = []
        if self.position.white_to_move == True:
            moves = self.get_pseudo_legal_moves(self.position)
            for move in moves:
                child = self.position.make_move(move)
                king_pos = self.find_piece(child.boardstate, King, 'w')[0]
                self.visions_black(child.boardstate)
                if self.vision_black[king_pos] == False:
                    legal_moves.append(move)


        if self.position.white_to_move == False:
            moves = self.get_pseudo_legal_moves(self.position)
            for move in moves:
                child = self.position.make_move(move)
                king_pos = self.find_piece(child.boardstate, King, 'b')[0]
                self.visions_black(child.boardstate)

                if self.vision_white[king_pos] == False:
                    legal_moves.append(move)

        return legal_moves


                    