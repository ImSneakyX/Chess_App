class Piece:
    def __init__(self, name, value, color):
        self.move = 'Can move'
        self.name = name
        self.value = value
        self.color = color
        self.moved = False

    def get_legal_moves(self, boardstate, start_square, vision):
        pass

    def move_tracker(self):
        pass


class Pawn(Piece):
    def __init__(self, color):
        Piece.__init__(self, 'Pawn', 1, color)


    def get_legal_moves(self, boardstate, start_square, vision):
        
        moves_for_vision = []
        moves = []
        row, col = start_square

        if self.color == 'w':
         
            if 0 <= col - 1 < 8:
                if boardstate[(row - 1, col - 1)].color != self.color and boardstate[(row - 1, col -1)].color != None: 
                    moves.append((row - 1, col -1))
            if 0 <= col + 1 < 8:
                if boardstate[(row - 1, col + 1)].color != None and boardstate[(row - 1, col + 1)].color != self.color: 
                        moves.append((row - 1, col + 1))

            if row == 6: 
                if boardstate[(row - 1, col)].value == 0:
                    moves.append((row - 1, col))  
                    if boardstate[(row - 2, col)].value == 0:
                        moves.append((row - 2, col))             
            elif row > 0 and boardstate[row-1, col].value == 0:
                    moves.append((row-1, col))
                
        else:
            if 0 <= col - 1 < 8:
                if boardstate[(row + 1, col - 1)].color != None and boardstate[(row + 1, col - 1)].color != self.color: 
                    moves.append((row + 1, col -1))
            if 0 <= col + 1 < 8:
                if boardstate[(row + 1, col + 1)].color != None and boardstate[(row + 1, col + 1)].color != self.color: 
                    moves.append((row + 1, col + 1))

            if row == 1:
                if boardstate[(row + 1, col)].value == 0:
                    moves.append((row + 1, col))
                    if boardstate [(row + 2, col)].value == 0:
                        moves.append((row + 2, col)) 

            elif row < 7 and boardstate[row+1, col].value == 0:
                    moves.append((row+1, col))
        return moves, moves_for_vision


class Knight(Piece):
    def __init__(self,color):
        Piece.__init__(self, 'Knight', 3, color)

    def get_legal_moves(self, boardstate, start_square, vision):
        
        moves = []
        moves_for_vision = []
        row, col = start_square

        offsets = [(-2, 1), (-2, -1), (-1, -2), (1,-2), (2,-1), (2,1), (1,2), (-1, 2)]

        for x, y in offsets:
            new_row, new_col = row + x, col + y
            if 0 <= new_row <8 and 0 <= new_col <8 and boardstate[(new_row, new_col)].color != self.color:
                moves.append((new_row, new_col))
            if 0 <= new_row <8 and 0 <= new_col <8 and boardstate[(new_row, new_col)].color == self.color:
                moves_for_vision.append((new_row, new_col))
        return moves, moves_for_vision
         

class Bishop(Piece):
    def __init__(self, color):
        Piece.__init__(self, 'Bishop', 3, color)

    def get_legal_moves(self, boardstate, start_square, vision):
        
        moves = []
        moves_for_vision = []
        row, col = start_square

        limit1 = min(row, col) #oben links
        limit2 = min(7-row, 7-col) #unten rechts
        limit3 = min(7-row, col) #unten links
        limit4 = min(row, 7-col) #oben rechts


        for i in range(1, limit1 + 1):
            new_row, new_col = row - i, col - i 
            if boardstate[(new_row, new_col)].value != 0:
                if boardstate[(new_row, new_col)].color == self.color:
                    moves_for_vision.append((new_row, new_col))
                    break
                else:
                    moves.append((new_row, new_col))
                    break
            else:
                moves.append((new_row, new_col))

        for i in range(1, limit2 + 1):
            new_row, new_col = row + i, col + i 
            if boardstate[(new_row, new_col)].value != 0:
                if boardstate[(new_row, new_col)].color == self.color:
                    moves_for_vision.append((new_row, new_col))
                    break
                else:
                    moves.append((new_row, new_col))
                    break
            else:
                moves.append((new_row, new_col))

        for i in range(1, limit3 + 1):
            new_row, new_col = row + i, col - i 
            if boardstate[(new_row, new_col)].value != 0:
                if boardstate[(new_row, new_col)].color == self.color:
                    moves_for_vision.append((new_row, new_col))
                    break
                else:
                    moves.append((new_row, new_col))
                    break
            else:
                moves.append((new_row, new_col))

        for i in range(1, limit4 + 1):
            new_row, new_col = row - i, col + i 
            if boardstate[(new_row, new_col)].value != 0:
                if boardstate[(new_row, new_col)].color == self.color:
                    moves_for_vision.append((new_row, new_col))
                    break
                else:
                    moves.append((new_row, new_col))
                    break
            else:
                moves.append((new_row, new_col))

        return moves, moves_for_vision

class Rook(Piece):
    def __init__(self, color, side):
        Piece.__init__(self, 'Rook', 5, color)
        self.side = side

    def get_legal_moves(self, boardstate, start_square, vision):
        moves = []
        moves_for_vision = []
        row, col = start_square

        limit1 = row # oben
        limit2 = col #links 
        limit3 = 7 - row #unten
        limit4 = 7 - col #rechts


        for i in range(1, limit1 + 1):
            new_row, new_col = row - i, col
            if boardstate[(new_row, new_col)].value != 0:
                if boardstate[(new_row, new_col)].color == self.color:
                    moves_for_vision.append((new_row, new_col))
                    break
                else:
                    moves.append((new_row, new_col))
                    break
            else:
                moves.append((new_row, new_col))

        for i in range(1, limit2 + 1):
            new_row, new_col = row, col - i
            if boardstate[(new_row, new_col)].value != 0:
                if boardstate[(new_row, new_col)].color == self.color:
                    moves_for_vision.append((new_row, new_col))
                    break
                else:
                    moves.append((new_row, new_col))
                    break
            else:
                moves.append((new_row, new_col))

        for i in range(1, limit3 + 1):
            new_row, new_col = row + i, col
            if boardstate[(new_row, new_col)].value != 0:
                if boardstate[(new_row, new_col)].color == self.color:
                    moves_for_vision.append((new_row, new_col))
                    break
                else:
                    moves.append((new_row, new_col))
                    break
            else:
                moves.append((new_row, new_col))

        for i in range(1, limit4 + 1):
            new_row, new_col = row, col + i
            if boardstate[(new_row, new_col)].value != 0:
                if boardstate[(new_row, new_col)].color == self.color:
                    moves_for_vision.append((new_row, new_col))
                    break
                else:
                    moves.append((new_row, new_col))
                    break
            else:
                moves.append((new_row, new_col))


        return moves, moves_for_vision
    
    def move_tracker(self, start_position_rook, start_square):

        if start_square == start_position_rook:
            self.moved = True


        return self.moved




class Queen(Piece):
    def __init__(self, color):
        Piece.__init__(self, 'Queen', 9, color)

    def get_legal_moves(self, boardstate, start_square, vision):
        moves = []
        moves_for_vision = []
        row, col = start_square

        limit1 = row # oben
        limit2 = col #links 
        limit3 = 7 - row #unten
        limit4 = 7 - col #rechts

        limit5 = min(row, col) #oben links
        limit6 = min(7-row, 7-col) #unten rechts
        limit7 = min(7-row, col) #unten links
        limit8 = min(row, 7-col) #oben rechts

        for i in range(1, limit1 + 1):
            new_row, new_col = row - i, col
            if boardstate[(new_row, new_col)].value != 0:
                if boardstate[(new_row, new_col)].color == self.color:
                    moves_for_vision.append((new_row, new_col))
                    break
                else:
                    moves.append((new_row, new_col))
                    break
            else:
                moves.append((new_row, new_col))

        for i in range(1, limit2 + 1):
            new_row, new_col = row, col - i
            if boardstate[(new_row, new_col)].value != 0:
                if boardstate[(new_row, new_col)].color == self.color:
                    moves_for_vision.append((new_row, new_col))
                    break
                else:
                    moves.append((new_row, new_col))
                    break
            else:
                moves.append((new_row, new_col))

        for i in range(1, limit3 + 1):
            new_row, new_col = row + i, col
            if boardstate[(new_row, new_col)].value != 0:
                if boardstate[(new_row, new_col)].color == self.color:
                    moves_for_vision.append((new_row, new_col))
                    break
                else:
                    moves.append((new_row, new_col))
                    break
            else:
                moves.append((new_row, new_col))

        for i in range(1, limit4 + 1):
            new_row, new_col = row, col + i
            if boardstate[(new_row, new_col)].value != 0:
                if boardstate[(new_row, new_col)].color == self.color:
                    moves_for_vision.append((new_row, new_col))
                    break
                else:
                    moves.append((new_row, new_col))
                    break
            else:
                moves.append((new_row, new_col))

        for i in range(1, limit5 + 1):
            new_row, new_col = row - i, col - i 
            if boardstate[(new_row, new_col)].value != 0:
                if boardstate[(new_row, new_col)].color == self.color:
                    moves_for_vision.append((new_row, new_col))
                    break
                else:
                    moves.append((new_row, new_col))
                    break
            else:
                moves.append((new_row, new_col))

        for i in range(1, limit6 + 1):
            new_row, new_col = row + i, col + i 
            if boardstate[(new_row, new_col)].value != 0:
                if boardstate[(new_row, new_col)].color == self.color:
                    moves_for_vision.append((new_row, new_col))
                    break
                else:
                    moves.append((new_row, new_col))
                    break
            else:
                moves.append((new_row, new_col))

        for i in range(1, limit7 + 1):
            new_row, new_col = row + i, col - i 
            if boardstate[(new_row, new_col)].value != 0:
                if boardstate[(new_row, new_col)].color == self.color:
                    moves_for_vision.append((new_row, new_col))
                    break
                else:
                    moves.append((new_row, new_col))
                    break
            else:
                moves.append((new_row, new_col))

        for i in range(1, limit8 + 1):
            new_row, new_col = row - i, col + i 
            if boardstate[(new_row, new_col)].value != 0:
                if boardstate[(new_row, new_col)].color == self.color:
                    moves_for_vision.append((new_row, new_col))
                    break
                else:
                    moves.append((new_row, new_col))
                    break
            else:
                moves.append((new_row, new_col))

        return moves, moves_for_vision
    
class King(Piece):
    def __init__(self, color):
        Piece.__init__(self, 'King', 100, color)
        self.castling_c = False
        self.castling_g = False
        

    def get_legal_moves(self, boardstate, start_square, vision):
        
        moves = []
        moves_for_vision = []
        row, col = start_square

        offsets = [(1, 1), (1, 0), (1, -1), (0,-1), (-1,-1), (-1,0), (-1,1), (0, 1)]

        for x, y in offsets:
            new_row, new_col = row + x, col + y
            if 0 <= new_row <8 and 0 <= new_col <8 and boardstate[(new_row, new_col)].color != self.color and vision[(new_row, new_col)] == False:
                moves.append((new_row, new_col))
        if self.castling_c == True:
            moves.append((row, 2))

        if self.castling_g == True:
            moves.append((row, 6))
        return moves, moves_for_vision
    
    def move_tracker(self, start_position_king, input_start_square):

        if input_start_square == start_position_king:
            self.moved = True


        return self.moved

    def castling(self, boardstate, moved_rook_left, moved_rook_right, moved_king, start_square_king, start_square_rook_left, start_square_rook_right, vision):
        row, col = start_square_king 
        row_l, col_l = start_square_rook_left
        row_r, col_r = start_square_rook_right
        col_min_l, col_max_l = sorted([2, col])

        if moved_rook_left == False and moved_king == False and all(isinstance(square, Empty) for square in boardstate[row, col_l + 1:col]) == True and vision[row, col_min_l:col_max_l+1].any() == False:
            self.castling_c = True
        else:
            self.castling_c = False

        if moved_rook_right == False and moved_king == False and all(isinstance(square, Empty) for square in boardstate[row, col + 1:col_r]) == True and vision[row, col:col_r].any() == False:
            self.castling_g = True
        else:
            self.castling_g = False




class Empty(Piece):
    def __init__(self):
        Piece.__init__(self, 'empty', 0, None)

    def get_legal_moves(self, boardstate, start_square, vision):
        moves = []
        moves_for_vision = []
        return moves, moves_for_vision
