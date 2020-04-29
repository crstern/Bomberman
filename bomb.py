class Bomb:
    def __init__(self, position, owner):
        self.position = position
        self.activated = False
        self.owner = owner

    def clear(self, game):
        game.table[self.position[0]][self.position[1]] = ' '

    def activate(self, game):
        game.table[self.position[0]][self.position[1]] = 'a'
        self.activated = True

