import sys 
from chessboard.move import Move_White, Move_Black
from chessboard.board import Board

class Game: 
    def __init__(self):
        self.brett = Board()
        self.start_pos = self.brett.start_position()
        self.brett.chessboard_notation()
        self.position = self.brett.start_pos
        self.game = 0
        self.start_game()


    def start_game(self):
        print(f'The game begins!')
        self.brett.display('name', self.brett.start_pos)
        while self.game == 0:
            self.make_move_white()
            self.make_move_black()
    
    def make_move_white(self):
        start_square = input(f'White, make a move! Select the square with the piece that you want to move: ')
        end_square = input(f'and select the square you want to put the piece on: ')
        for row, i in enumerate(self.brett.notation):
            for col, j in enumerate(i):
                if  self.brett.notation[row, col] == start_square:
                    start_square = tuple((row, col))
                if  self.brett.notation[row, col] == end_square:
                    end_square = tuple((row, col))
        

        if isinstance(start_square, str):
            if isinstance(end_square, str):
                print(f"Both selected squares don't exist! Please select exisitng squares")
                return self.make_move_white()
            else:
                print(f"Selected start square doesn't exist! Please select an exisiting square")
                return self.make_move_white()
        if isinstance(end_square, str) and not isinstance(start_square, str):
            print(f"Selected end square doesn't exist! Please select an exisitng square")
            return self.make_move_white()


        x = Move_White(self.position, start_square, end_square, self.start_pos)
        if x.mate == True:
            print('Schachmatt, Schwarz gewinnt!')
            self.game = 1
            return self.game
        if x.stalemate == True:
            print('Patt!')
            self.game = 1
            return self.game
        if x.legal == True:
            self.position = x.pos_new #wird wieder zu Brett umgewandelt
        else: 
            self.make_move_white()

    def make_move_black(self):
        start_square = input(f'Black, make a move! Select the square with the piece that you want to move: ')
        end_square = input(f'and select the square you want to put the piece on: ')
        for row, i in enumerate(self.brett.notation):
            for col, j in enumerate(i):
                if  self.brett.notation[row, col] == start_square:
                        start_square = tuple((row, col))
                if  self.brett.notation[row, col] == end_square:
                        end_square = tuple((row, col))

        if isinstance(start_square, str):
            if isinstance(end_square, str):
                print(f"Both selected squares don't exist! Please select exisitng squares")
                return self.make_move_black()
            else:
                print(f"Selected start square doesn't exist! Please select an exisiting square")
                return self.make_move_black()
        if isinstance(end_square, str) and not isinstance(start_square, str):
            print(f"Selected end square doesn't exist! Please select an exisitng square")
            return self.make_move_black()


        x = Move_Black(self.position, start_square, end_square, self.start_pos)
        if x.mate == True:
            print('Schachmatt, Weiß gewinnt!')
            self.game = 1
            return self.game
        if x.stalemate == True:
            print('Patt!')
            self.game = 1
            return self.game
        if x.legal == True:
             self.position = x.pos_new
             self.vision = x.vision
        else:
             self.make_move_black()





Game()

