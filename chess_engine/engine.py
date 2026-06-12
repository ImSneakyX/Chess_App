import sys
import os 
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chessboard.move import Move_White, Move_Black
from chessboard.pieces import Pawn, Rook, Knight, Queen, King, Bishop, Empty
from chessboard.board import Board
import time



class Ultimate:

    def __init__(self, game_over, start_pos):
        self.game_over = game_over
        self.child = []
        self.start_pos = start_pos
        self.end_pos = None
        self.played_moves = []
        self.calculations = 0




    def minimax(self, position, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or self.game_over:
            self.calculations += 1
            
            return self.static_evaluation(position)
        
        if maximizingPlayer == 'w':

            maxEval = -100000
            self.get_child_pos(position, 'w')
            for c in self.child:
                eval = self.minimax(c, depth-1, alpha, beta, 'b')
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval = 100000
            self.get_child_pos(position, 'b')
            for c in self.child:
                eval = self.minimax(c, depth-1, alpha, beta, 'w')
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
        if maximizingPlayer == 'w':

            for i in range(8):
                for j in range(8):
                    if position[i, j].color == 'w':
                        if not isinstance(position[i, j], King):
                            moves, moves_for_vision = position[i, j].get_legal_moves(position, (i, j), None)
                            for m in moves:
                                child = Move_White(position, (i, j), m, self.start_pos)
                                self.child.append(child.pos_new)

                        elif isinstance(position[i, j], King):
                            
        
        if maximizingPlayer == 'b':

            for i in range(8):
                for j in range(8):
                    if position[i, j].color == 'b':
                        if not isinstance(position[i, j], King):
                            moves, moves_for_vision = position[i, j].get_legal_moves(position, (i, j), None)
                            for m in moves:
                                child = Move_Black(position, (i, j), m, self.start_pos)
                                self.child.append(child.pos_new)


if __name__ == '__main__':
    board = Board()
    test_board = board.start_position()
    #test_board[0, 3] = Empty()
    
    engine = Ultimate(False, board.start_position())

    t1 = time.time()
    print(engine.minimax(test_board, 1, -10000, 10000, 'w'))
    print(engine.calculations)
    #board.display('name', engine.end_pos)
    t2 = time.time()

    print(f'{t2 - t1} sekunden')







