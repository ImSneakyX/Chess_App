import sys 
from chessboard.move import Move
from chessboard.board import Board

class Game: 
    def __init__(self):
        self.brett = Board()
        self.brett.chessboard_notation()
        self.start_game()
        self.make_move()

    def start_game(self):
        print(f'The game begins!')
        print(self.brett.start_position())
    
    def make_move(self):
        start_square = input(f'Make a move! Select the square with the piece that you want to move: ')
        end_square = input(f'and select the square you want to put the piece on: ')
        for row, i in enumerate(self.brett.notation):
            for col, j in enumerate(i):
                if  self.brett.notation[row, col] == start_square:
                    start_square = tuple((row, col))
                if  self.brett.notation[row, col] == end_square:
                    end_square = tuple((row, col))


        new_pos = Move(self.brett.start_position(), start_square, end_square)
        return new_pos




Game()

