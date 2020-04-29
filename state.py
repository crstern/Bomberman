class State:

    """
    Class used by minmax and alphabeta algorithms
    """

    MAXIMUM_DEPTH = None

    def __init__(self, board, current_player, depth, parent=None, score=None):
        self.board = board  # it s a 'Game' object so board.table gives us the table config
        self.current_player = board.get_player_by_name(current_player)
        self.depth = depth
        self.score = score
        self.parent = parent

        self.possible_moves = []
        self.chosen_state = None

    def opposite_player(self):
        if self.current_player == self.board.pmin:
            return self.board.pmax
        else:
            return self.board.pmin

    def state_moves(self):
        moves_list = self.board.game_moves(self.current_player)
        opp_player = self.opposite_player()

        state_moves_list = [State(move, opp_player, self.depth - 1, self) for move in moves_list]
        return state_moves_list

    def __str__(self):
        return str(self.board.table) + "(Current player:" + self.current_player + ")\n"

