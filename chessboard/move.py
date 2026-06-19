class Move:

    def __init__(self, start_square, end_square, promotion_piece = None, en_passant = None):


        self.start_square = start_square
        self.end_square = end_square
        self.promotion_piece = promotion_piece
        self.en_passant = en_passant