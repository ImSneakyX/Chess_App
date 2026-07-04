import sys
import os 
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chessboard.pieces import Pawn, Rook, Knight, Queen, King, Bishop, Empty
from chessboard.board import Board
from chessboard.game_engine import MoveGenerator
import time



class Ultimate:

    def __init__(self, game_over = False):
        self.game_over = game_over
        self.played_moves = []
        self.calculations = 0
        self.best_move = None



    
    def minimax(self, position, depth, alpha, beta):
        if depth == 0 or self.game_over:
            self.calculations += 1
            
            return self.static_evaluation(position), None
        
        move_gen = MoveGenerator(position)
        
        moves = move_gen.generate_legal_moves()
        best_move = 10
        if position.white_to_move == True:

            maxEval = -100000
            
            for move in moves:
                undo = position.make_move(move)
                eval, _ = self.minimax(position, depth-1, alpha, beta)

                position.unmake_move(move, undo)
                if maxEval <= eval:
                    maxEval = eval
                    best_move = move

                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            
            
            return maxEval, best_move
        else:
            minEval = 100000
            for move in moves:
                undo = position.make_move(move)
                eval, _ = self.minimax(position, depth-1, alpha, beta)
                position.unmake_move(move, undo)
                if minEval >= eval:
                    minEval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval, best_move
        


    def static_evaluation(self, position):

        evaluation = position.abs_piece_value + round(position.add_pawn_value, 1)
        return evaluation

    




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







