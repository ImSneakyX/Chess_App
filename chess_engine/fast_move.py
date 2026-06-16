import sys
import os 
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chessboard.board import Board
from chessboard.pieces import Pawn, Rook, Knight, Queen, King, Bishop, Empty
import numpy as np

class Move(Board):
    def __init__(self, boardstate, start_square, end_square, start_pos): 
        Board.__init__(self)
        self.start = boardstate
        self.start_pos = start_pos
        self.start_square = start_square
        self.end_square = end_square
        self.piece = self.start[self.start_square]

        self.promotion = False

        self.vision = None
        self.legal = None
        self.pos_new = None
        self.order()

    def order(self):
        pass

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


    def get_legal_move_mask(self):
        pass


    def move(self):
        pass

    def get_all_legal_moves(self):
        pass

    
    
    

class Move_White_kbqr(Move):
    def __init__(self, boardstate, start_square, end_square, start_pos): 
        Move.__init__(self, boardstate, start_square, end_square, start_pos)

    def order(self):
        

        self.move()


        
    
    
    def move(self):
        self.start1 = self.start.copy()
        self.start1[self.end_square] = self.piece
        self.start1[self.start_square] = self.empty
        self.pos_new = self.start1
        self.visions_black(self.pos_new)
        if self.vision_black[self.find_piece(self.pos_new, King, 'w')[0]] == False:
            self.legal = True 

        else:
            self.pos_new = self.start
            self.legal = False
        # Move-Tracker 
        if self.legal == True and isinstance(self.piece, Rook):
            self.rook_starts = self.find_piece(self.start_pos, Rook, 'w')
            self.rook_l = self.start_pos[self.rook_starts[0]]
            self.rook_r = self.start_pos[self.rook_starts[1]]
            self.moved_rook_l = self.rook_l.move_tracker(self.rook_starts[0], self.start_square)
            self.moved_rook_r = self.rook_r.move_tracker(self.rook_starts[1], self.start_square)

        return self.pos_new     


            

    
class Move_Black_kbqr(Move):
    def __init__(self, boardstate, start_square, end_square, start_pos): 
        Move.__init__(self, boardstate, start_square, end_square, start_pos)
        

    def order(self):

        self.move()

    
    
    def move(self):
        self.start1 = self.start.copy()
        self.start1[self.end_square] = self.piece
        self.start1[self.start_square] = self.empty
        self.pos_new = self.start1
        self.visions_white(self.pos_new)
        if self.vision_white[self.find_piece(self.pos_new, King, 'b')[0]] == False:
            self.legal = True

        else: 
            self.legal = False
            self.pos_new = self.start
        # Move-Tracker 
        if self.legal == True and isinstance(self.piece, Rook):
            self.rook_starts = self.find_piece(self.start_pos, Rook, 'w')
            self.rook_l = self.start_pos[self.rook_starts[0]]
            self.rook_r = self.start_pos[self.rook_starts[1]]
            self.moved_rook_l = self.rook_l.move_tracker(self.rook_starts[0], self.start_square)
            self.moved_rook_r = self.rook_r.move_tracker(self.rook_starts[1], self.start_square)

        return self.pos_new
    
class Move_White_King(Move):
    def __init__(self, boardstate, start_square, end_square, start_pos): 
        Move.__init__(self, boardstate, start_square, end_square, start_pos)

    def order(self):

        self.visions_black(self.start)
        self.castling_white(self.start)
        self.move()


    def castling_white(self, boardstate):
        self.king_start = self.find_piece(self.start_pos, King, 'w')[0]
        self.king = self.start_pos[self.king_start]

        self.rook_starts = self.find_piece(self.start_pos, Rook, 'w')
        self.rook_l = self.start_pos[self.rook_starts[0]]
        self.rook_r = self.start_pos[self.rook_starts[1]]
        self.king.castling(boardstate, self.rook_l.moved, self.rook_r.moved, self.king.moved, self.king_start, self.rook_starts[0], self.rook_starts[1], self.vision_black)
    
    
    def move(self):
        self.start1 = self.start.copy()
        self.start1[self.end_square] = self.piece
        self.start1[self.start_square] = self.empty

        if isinstance(self.piece, King) and self.start_square == self.king_start and self.end_square == (7, 6):
            self.start1[self.rook_starts[1]] = self.empty
            self.start1[(7, 5)] = self.rook_r

        if isinstance(self.piece, King) and self.start_square == self.king_start and self.end_square == (7, 2):
            self.start1[self.rook_starts[0]] = self.empty
            self.start1[(7, 3)] = self.rook_l

        self.pos_new = self.start1
        self.display('name', self.pos_new)
        print(self.end_square)
        self.visions_black(self.pos_new)
        if self.vision_black[self.find_piece(self.pos_new, King, 'w')[0]] == False:
                
            self.legal = True

        else: 
            self.legal = False
            self.pos_new = self.start

        # Move-Tracker 
        if self.legal == True:
            self.moved_king = self.king.move_tracker(self.king_start, self.start_square)
            self.moved_rook_l = self.rook_l.move_tracker(self.rook_starts[0], self.start_square)
            self.moved_rook_r = self.rook_r.move_tracker(self.rook_starts[1], self.start_square)

        return self.pos_new

            

    
class Move_Black_King(Move):
    def __init__(self, boardstate, start_square, end_square, start_pos): 
        Move.__init__(self, boardstate, start_square, end_square, start_pos)
        

    def order(self):
        
        self.visions_white(self.start)
        self.castling_black(self.start)
        self.move()


    def castling_black(self, boardstate):
        self.king_start = self.find_piece(self.start_pos, King, 'b')[0]
        self.king = self.start_pos[self.king_start]

        self.rook_starts = self.find_piece(self.start_pos, Rook, 'b')
        self.rook_l = self.start_pos[self.rook_starts[0]]
        self.rook_r = self.start_pos[self.rook_starts[1]]
        self.king.castling(boardstate, self.rook_l.moved, self.rook_r.moved, self.king.moved, self.king_start, self.rook_starts[0], self.rook_starts[1], self.vision_white)
    
    
    def move(self):
        self.start1 = self.start.copy()
        self.start1[self.end_square] = self.piece
        self.start1[self.start_square] = self.empty
        if isinstance(self.piece, King) and self.start_square == self.king_start and self.end_square == (0, 6):
            self.start1[self.rook_starts[1]] = self.empty
            self.start1[(0, 5)] = self.rook_r

        if isinstance(self.piece, King) and self.start_square == self.king_start and self.end_square == (0, 2):
            self.start1[self.rook_starts[0]] = self.empty
            self.start1[(0, 3)] = self.rook_l

        self.pos_new = self.start1
        self.visions_white(self.pos_new)
        if self.vision_white[self.find_piece(self.pos_new, King, 'b')[0]] == False:

                self.legal = True

        else: 

                self.legal = False
                self.pos_new = self.start



        # Move-Tracker 
        if self.legal == True:
            self.moved_king = self.king.move_tracker(self.king_start, self.start_square)
            self.moved_rook_l = self.rook_l.move_tracker(self.rook_starts[0], self.start_square)
            self.moved_rook_r = self.rook_r.move_tracker(self.rook_starts[1], self.start_square)

        return self.pos_new
    

class Move_White_Pawn(Move):
    def __init__(self, boardstate, start_square, end_square, start_pos): 
        Move.__init__(self, boardstate, start_square, end_square, start_pos)

    def order(self):

        self.move()


        
    
    
    def move(self):
        self.start1 = self.start.copy()
        piece_on_end_square = self.start1[self.end_square]
        self.start1[self.end_square] = self.piece
        self.start1[self.start_square] = self.empty


        if isinstance(self.piece, Pawn) and isinstance(piece_on_end_square, Empty) and self.start_square[1] != self.end_square[1]:
            self.start1[(self.start_square[0], self.end_square[1])] = self.empty



        if isinstance(self.piece, Pawn) and self.start_square[0] == 6 and self.end_square[0] == 4:
            self.start1[self.end_square] = self.pawn_w 
            self.pawn_w.two_steps()

        if isinstance(self.piece, Pawn) and self.end_square[0] == 0:
            self.promotion = True




        self.pos_new = self.start1
        self.visions_black(self.pos_new)
        if self.vision_black[self.find_piece(self.pos_new, King, 'w')[0]] == False:

                self.legal = True

        else: 

                self.legal = False
                self.pos_new = self.start

        # Move-Tracker 
        if self.legal == True:
            for row, i in enumerate(self.start1):
                for col, j in enumerate(i):
                    if isinstance(self.start1[row, col], Pawn) and self.start1[row, col] != self.pawn_w: 
                        self.start1[row, col].moved_two_steps = False
        return self.pos_new


            

    
class Move_Black_Pawn(Move):
    def __init__(self, boardstate, start_square, end_square, start_pos): 
        Move.__init__(self, boardstate, start_square, end_square, start_pos)
        

    def order(self):

        self.move()



    
    
    def move(self):
        self.start1 = self.start.copy()
        piece_on_end_square = self.start1[self.end_square]
        self.start1[self.end_square] = self.piece
        self.start1[self.start_square] = self.empty


        if isinstance(self.piece, Pawn) and isinstance(piece_on_end_square, Empty) and self.start_square[1] != self.end_square[1]:
            self.start1[(self.start_square[0], self.end_square[1])] = self.empty
            
        if isinstance(self.piece, Pawn) and self.start_square[0] == 1 and self.end_square[0] == 3:
            self.start1[self.end_square] = self.pawn_b
            self.pawn_b.two_steps()


        if isinstance(self.piece, Pawn) and self.end_square[0] == 7:
            self.promotion = True

        self.pos_new = self.start1
        self.visions_white(self.pos_new)
        if self.vision_white[self.find_piece(self.pos_new, King, 'b')[0]] == False:

                self.legal = True
  
        else: 

            self.legal = False
            self.pos_new = self.start


        # Move-Tracker 
        if self.legal == True:
            for row, i in enumerate(self.start1):
                for col, j in enumerate(i):
                    if isinstance(self.start1[row, col], Pawn) and self.start1[row, col] != self.pawn_b: 
                        self.start1[row, col].moved_two_steps = False
        return self.pos_new
    



