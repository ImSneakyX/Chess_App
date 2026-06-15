import sys
import os 
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chessboard.move import Move_White, Move_Black
from chessboard.pieces import Pawn, Rook, Knight, Queen, King, Bishop, Empty
from chessboard.board import Board
from chess_engine.fast_move import Move_White_kbqr, Move_Black_kbqr, Move_White_King, Move_Black_King, Move_White_Pawn, Move_Black_Pawn, Move
import time



class Ultimate:

    def __init__(self, start_pos, game_over = False):
        self.game_over = game_over
        self.child = []
        self.start_pos = start_pos
        self.end_pos = None
        self.played_moves = []
        self.calculations = 0
        self.move = Move(self.start_pos, (0, 0), (0, 0), self.start_pos)
        




    def minimax(self, position, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or self.game_over:
            self.calculations += 1
            
            return self.static_evaluation(position)
        
        if maximizingPlayer == True:

            maxEval = -100000
            self.get_child_pos(position, True)
            for c in self.child:
                eval = self.minimax(c, depth-1, alpha, beta, False)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval = 100000
            self.get_child_pos(position, False)
            for c in self.child:
                eval = self.minimax(c, depth-1, alpha, beta, True)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval
        


    def static_evaluation(self, position):

        sum_value_white = 0
        sum_value_black = 0

        for i in range(8):
            for j in range(8):

                if position[i, j].color == 'w':
                    sum_value_white += position[i, j].value
                elif position[i, j].color == 'b':
                    sum_value_black += position[i, j].value

        evaluation = sum_value_white - sum_value_black
        return evaluation

    
    def get_child_pos(self, position, maximizingPlayer):
        self.child.clear()
        if maximizingPlayer == True:

            for i in range(8):
                for j in range(8):
                    if position[i, j].color == 'w':
                        if isinstance(position[i, j], Bishop) or isinstance(position[i, j], Knight) or isinstance(position[i, j], Queen) or isinstance(position[i, j], Rook):
                            moves, moves_for_vision = position[i, j].get_legal_moves(position, (i, j), None)
                            for m in moves:
                                child = Move_White_kbqr(position, (i, j), m, self.start_pos)
                                self.child.append(child.pos_new)

                        elif isinstance(position[i, j], King):
                            vision = self.move.visions_black(position)
                            moves, moves_for_vision = position[i, j].get_legal_moves(position, (i, j), vision)
                            for m in moves:
                                child = Move_White_King(position, (i, j), m, self.start_pos)
                                self.child.append(child.pos_new)

                        elif isinstance(position[i, j], Pawn):
                            moves, moves_for_vision = position[i, j].get_legal_moves(position, (i, j), None)
                            for m in moves:
                                child = Move_White_Pawn(position, (i, j), m, self.start_pos)
                                self.child.append(child.pos_new)
                            
        
        if maximizingPlayer == False:

            for i in range(8):
                for j in range(8):
                    if position[i, j].color == 'b':
                        if isinstance(position[i, j], Bishop) or isinstance(position[i, j], Knight) or isinstance(position[i, j], Queen) or isinstance(position[i, j], Rook):
                            moves, moves_for_vision = position[i, j].get_legal_moves(position, (i, j), None)
                            for m in moves:
                                child = Move_Black_kbqr(position, (i, j), m, self.start_pos)
                                self.child.append(child.pos_new)

                        elif isinstance(position[i, j], King):
                            vision = self.move.visions_black(position)
                            moves, moves_for_vision = position[i, j].get_legal_moves(position, (i, j), vision)
                            for m in moves:
                                child = Move_Black_King(position, (i, j), m, self.start_pos)
                                self.child.append(child.pos_new)

                        elif isinstance(position[i, j], Pawn):
                            moves, moves_for_vision = position[i, j].get_legal_moves(position, (i, j), None)
                            for m in moves:
                                child = Move_Black_Pawn(position, (i, j), m, self.start_pos)
                                self.child.append(child.pos_new)




if __name__ == '__main__':
    board = Board()
    test_board = board.start_position()
    #test_board[0, 3] = Empty()
    
    engine = Ultimate(False, board.start_position())

    t1 = time.time()
    print(engine.minimax(test_board, 4, -10000, 10000, True))
    print(engine.calculations)
    #board.display('name', engine.end_pos)
    t2 = time.time()

    print(f'{t2 - t1} sekunden')







