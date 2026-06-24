class Move:

    def __init__(self, start_square, end_square, promotion_piece = None, en_passant = None):


        self.start_square = start_square
        self.end_square = end_square
        self.promotion_piece = promotion_piece
        self.en_passant = en_passant

class Undo:

    def __init__(self):


        self.moved_piece = None
        self.captured_piece = None
        self.start_square = None
        self.end_square = None

        self.old_turn = None

        self.old_castle_white_c = None
        self.old_castle_white_g = None
        self.old_castle_black_c = None
        self.old_castle_black_g = None

        self.old_en_passant = None

        self.promotion = None

        self.ep_captured_square = None
        self.ep_captured_piece = None

        self.rook_from = None
        self.rook_to = None
        self.rook = None
        
        self.abs_piece_value = None
        self.add_pawn_value = None


