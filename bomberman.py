from state import State
from player import Player
from game import Game
from pygame.locals import *
import pygame
import sys
import time

default_table = [
    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
    ['#', '1', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', ' ', '#', ' ', ' ', ' ', '#', '#', '#', ' ', ' ', ' ', '#', '#', '#', '#', ' ', '#', '#', '#', '#', '#'],
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

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)


def add_positions(p1, p2):
    return p1[0] + p2[0], p1[1] + p2[1]


def draw_game(display, config):
    h_gr = 60
    w_gr = 65

    font = pygame.font.Font('freesansbold.ttf', 50)
    text = font.render(str(config.pmin.number_of_protections), False, white)

    explosion_img = pygame.image.load('B:\\Desk\\facultate-sem-2\\IA\\Bomberman\\explosion.png')
    explosion_img = pygame.transform.scale(explosion_img, (w_gr, h_gr))

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

    protection_img = pygame.image.load('B:\\Desk\\facultate-sem-2\\IA\\Bomberman\\protection.png')
    protection_img = pygame.transform.scale(protection_img, (w_gr, h_gr))

    drt = []
    for row in range(len(config.table)):
        for col in range(len(config.table[0])):
            patr = pygame.Rect(col * (w_gr + 1), row * (h_gr + 1), w_gr, h_gr)
            drt.append(patr)
            pygame.draw.rect(display, (255, 255, 255), patr)
            if config.table[row][col] == '#':
                display.blit(wall_img, (col * w_gr, row * h_gr))
            elif config.table[row][col] == ' ':
                display.blit(space_img, (col * w_gr, row * h_gr))
            elif config.table[row][col] == 'b':
                display.blit(bomb_img, (col * w_gr, row * h_gr))
            elif config.table[row][col] == '1':
                display.blit(player1_img, (col * w_gr, row * h_gr))
            elif config.table[row][col] == '2':
                display.blit(player2_img, (col * w_gr, row * h_gr))
            elif config.table[row][col] == 'p':
                display.blit(protection_img, (col * w_gr, row * h_gr))
            elif config.table[row][col] == 'a':
                display.blit(explosion_img, (col * w_gr, row * h_gr))
    display.blit(text, (0, 0))

    pygame.display.flip()
    return drt


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
            print("Draw!")
        else:
            print("Player " + final + " won!")
        return True
    return False


def main():
    # initialing
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
    screen = pygame.display.set_mode((1500, 800))

    # print("Initial Table")
    # print(str(current_board))

    current_state = State(current_board, current_board.pmax.player_name, State.MAXIMUM_DEPTH)

    font = pygame.font.Font('freesansbold.ttf', 50)
    text = font.render(str(current_state.board.pmin), True, green, blue)
    text_rect = text.get_rect()
    text_rect.center = (400, 200)
    squares = draw_game(screen, current_state.board)

    bomb = 'n'

    while True:
        t_before = int(round(time.time() * 1000))
        for bomb_activated in current_state.board.bombs:
            if bomb_activated.activated:
                current_state.board.table[bomb_activated.position[0]][bomb_activated.position[1]] = ' '
                current_state.board.bombs.remove(bomb_activated)
                bomb_activated.owner.bomb_dropped = None
        if current_state.current_player.player_name == current_board.pmin.player_name:
            # the player moves
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:

                    increment_location = None

                    if event.key == K_b:
                        print("bomb")
                        bomb = 'y'
                        continue
                    if event.key == K_w:
                        increment_location = (-1, 0)
                    elif event.key == K_s:
                        increment_location = (1, 0)
                    elif event.key == K_a:
                        increment_location = (0, -1)
                    elif event.key == K_d:
                        increment_location = (0, 1)
                    if increment_location:
                        new_position = add_positions(current_state.current_player.position, increment_location)
                        if current_state.board.table[new_position[0]][new_position[1]] in [' ', 'p']:
                            if bomb == 'y':
                                current_state.board, current_state.current_player = \
                                    current_state.board.player_attacks(current_state.current_player.player_name,
                                                                       new_position[0],
                                                                       new_position[1])
                                bomb = 'n'
                            else:
                                current_state.board, current_state.current_player = \
                                    current_state.board.player_moves(current_state.current_player.player_name,
                                                                     new_position[0],
                                                                     new_position[1])
                            if print_if_final(current_state):
                                pygame.quit()
                                sys.exit()
                                break

                            t_after = int(round(time.time() * 1000))
                            print("The player taught for " + str(t_after - t_before) + " miliseconds.")
                            current_state.depth = 3
                            current_state.current_player = current_state.opposite_player()
        else:
            # JMAX moves
            t_before = int(round(time.time() * 1000))
            if algorithm_type == '1':
                updated_state = min_max(current_state)
            else:
                updated_state = alpha_beta(-5000, 5000, current_state)
            current_state = updated_state.chosen_state
            draw_game(screen, current_state.board)

            t_after = int(round(time.time() * 1000))
            print("The AI taught " + str(t_after - t_before) + " miliseconds.")
            # print("Scor " + str(current_state.score))
            # current_state.current_player = updated_state.chosen_state.current_player
            # current_state.current_player = updated_state.chosen_state.current_player
            current_state.depth = 3
            current_state.current_player = current_state.opposite_player()

    """Without pygame"""

    # while True:
    #     t_before = int(round(time.time() * 1000))
    #     for bomb_activated in current_state.board.bombs:
    #         if bomb_activated.activated:
    #             if not current_state.board.is_player_safe(Game.PMAX, bomb_activated.position):
    #                 current_state.board.pmax.number_of_protections -= 1
    #             if not current_state.board.is_player_safe(Game.PMIN, bomb_activated.position):
    #                 current_state.board.pmin.number_of_protections -= 1
    #
    #             current_state.board.table[bomb_activated.position[0]][bomb_activated.position[1]] = ' '
    #             current_state.board.bombs.remove(bomb_activated)
    #             bomb_activated.owner.bomb_dropped = None
    #
    #     if current_state.current_player.player_name == current_board.pmin.player_name:
    #         print("                 Protections: " + str(current_state.current_player.number_of_protections) + "\n" +
    #               "Current board:   Oponent Protections:" + str(current_state.opposite_player().number_of_protections))
    #         print(str(current_state.board))
    #         valid_answer = False
    #         bomb = None
    #         new_position = None
    #         while not valid_answer:
    #             print("If you want to exit, enter 'q'")
    #             bomb = input("Do you want to attack? (y/n): ").lower()
    #
    #             if bomb not in ['y', 'n']:
    #                 if bomb == 'q':
    #                     return 0
    #                 print("Answer must be y or n!")
    #                 continue
    #             direction = input("direction: ").lower()
    #
    #             if direction == 'w':
    #                 increment_location = (-1, 0)
    #             elif direction == "s":
    #                 increment_location = (1, 0)
    #             elif direction == "a":
    #                 increment_location = (0, -1)
    #             elif direction == "d":
    #                 increment_location = (0, 1)
    #             else:
    #                 print("Answer must be w, a, s or d!")
    #                 continue
    #
    #             new_position = add_positions(current_state.current_player.position, increment_location)
    #             if current_state.board.table[new_position[0]][new_position[1]] in [' ', 'p']:
    #                 valid_answer = True
    #             else:
    #                 print("Can't go there!" + str(current_state.board.table[new_position[0]][new_position[1]]))
    #
    #         if bomb == 'y':
    #             current_state.board, current_state.current_player = \
    #                 current_state.board.player_attacks(current_state.current_player.player_name, new_position[0],
    #                                                    new_position[1])
    #         else:
    #             current_state.board, current_state.current_player = \
    #                 current_state.board.player_moves(current_state.current_player.player_name, new_position[0],
    #                                                  new_position[1])



if __name__ == '__main__':
    main()
