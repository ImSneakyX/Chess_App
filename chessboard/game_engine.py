import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chessboard.move import Move
from chessboard.board import Board
from chessboard.pieces import Rook, King, Queen, Knight, Bishop, Pawn, Empty
from ui.dialogs import Promote
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
                if move_made.promotion_piece != None:
                    self.legal = True
                else:
                    self.legal = True
                    promote_dialog = Promote('w' if self.position.white_to_move else 'b')

                    promote_dialog.selected_piece.connect(lambda piece: setattr(move_made, 'promotion_piece', piece))
            
                    promote_dialog.exec_()

            else:
                self.legal = True


        else:
            self.legal = False
        

        if self.legal == True:
            if check_move[0].en_passant == True:
                move_made.en_passant = True
                self.position.make_move(move_made)

            else:
                self.position.make_move(move_made)
            
            move_gen = MoveGenerator(self.position)
            legal_moves = move_gen.generate_legal_moves()
            self.mate = None
            self.stalemate = None
            if len(legal_moves) == 0:
                if self.position.white_to_move:
                    if move_gen.is_square_in_check(self.position.king_w_pos, 'b'):
                        self.mate = True
                    else:
                        self.stalemate = True

                else:
                    if move_gen.is_square_in_check(self.position.king_b_pos, 'w'):
                        self.mate = True
                    else:
                        self.stalemate = True

            
class MoveGenerator:

    def __init__(self, position):

        self.position = position

    def get_pseudo_legal_moves(self):
        pseudo_moves = []
        board = self.position.boardstate
        if self.position.white_to_move == True:
            for i in range(8):
                for j in range(8):
                    piece = board[i, j]
                    if piece.color == 'w':
                        if piece.name != 'King' and piece.name != 'Pawn':
                            moves, moves_vision = piece.get_legal_moves(board, (i, j))
                            for m in moves: 
                                move = Move((i, j), m)
                                pseudo_moves.append(move)
                        elif piece.name == 'Pawn':
                            moves, moves_vision = piece.get_legal_moves(board, (i, j))
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





                        elif piece.name == 'King':
                            white_castling_c = None
                            white_castling_g = None
                            if self.position.white_castle_g:
                                    if all(isinstance(square, Empty) for square in board[7, 5:7]) == True and self.is_square_in_check([7, 4], 'b') == False and self.is_square_in_check([7, 5], 'b') == False and self.is_square_in_check([7, 6], 'b') == False:
                                        white_castling_g = True

                                    else:
                                        white_castling_g = False
                            

                            if self.position.white_castle_c:
                                    if all(isinstance(square, Empty) for square in board[7, 1:4]) == True and self.is_square_in_check([7, 4], 'b') == False and self.is_square_in_check([7, 3], 'b') == False and self.is_square_in_check([7, 2], 'b') == False:
                                        white_castling_c = True
                                    else:
                                        white_castling_c = False

                            moves, moves_vision = piece.get_legal_moves(board, (i, j), white_castling_c, white_castling_g)
                            for m in moves: 
                                move = Move((i, j), m)
                                pseudo_moves.append(move)
                        
                        

        
        elif self.position.white_to_move == False:
                for i in range(8):
                    for j in range(8):
                        piece = board[i, j]
                        if piece.color == 'b':
                            if piece.name != 'King' and piece.name != 'Pawn':
                                moves, moves_vision = piece.get_legal_moves(board, (i, j))
                                for m in moves: 
                                    move = Move((i, j), m)
                                    pseudo_moves.append(move)


                            elif piece.name == 'Pawn':
                                moves, moves_vision = piece.get_legal_moves(board, (i, j))
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

                            elif piece.name == 'King':
                                black_castling_c = None
                                black_castling_g = None
                                if self.position.black_castle_g:
                                    if all(isinstance(square, Empty) for square in board[0, 5:7]) == True and self.is_square_in_check([0, 4], 'w') == False and self.is_square_in_check([0, 5], 'w') == False and self.is_square_in_check([0, 6], 'w') == False:
                                        black_castling_g = True

                                    else:
                                        black_castling_g = False
                            

                                if self.position.black_castle_c:
                                    if all(isinstance(square, Empty) for square in board[0, 1:4]) == True and self.is_square_in_check([0, 4], 'w') == False and self.is_square_in_check([0, 3], 'w') == False and self.is_square_in_check([0, 2], 'w') == False:
                                        black_castling_c = True

                                    else:
                                        black_castling_c = False

                                moves, moves_vision = piece.get_legal_moves(board, (i, j), black_castling_c, black_castling_g)
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
    
    def is_square_in_check(self, square, color):
        
        board = self.position.boardstate
        row, col = square

        limit1 = row # oben
        limit2 = col #links 
        limit3 = 7 - row #unten
        limit4 = 7 - col #rechts

        limit5 = min(row, col) #oben links
        limit6 = min(7-row, 7-col) #unten rechts
        limit7 = min(7-row, col) #unten links
        limit8 = min(row, 7-col) #oben rechts

        
        for i in range(1, limit1 + 1):
            piece = board[(row - i, col)]
            if piece.name != 'empty':
                if piece.color == color and (piece.name == 'Queen' or piece.name == 'Rook'):
                    return True
                break

        for i in range(1, limit2 + 1):
            piece = board[(row, col - i)]
            if piece.name != 'empty':
                if piece.color == color and (piece.name == 'Queen' or piece.name == 'Rook'):
                    return True
                break

        for i in range(1, limit3 + 1):
            piece = board[(row + i, col)]
            if piece.name != 'empty':
                if piece.color == color and (piece.name == 'Queen' or piece.name == 'Rook'):
                    return True
                break

        for i in range(1, limit4 + 1):
            piece = board[(row, col + i)]
            if piece.name != 'empty':
                if piece.color == color and (piece.name == 'Queen' or piece.name == 'Rook'):
                    return True
                break


        for i in range(1, limit5 + 1):
            piece = board[(row - i, col - i)]
            if piece.name != 'empty':
                if piece.color == color and (piece.name == 'Queen' or piece.name == 'Bishop'):
                    return True
                break
            
        for i in range(1, limit6 + 1):
            piece = board[(row + i, col + i)]
            if piece.name != 'empty':
                if piece.color == color and (piece.name == 'Queen' or piece.name == 'Bishop'):
                    return True
                break
            
        for i in range(1, limit7 + 1):
            piece = board[(row + i, col - i)]
            if piece.name != 'empty':
                if piece.color == color and (piece.name == 'Queen' or piece.name == 'Bishop'):
                    return True
                break

        for i in range(1, limit8 + 1):
            piece = board[(row - i, col + i)]
            if piece.name != 'empty':
                if piece.color == color and (piece.name == 'Queen' or piece.name == 'Bishop'):
                    return True
                break
            

        offsets_knight = [(-2, 1), (-2, -1), (-1, -2), (1,-2), (2,-1), (2,1), (1,2), (-1, 2)]

        for x, y in offsets_knight:
            new_row, new_col = row + x, col + y
            if 0 <= new_row <8 and 0 <= new_col <8: 
                piece = board[(new_row, new_col)]
                if piece.color == color and piece.name == 'Knight':
                    return True
        
        offsets_king = [(1, 1), (1, 0), (1, -1), (0,-1), (-1,-1), (-1,0), (-1,1), (0, 1)]

        for x, y in offsets_king:
            new_row, new_col = row + x, col + y
            if 0 <= new_row <8 and 0 <= new_col <8: 
                piece = board[(new_row, new_col)]
                if piece.color == color and piece.name == 'King':
                    return True
        
            
        if color == 'b':

            if 0 <= row - 1 < 8 and 0 <= col - 1 < 8:
                piece = board[(row - 1, col - 1)]
                if piece.color == color and piece.name == 'Pawn':
                    return True
            
            if 0 <= row - 1 < 8 and 0 <= col + 1 < 8:
                piece = board[(row - 1, col + 1)]
                if piece.color == color and piece.name == 'Pawn':
                    return True
        
        else: 
            if 0 <= row + 1 < 8 and 0 <= col - 1 < 8:
                piece = board[(row + 1, col - 1)]
                if piece.color == color and piece.name == 'Pawn':
                    return True
            
            if 0 <= row + 1 < 8 and 0 <= col + 1 < 8:
                piece = board[(row + 1, col + 1)]
                if piece.color == color and piece.name == 'Pawn':
                    return True

        return False





    
    def generate_legal_moves(self):
        legal_moves = []
        self.position.calc_pins()
        moves = self.get_pseudo_legal_moves()
        for move in moves:
            piece = self.position.boardstate[move.start_square]
            if move.start_square in self.position.pinned:
                dr, dc = self.position.pinned[move.start_square]
                sr, sc = move.start_square
                er, ec = move.end_square

                move_dr = er - sr
                move_dc = ec - sc

                if move_dr * dc != move_dc * dr:
                    continue

            if len(self.position.checkers) == 1:

                if piece.name != 'King':

                    if move.end_square not in self.position.check_mask:
                            continue

            if len(self.position.checkers) >= 2:

                if piece.name != 'King':
                    continue
                    
            if piece.name == 'King':

                undo = self.position.make_move(move)
                if self.position.white_to_move == False:
                    legal = not self.is_square_in_check(self.position.king_w_pos, 'b')

                else: 
                    legal = not self.is_square_in_check(self.position.king_b_pos, 'w')
        
                self.position.unmake_move(move, undo)
            else:
                legal = True

            if legal:
                    legal_moves.append(move)

           

        return legal_moves
    
    def generate_legal_moves_directly(self):

        pass


                    