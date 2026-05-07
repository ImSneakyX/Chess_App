import sys 
from chessboard.move import Move_White, Move_Black
from chessboard.board import Board

class Game: 
    def __init__(self):
        self.brett = Board()
        self.brett.start_position()
        self.brett.chessboard_notation()
        self.position = self.brett.start
        self.start_game()
        self.make_move_white()

    def start_game(self):
        print(f'The game begins!')
        self.brett.display('name', self.brett.start)
    
    def make_move_white(self):
        start_square = input(f'White, make a move! Select the square with the piece that you want to move: ')
        end_square = input(f'and select the square you want to put the piece on: ')
        for row, i in enumerate(self.brett.notation):
            for col, j in enumerate(i):
                if  self.brett.notation[row, col] == start_square:
                    start_square = tuple((row, col))
                if  self.brett.notation[row, col] == end_square:
                    end_square = tuple((row, col))


        x = Move_White(self.position, start_square, end_square)
        self.position = x.pos_new #wird wieder zu Brett umgewandelt
        self.make_move_black() #ruft die andere func auf

    def make_move_black(self):
        start_square = input(f'Black, make a move! Select the square with the piece that you want to move: ')
        end_square = input(f'and select the square you want to put the piece on: ')
        for row, i in enumerate(self.brett.notation):
            for col, j in enumerate(i):
                if  self.brett.notation[row, col] == start_square:
                        start_square = tuple((row, col))
                if  self.brett.notation[row, col] == end_square:
                        end_square = tuple((row, col))


        x = Move_Black(self.position, start_square, end_square)
        self.position = x.pos_new #wird wieder zu Brett umgewandelt
        self.make_move_white() #ruft wieder sofort die andere func uf




Game()

