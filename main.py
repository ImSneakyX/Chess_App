import sys 
from chessboard.move import Move
from chessboard.board import Board

class Spiel: 
    def __init__(self):
        self.brett = Board()
        self.start_Spiel()

    def start_Spiel(self):
        print(f'Das Spiel startet')
        print(self.brett.start_position())


Spiel()

