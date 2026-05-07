class Piece:
    def __init__(self, name, value, color):
        self.move = 'Can move'
        self.name = name
        self.value = value
        self.color = color

    def get_legal_moves(self, boardstate, start_square):
        pass

class Pawn(Piece):
    def __init__(self, color):
        Piece.__init__(self, 'Pawn', 1, color)

    def get_legal_moves(self, boardstate, start_square):

        moves = []
        row, col = start_square

        if self.color == 'w':
            if boardstate[(row - 1, col - 1)].color != self.color and boardstate[(row - 1, col -1)].color != None: 
                moves.append((row - 1, col -1))
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
            if boardstate[(row + 1, col - 1)].color != None and boardstate[(row + 1, col - 1)].color != self.color: 
                moves.append((row + 1, col -1))
            if boardstate[(row + 1, col + 1)].color != None and boardstate[(row + 1, col + 1)].color != self.color: 
                moves.append((row + 1, col + 1))

            if row == 1:
                if boardstate[(row + 1, col)].value == 0:
                    moves.append((row + 1, col))
                    if boardstate [(row + 2, col)].value == 0:
                        moves.append((row + 2, col)) 

            elif row < 7 and boardstate[row+1, col].value == 0:
                    moves.append((row+1, col))
        return moves 


class Knight(Piece):
    def __init__(self,color):
        Piece.__init__(self, 'Knight', 3, color)

    def get_legal_moves(self, boardstate, start_square):
        
        moves = []
        row, col = start_square

        offsets = [(-2, 1), (-2, -1), (-1, -2), (1,-2), (2,-1), (2,1), (1,2), (-1, 2)]

        for x, y in offsets:
            new_row, new_col = row + x, col + y
            if 0 <= new_row <8 and 0 <= new_col <8 and (boardstate[(new_row, new_col)].color != self.color or boardstate[(new_row, new_col)] == 0):
                moves.append((new_row, new_col))
        return moves
         

class Bishop(Piece):
    def __init__(self, color):
        Piece.__init__(self, 'Bishop', 3, color)

    def get_legal_moves(self, boardstate, start_square):
        
        moves = []
        row, col = start_square

        limit1 = min(row, col) #oben links
        limit2 = min(7-row, 7-col) #unten rechts
        limit3 = min(7-row, col) #unten links
        limit4 = min(row, 7-col) #oben rechts

        for i in range(1, limit1 + 1):
            new_row, new_col = row - i, col - i 
            if boardstate[(new_row, new_col)] != 0:
                if boardstate[(new_row, new_col)].color == self.color:
                    break
                else:
                    moves.append((new_row, new_col))
                    break
            else:
                moves.append((new_row, new_col))

        for i in range(1, limit2 + 1):
            new_row, new_col = row + i, col + i 
            if boardstate[(new_row, new_col)] != 0:
                if boardstate[(new_row, new_col)].color == self.color:
                    break
                else:
                    moves.append((new_row, new_col))
                    break
            else:
                moves.append((new_row, new_col))

        for i in range(1, limit3 + 1):
            new_row, new_col = row + i, col - i 
            if boardstate[(new_row, new_col)] != 0:
                if boardstate[(new_row, new_col)].color == self.color:
                    break
                else:
                    moves.append((new_row, new_col))
                    break
            else:
                moves.append((new_row, new_col))

        for i in range(1, limit4 + 1):
            new_row, new_col = row - i, col + i 
            if boardstate[(new_row, new_col)] != 0:
                if boardstate[(new_row, new_col)].color == self.color:
                    break
                else:
                    moves.append((new_row, new_col))
                    break
            else:
                moves.append((new_row, new_col))

        return moves

class Rook(Piece):
    def __init__(self, color):
        Piece.__init__(self, 'Rook', 5, color)

    def get_legal_moves(self, boardstate, start_square):
        moves = []
        row, col = start_square

        limit1 = row # oben
        limit2 = col #links 
        limit3 = 7 - row #unten
        limit4 = 7 - col #rechts


        for i in range(1, limit1 + 1):
            new_row, new_col = row - i, col
            if boardstate[(new_row, new_col)] != 0:
                if boardstate[(new_row, new_col)].color == self.color:
                    break
                else:
                    moves.append((new_row, new_col))
                    break
            else:
                moves.append((new_row, new_col))

        for i in range(1, limit2 + 1):
            new_row, new_col = row, col - i
            if boardstate[(new_row, new_col)] != 0:
                if boardstate[(new_row, new_col)].color == self.color:
                    break
                else:
                    moves.append((new_row, new_col))
                    break
            else:
                moves.append((new_row, new_col))

        for i in range(1, limit3 + 1):
            new_row, new_col = row + i, col
            if boardstate[(new_row, new_col)] != 0:
                if boardstate[(new_row, new_col)].color == self.color:
                    break
                else:
                    moves.append((new_row, new_col))
                    break
            else:
                moves.append((new_row, new_col))

        for i in range(1, limit4 + 1):
            new_row, new_col = row, col + i
            if boardstate[(new_row, new_col)] != 0:
                if boardstate[(new_row, new_col)].color == self.color:
                    break
                else:
                    moves.append((new_row, new_col))
                    break
            else:
                moves.append((new_row, new_col))


        return moves




class Queen(Piece):
    def __init__(self, color):
        Piece.__init__(self, 'Queen', 9, color)

    def get_legal_moves(self, boardstate, start_square):
        moves = []
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
            if boardstate[(new_row, new_col)] != 0:
                if boardstate[(new_row, new_col)].color == self.color:
                    break
                else:
                    moves.append((new_row, new_col))
                    break
            else:
                moves.append((new_row, new_col))

        for i in range(1, limit2 + 1):
            new_row, new_col = row, col - i
            if boardstate[(new_row, new_col)] != 0:
                if boardstate[(new_row, new_col)].color == self.color:
                    break
                else:
                    moves.append((new_row, new_col))
                    break
            else:
                moves.append((new_row, new_col))

        for i in range(1, limit3 + 1):
            new_row, new_col = row + i, col
            if boardstate[(new_row, new_col)] != 0:
                if boardstate[(new_row, new_col)].color == self.color:
                    break
                else:
                    moves.append((new_row, new_col))
                    break
            else:
                moves.append((new_row, new_col))

        for i in range(1, limit4 + 1):
            new_row, new_col = row, col + i
            if boardstate[(new_row, new_col)] != 0:
                if boardstate[(new_row, new_col)].color == self.color:
                    break
                else:
                    moves.append((new_row, new_col))
                    break
            else:
                moves.append((new_row, new_col))

        for i in range(1, limit5 + 1):
            new_row, new_col = row - i, col - i 
            if boardstate[(new_row, new_col)] != 0:
                if boardstate[(new_row, new_col)].color == self.color:
                    break
                else:
                    moves.append((new_row, new_col))
                    break
            else:
                moves.append((new_row, new_col))

        for i in range(1, limit6 + 1):
            new_row, new_col = row + i, col + i 
            if boardstate[(new_row, new_col)] != 0:
                if boardstate[(new_row, new_col)].color == self.color:
                    break
                else:
                    moves.append((new_row, new_col))
                    break
            else:
                moves.append((new_row, new_col))

        for i in range(1, limit7 + 1):
            new_row, new_col = row + i, col - i 
            if boardstate[(new_row, new_col)] != 0:
                if boardstate[(new_row, new_col)].color == self.color:
                    break
                else:
                    moves.append((new_row, new_col))
                    break
            else:
                moves.append((new_row, new_col))

        for i in range(1, limit8 + 1):
            new_row, new_col = row - i, col + i 
            if boardstate[(new_row, new_col)] != 0:
                if boardstate[(new_row, new_col)].color == self.color:
                    break
                else:
                    moves.append((new_row, new_col))
                    break
            else:
                moves.append((new_row, new_col))

        return moves
    
class King(Piece):
    def __init__(self, color):
        Piece.__init__(self, 'King', 100, color)

    def get_legal_moves(self, boardstate, start_square):
        
        moves = []
        row, col = start_square

        offsets = [(1, 1), (1, 0), (1, -1), (0,-1), (-1,-1), (-1,0), (-1,1), (0, 1)]

        for x, y in offsets:
            new_row, new_col = row + x, col + y
            if 0 <= new_row <8 and 0 <= new_col <8 and (boardstate[(new_row, new_col)].color != self.color or boardstate[(new_row, new_col)] == 0):
                moves.append((new_row, new_col))
        return moves

class Empty(Piece):
    def __init__(self):
        Piece.__init__(self, 'empty', 0, None)

    def get_legal_moves(self, boardstate, start_square):
        moves = []
        return moves 
