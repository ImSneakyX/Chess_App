import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chessboard.move import Move
from chessboard.board import Board
from chessboard.pieces import Rook, King, Queen, Knight, Bishop, Pawn, Empty
import numpy as np
import time

class GameEngine:
    def __init__(self, position):

        self.position = position
        self.legal = None
        self.promotion = False
        
        self.mate = None
        self.stalemate = None

    def check_move(self, move_made):

        check_move = []
        move_gen = MoveGenerator(self.position)
        legal_moves = move_gen.generate_legal_moves()
        for move in legal_moves:
            if move.start_square == move_made.start_square and move.end_square == move_made.end_square:
                check_move.append(move)

        if len(check_move) >= 1:
            if check_move[0].promotion_piece != None:
                self.legal = True
                self.promotion = True

            else:
                self.legal = True
                self.promotion = False

        else:
            self.legal = False
        

        if self.legal == True:
            if check_move[0].en_passant == True:
                move_made.en_passant = True
                self.position.make_move(move_made)
                print(self.position.boardstate, 'EP')

            else:
                self.position.make_move(move_made)
                print(self.position.boardstate)




    def promote_pawns(self, piece, square_of_promotion):

        self.position.boardstate[square_of_promotion] = piece


        
        

            
class MoveGenerator:

    def __init__(self, position):

        self.position = position

    def get_pseudo_legal_moves(self):
        pseudo_moves = []
        if self.position.white_to_move == True:
            for i in range(8):
                for j in range(8):
                    if self.position.boardstate[i, j].color == 'w':
                        if not isinstance(self.position.boardstate[i, j], King) and not isinstance(self.position.boardstate[i, j], Pawn):
                            moves, moves_vision = self.position.boardstate[i, j].get_legal_moves(self.position.boardstate, (i, j))
                            for m in moves: 
                                move = Move((i, j), m)
                                pseudo_moves.append(move)
                        elif isinstance(self.position.boardstate[i, j], Pawn):
                            moves, moves_vision = self.position.boardstate[i, j].get_legal_moves(self.position.boardstate, (i, j))
                            for m in moves: 
                                if m[0] == 0:
                                    promotion_pieces = ['Q', 'R', 'K', 'B']
                                    for piece in promotion_pieces:
                                        move = Move((i, j), m, piece)
                                        pseudo_moves.append(move)

                                else: 
                                    move = Move((i, j), m)
                                    pseudo_moves.append(move)
                                
                            if self.position.en_passant_square == (i - 1, j + 1) or self.position.en_passant_square == (i - 1, j - 1):
                                move = Move((i, j), self.position.en_passant_square, None, True)
                                pseudo_moves.append(move)





                        elif isinstance(self.position.boardstate[i, j], King):
                            white_castling_c = None
                            white_castling_g = None
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
                                move = Move((i, j), m)
                                pseudo_moves.append(move)
                        
                        

        
        elif self.position.white_to_move == False:
                for i in range(8):
                    for j in range(8):
                        if self.position.boardstate[i, j].color == 'b':
                            if not isinstance(self.position.boardstate[i, j], King) and not isinstance(self.position.boardstate[i, j], Pawn):
                                moves, moves_vision = self.position.boardstate[i, j].get_legal_moves(self.position.boardstate, (i, j))
                                for m in moves: 
                                    move = Move((i, j), m)
                                    pseudo_moves.append(move)


                            elif isinstance(self.position.boardstate[i, j], Pawn):
                                moves, moves_vision = self.position.boardstate[i, j].get_legal_moves(self.position.boardstate, (i, j))
                                for m in moves: 
                                    if m[0] == 7:
                                        promotion_pieces = ['Q', 'R', 'K', 'B']
                                        for piece in promotion_pieces:
                                            move = Move((i, j), m, piece)
                                            pseudo_moves.append(move)

                                    else: 
                                        move = Move((i, j), m)
                                        pseudo_moves.append(move)

                                if self.position.en_passant_square == (i + 1, j + 1) or self.position.en_passant_square == (i + 1, j - 1):
                                    move = Move((i, j), self.position.en_passant_square, None, True)
                                    pseudo_moves.append(move)

                            elif isinstance(self.position.boardstate[i, j], King):
                                black_castling_c = None
                                black_castling_g = None
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
                                    move = Move((i, j), m)
                                    pseudo_moves.append(move)

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
                    moves, moves_for_vision = boardstate[(row, col)].get_legal_moves(boardstate, (row, col))
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
                    moves, moves_for_vision = boardstate[(row, col)].get_legal_moves(boardstate, (row, col))
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
            moves = self.get_pseudo_legal_moves()
            for move in moves:
                before_board = str(self.position.boardstate)
                before_kw = self.position.king_w_pos
                before_kb = self.position.king_b_pos
                
                undo = self.position.make_move(move)
                self.visions_black(self.position.boardstate)
                if self.vision_black[self.position.king_w_pos] == False:
                    legal_moves.append(move)
                self.position.unmake_move(move, undo)
                if (
                    before_board != str(self.position.boardstate)
                    or before_kw != self.position.king_w_pos
                    or before_kb != self.position.king_b_pos
                ):
                    print("BUG BEI ZUG:", move.start_square, move.end_square)
                    return []
    


        if self.position.white_to_move == False:
            moves = self.get_pseudo_legal_moves()
            for move in moves:
                before_board = str(self.position.boardstate)
                before_kw = self.position.king_w_pos
                before_kb = self.position.king_b_pos
                undo = self.position.make_move(move)
                self.visions_white(self.position.boardstate)
                if self.vision_white[self.position.king_b_pos] == False:
                    legal_moves.append(move)
                self.position.unmake_move(move, undo)
                if (
                        before_board != str(self.position.boardstate)
                        or before_kw != self.position.king_w_pos
                        or before_kb != self.position.king_b_pos
                    ):
                        print("BUG BEI ZUG:", move.start_square, move.end_square)
                        return []
        return legal_moves


                    