from copy import deepcopy
from random import randint
from bomb import Bomb

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

def add_positions(p1, p2):
    return p1[0] + p2[0], p1[1] + p2[1]

def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


class Game:
    ROWS = 11
    COLUMNS = 21
    PMIN = None  # Player object
    PMAX = None  # Player object
    EMPTY = ' '
    WALL = '#'
    PROTECTION = 'p'
    BOMB = 'b'

    def __init__(self, table, bombs, pmin, pmax):
        self.table = table
        self.bombs = bombs  # array of bombs
        self.pmin = pmin
        self.pmax = pmax

    def get_player_by_name(self, name):
        if name == self.pmin.player_name:
            return self.pmin
        else:
            return self.pmax

    def is_player_safe(self, player_name, bomb_position):
        """
        function which returns True if a player is safe
        after a bomb (that is on the same line or the same
        column as the player_name) exploded
        :param bomb_position:
        :param player_name:
        :return boolean:
        """
        player_position = self.get_player_by_name(player_name).position
        # we verify in every direction if the first thing next to player
        # is bomb or wall.

        is_safe_x = False
        is_safe_y = False

        if player_position[0] == bomb_position[0]:
            for orizontal_index in range(player_position[1], bomb_position[1]):
                if self.table[player_position[0]][orizontal_index] == '#':
                    is_safe_x = True
                    break
            for orizontal_index in range(bomb_position[1], player_position[1]):
                if self.table[player_position[0]][orizontal_index] == '#':
                    is_safe_x = True
                    break
        else:
            is_safe_x = True

        if player_position[1] == bomb_position[1]:
            for vertical_index in range(player_position[0], bomb_position[0]):
                if self.table[vertical_index][player_position[1]] == '#':
                    is_safe_y = True
                    break

            for vertical_index in range(bomb_position[0], player_position[0]):
                if self.table[vertical_index][player_position[1]] == '#':
                    is_safe_y = True
                    break
        else:
            is_safe_y = True
        if is_safe_y and is_safe_x:
            return True
        return False

    def player_near_danger(self, player, bomb_position):
        neighbourhood = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        for pos in neighbourhood:
            if self.is_player_safe(player.player_name, add_positions(bomb_position, pos)):
                return True
        return False

    def game_over(self):
        """
            The game is over when one of the player dies
            ie a player is positioned on the same line or
            the same column as an activated bomb

            The game can end if a player blocks itself with a bomb

        """
        if self.pmin.number_of_protections < 0 and self.pmax.number_of_protections < 0:
            return "remiza"

        if self.pmin.number_of_protections < 0:
            return Game.PMAX
        if self.pmax.number_of_protections < 0:
            return Game.PMIN

        for bomb in self.bombs:
            if bomb.activated:
                pmin_dies = False
                pmax_dies = False
                if not self.is_player_safe(self.pmin.player_name, bomb.position):
                    self.pmin.number_of_protections -= 1
                    if self.pmin.number_of_protections < 0:
                        pmin_dies = True

                if not self.is_player_safe(self.pmin.player_name, bomb.position):
                    self.pmax.number_of_protections -= 1
                    if self.pmax.number_of_protections < 0:
                        pmax_dies = True

                if pmin_dies and pmax_dies:
                    return "remiza"
                elif pmax_dies:
                    return Game.PMIN
                elif pmin_dies:
                    return Game.PMAX
        is_pmax_ok = False

        for pos in range(4):
            new_pmax_position_x = self.pmax.position[0] + dx[pos]
            new_pmax_position_y = self.pmax.position[1] + dy[pos]

            if self.table[new_pmax_position_x][new_pmax_position_y] in [' ', 'p']:
                is_pmax_ok = True

        is_pmin_ok = False

        for pos in range(4):
            new_pmin_position_x = self.pmin.position[0] + dx[pos]
            new_pmin_position_y = self.pmin.position[1] + dy[pos]

            if self.table[new_pmin_position_x][new_pmin_position_y] in [' ', 'p']:
                is_pmin_ok = True
        if not is_pmax_ok:
            return Game.PMIN
        if not is_pmin_ok:
            return Game.PMAX

        return False

    def found_protection(self, player, new_pos_x, new_pos_y):
        self.table[new_pos_x][new_pos_y] = player.player_name
        player.number_of_protections += 1
        player.position = (new_pos_x, new_pos_y)

    def not_found_protection(self, player, new_pos_x, new_pos_y):
        self.table[new_pos_x][new_pos_y] = player.player_name
        player.position = (new_pos_x, new_pos_y)

    def player_attacks(self, player, new_pos_x, new_pos_y):
        game_copy_attacks = deepcopy(self)
        player_copy = game_copy_attacks.get_player_by_name(player)

        if player_copy.bomb_dropped is None or player_copy.bomb_dropped.activated:
            # player drops a bomb
            game_copy_attacks.table[player_copy.position[0]][player_copy.position[1]] = 'b'
            new_bomb = Bomb(position=player_copy.position, owner=player_copy)
            player_copy.bomb_dropped = new_bomb
            game_copy_attacks.bombs.append(new_bomb)

        else:
            # player activates the bomb dropped
            game_copy_attacks.table[player_copy.position[0]][player_copy.position[1]] = ' '
            for bomb in game_copy_attacks.bombs:
                if bomb.owner.player_name == player and not bomb.activated:
                    bomb.activate(game_copy_attacks)
                    break

        if game_copy_attacks.table[new_pos_x][new_pos_y] == 'p':
            game_copy_attacks.found_protection(player_copy, new_pos_x, new_pos_y)
        else:
            game_copy_attacks.not_found_protection(player_copy, new_pos_x, new_pos_y)

        return game_copy_attacks, player_copy

    def player_moves(self, player, new_pos_x, new_pos_y):
        game_copy = deepcopy(self)
        player_copy = game_copy.get_player_by_name(player)

        game_copy.table[player_copy.position[0]][player_copy.position[1]] = ' '
        if game_copy.table[new_pos_x][new_pos_y] == 'p':
            game_copy.found_protection(player_copy, new_pos_x, new_pos_y)
        else:
            game_copy.not_found_protection(player_copy, new_pos_x, new_pos_y)
        return game_copy, player_copy

    def game_moves(self, player):
        """
        returns a list of tuples: like
        (new possible Game object with a new configuration,
        boolean which is true if the player gets a new protection with its next move and false otherwise)
        :param: string
        :return: list of games
        """
        moves_list = []
        current_player = self.get_player_by_name(player)

        for i in range(4):

            pos_x = current_player.position[0] + dx[i]
            pos_y = current_player.position[1] + dy[i]

            if self.table[pos_x][pos_y] in [' ', 'p']:
                """
                we create two copies on the actual game state:
                one for attacker player
                and one for a player that doesn't attack
                """
                game_copy, _ = self.player_moves(player, pos_x, pos_y)
                game_copy_attack, _ = self.player_attacks(player, pos_x, pos_y)
                # to do: if the player is blocked after he shipped the bomb
                # he won't be able to move to a position which has a dead end.

                # print("dont " + str(game_copy.estimate_score(0)))
                # print("attak  " + str(game_copy_attack.estimate_score(0)))
                moves_list.append(game_copy)
                moves_list.append(game_copy_attack)

        return moves_list

    def sanse_castig(self, player_name):
        score = 0
        player = self.get_player_by_name(player_name)
        oposite_player = self.pmin if player_name == self.PMAX else self.pmax
        for bomb in self.bombs:
            if bomb.owner == oposite_player:

                if not self.is_player_safe(player, bomb.position):
                    score -= 2
                    # print("i am not safe")

                elif self.player_near_danger(player, bomb.position):
                    score -= 2
                    # print("i am in danger")

            if bomb.owner == player:
                if bomb.activated and not self.is_player_safe(oposite_player, bomb.position):
                    score += 5
                    # print("PLAYER NOT SAFE")

                if not bomb.activated:
                    if self.player_near_danger(oposite_player, bomb.position):
                        score += 2
                        # print("Oposite IN DANGER")
                    elif not self.is_player_safe(oposite_player, bomb.position):
                        score += 2
                        # print("oposite is not safe")

                else:
                    score -= 5
            if bomb.owner == player and not bomb.activated:
                score += 5
        # score += manhattan(player.position, oposite_player.position)
        score += 10 * player.number_of_protections
        score -= manhattan(player.position, oposite_player.position)

        if score == 0:
            score = randint(1, 5)
            # print("IS RANDOM")

        return score

    def estimate_score(self, depth):
        t_game_over = self.game_over()
        if t_game_over == Game.PMIN:
            score = -999 - depth
        elif t_game_over == Game.PMAX:
            score = 999 + depth
        elif t_game_over == "remiza":
            score = 0
        else:
            score = self.sanse_castig(Game.PMAX) - self.sanse_castig(Game.PMIN)
        return score

    def __str__(self):
        result = ""
        for line in self.table:
            for i in line:
                result += (i)
            result += "\n"
        return result
