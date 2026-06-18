import sys
import os 
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chessboard.move import Move_White, Move_Black
from chessboard.pieces import Pawn, Rook, Knight, Queen, King, Bishop, Empty
from chessboard.board import Board
from chess_engine.fast_move import Move_White_kbqr, Move_Black_kbqr, Move_White_King, Move_Black_King, Move_White_Pawn, Move_Black_Pawn, Move
from chessboard.position import Position
from chessboard.game_engine import MoveGenerator
import time



class Ultimate:

    def __init__(self, game_over = False):
        self.game_over = game_over
        self.played_moves = []
        self.calculations = 0


    
    def minimax(self, position, depth, alpha, beta):
        if depth == 0 or self.game_over:
            self.calculations += 1
            
            return self.static_evaluation(position)
        
        children = self.get_child_pos(position)

        if position.white_to_move == True:

            maxEval = -100000
            for c in children:
                eval = self.minimax(c, depth-1, alpha, beta)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval = 100000
            for c in children:
                eval = self.minimax(c, depth-1, alpha, beta)
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

                if position.boardstate[i, j].color == 'w':
                    sum_value_white += position.boardstate[i, j].value
                elif position.boardstate[i, j].color == 'b':
                    sum_value_black += position.boardstate[i, j].value

        evaluation = sum_value_white - sum_value_black
        return evaluation

    
    def get_child_pos(self, position):
        children = []
        move_gen = MoveGenerator(position)
        legal_moves = move_gen.generate_legal_moves()
        for move in legal_moves:
            children.append(position.make_move(move))

                        
        return children




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







