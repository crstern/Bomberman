
def manhattan(p1, p2):

    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


class Player:
    """
    Contains the properties of player:
    if has dropped a bomb, number of protectons, position and name
    """

    def __init__(self, position, player_name, bomb_dropped=None, number_of_protections=0):
        self.bomb_dropped = bomb_dropped  #
        self.number_of_protections = number_of_protections
        self.position = position
        self.player_name = player_name

    def near_bomb(self, bomb):
        if manhattan(self.position, bomb.position) == 1:
            return True
        return False

