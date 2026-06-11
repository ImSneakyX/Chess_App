class Ultimate:

    def __init__(self, game_over):
        self.game_over = game_over



    def minimax(self, position, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or self.game_over:
            return self.evaluation(position)
        
        if maximizingPlayer == 'w':

            max = 100000
            for 