from state import State
from player import Player
from game import Game
import pygame
import time

default_table = [
    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
    ['#', '1', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', '#', '#', ' ', ' ', ' ', '#', '#', '#', ' ', ' ', ' ', '#', '#', '#', '#', ' ', '#', '#', '#', '#', '#'],
    ['#', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', ' ', ' ', ' ', ' ', 'p', ' ', '#', ' ', ' ', 'p', ' ', ' ', '#', ' ', ' ', '#', '#', '#', ' ', '#', '#'],
    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', '#', '#', '#', '#', ' ', ' ', ' ', ' ', '#', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'p', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', ' ', '#', '#', '#', '#', '#', '#', '#', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', ' ', ' ', '#'],
    ['#', ' ', ' ', ' ', ' ', '#', ' ', ' ', '#', ' ', ' ', ' ', '#', 'p', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', ' ', '#', '#', '#', '#', ' ', ' ', '#', ' ', ' ', ' ', '#', '#', '#', ' ', '#', '#', '#', ' ', ' ', '#'],
    ['#', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '2', '#'],
    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
]


def add_positions(p1, p2):
    return p1[0] + p2[0], p1[1] + p2[1]

def draw_game(display, config):
    h_gr = 73
    w_gr = 73

    player1_img = pygame.image.load('B:\\Desk\\facultate-sem-2\\IA\\Bomberman\\player1.png')
    player1_img = pygame.transform.scale(player1_img, (w_gr, h_gr))

    player2_img = pygame.image.load('B:\\Desk\\facultate-sem-2\\IA\\Bomberman\\player2.png')
    player2_img = pygame.transform.scale(player2_img, (w_gr, h_gr))

    wall_img = pygame.image.load('B:\\Desk\\facultate-sem-2\\IA\\Bomberman\\wall.png')
    wall_img = pygame.transform.scale(wall_img, (w_gr, h_gr))

    space_img = pygame.image.load('B:\\Desk\\facultate-sem-2\\IA\\Bomberman\\space.png')
    space_img = pygame.transform.scale(space_img, (w_gr, h_gr))

    bomb_img = pygame.image.load('B:\\Desk\\facultate-sem-2\\IA\\Bomberman\\bomb.png')
    bomb_img = pygame.transform.scale(bomb_img, (w_gr, h_gr))

    drt = []
    for row in range(len(config.table)):
        for col in range(len(config.table[0])):
            patr = pygame.Rect(col * (w_gr + 1), row * (h_gr + 1), w_gr, h_gr)




""" Algoritmul MinMax ! """


def min_max(state):
    """
    If we got to a leaf of the tree:
    - if we expanded the tree to the maximum depth possible
    - or if we got to a final game configuration
    """

    if state.depth == 0 or state.board.game_over():
        # we calculate the leaf score
        state.score = state.board.estimate_score(state.depth)
        return state

    # Else, we calculate all the possible moves from the current state

    state.possible_moves = state.state_moves()

    # We apply minMax algorith for all the possible moves,
    score_moves = [min_max(move) for move in state.possible_moves]

    # print(len(score_moves))

    if len(score_moves) == 0:
        print("ii bai")
        return state.parent

    if state.current_player.player_name == Game.PMAX:
        # if the player is MAX, then we choose the state with the maximum score
        state.chosen_state = max(score_moves, key=lambda x: x.score)
    else:
        # if the player is MIN, then we choose the state with the minimun score
        state.chosen_state = min(score_moves, key=lambda x: x.score)

    state.score = state.chosen_state.score
    # print(str(state.chosen_state.depth) + " " + str(state.chosen_state.score) + "\n" + str(state.chosen_state.board))

    return state


def alpha_beta(alpha, beta, state):
    if state.depth == 0 or state.board.game_over():
        state.score = state.board.estimate_score(state.depth)
        return state

    if alpha >= beta:
        # invalid interval
        return state

    # calculate all the possible moves from here
    state.possible_moves = state.state_moves()

    if state.current_player.player_name == Game.PMAX:
        current_score = float('-inf')

        for move in state.possible_moves:
            # we calculate the score
            new_state = alpha_beta(alpha, beta, move)

            if current_score < new_state.score:
                state.chosen_state = new_state
                current_score = new_state.score

            if alpha < new_state.score:
                alpha = new_state.score
                if alpha >= beta:
                    break

    elif state.current_player == Game.PMIN:
        current_score = float('inf')

        for move in state.possible_moves:
            new_state = alpha_beta(alpha, beta, move)

            if current_score > new_state.score:
                state.chosen_state = new_state
                current_score = new_state.score

            if beta > new_state.score:
                beta = new_state.score

                if alpha > beta:
                    break

    state.score = state.chosen_state.score

    return state


def print_if_final(current_state):
    final = current_state.board.game_over()
    if final:
        if final == "remiza":
            print("Remiza!")
        else:
            print("A castigat " + final)

        return True

    return False


def main():
    # initialing
    global algorithm_type
    valid_answer = False
    while not valid_answer:
        algorithm_type = input("Enter the algorithm type (Answer with 1 or 2)\n 1.MiniMax\n 2.Alpha-Beta\n")
        if algorithm_type in ['1', '2']:
            valid_answer = True
        else:
            print("Answer with 1 or 2!")

    # initialing MAXIMUM_DEPTH
    valid_answer = False
    while not valid_answer:
        n = input("Maximum depth of the tree: ")
        if n.isdigit():
            State.MAXIMUM_DEPTH = int(n)
            valid_answer = True
        else:
            print("You must introduce a natural number greater than 0!")

    # initialing players
    Game.PMIN = '1'
    Game.PMAX = '2'

    current_board = Game(default_table, [], Player((1, 1), Game.PMIN), Player((11, 20), Game.PMAX))

    pygame.init()
    pygame.display.set_caption("Bomberman")
    screen = pygame.display.set_mode((750,1334))
    # print("Initial Table")
    # print(str(current_board))

    current_state = State(current_board, current_board.pmax.player_name, State.MAXIMUM_DEPTH)

    while True:
        t_before = int(round(time.time() * 1000))

        if current_state.current_player.player_name == current_board.pmin.player_name:
            # the player moves
            print("                 Protections: " + str(current_state.current_player.number_of_protections) + "\n" +
                  "Current board:   Oponent Protections:" + str(current_state.opposite_player().number_of_protections))
            print(str(current_state.board))
            valid_answer = False
            bomb = None
            new_position = None
            while not valid_answer:
                print("If you want to exit, enter 'q'")
                bomb = input("bomb (y/n): ").lower()

                if bomb not in ['y', 'n']:
                    if bomb == 'q':
                        return 0
                    print("Answer must be y or n!")
                    continue
                direction = input("direction: ").lower()

                if direction == 'w':
                    increment_location = (-1, 0)
                elif direction == "s":
                    increment_location = (1, 0)
                elif direction == "a":
                    increment_location = (0, -1)
                elif direction == "d":
                    increment_location = (0, 1)
                else:
                    print("Answer must be w, a, s or d!")
                    continue

                new_position = add_positions(current_state.current_player.position, increment_location)
                if current_state.board.table[new_position[0]][new_position[1]] in [' ', 'p']:
                    valid_answer = True
                else:
                    print("Can't go there!" + str(current_state.board.table[new_position[0]][new_position[1]]))

            if bomb == 'y':
                current_state.board, current_state.current_player = \
                    current_state.board.player_attacks(current_state.current_player.player_name, new_position[0],
                                                       new_position[1])
            else:
                current_state.board, current_state.current_player = \
                    current_state.board.player_moves(current_state.current_player.player_name, new_position[0],
                                                     new_position[1])

            if print_if_final(current_state):
                break
            t_after = int(round(time.time() * 1000))
            print("Jucatorul a \"gandit\" timp de " + str(t_after - t_before) + " milisecunde.")

        else:
            # JMAX moves
            t_before = int(round(time.time() * 1000))
            if algorithm_type == 1:
                updated_state = min_max(current_state)
            else:
                updated_state = alpha_beta(-5000, 5000, current_state)
            current_state = updated_state.chosen_state
            t_after = int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de " + str(t_after - t_before) + " milisecunde.")
            # current_state.current_player = updated_state.chosen_state.current_player
            # current_state.current_player = updated_state.chosen_state.current_player

        current_state.depth = 3
        current_state.current_player = current_state.opposite_player()


if __name__ == '__main__':
    main()
