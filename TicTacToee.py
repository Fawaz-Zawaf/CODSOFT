import copy
import sys
import pygame 
import random
import numpy as np

from constants import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BG_COLOR)

class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))
        self.marked_sqrs = 0

    def final_state(self, show=False):
        
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    pygame.draw.line(screen, color, (col * SQRSIZE + SQRSIZE // 2, 20),
                                     (col * SQRSIZE + SQRSIZE // 2, HEIGHT - 20), LINE_WIDTH)
                return self.squares[0][col]

        
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    pygame.draw.line(screen, color, (20, row * SQRSIZE + SQRSIZE // 2),
                                     (WIDTH - 20, row * SQRSIZE + SQRSIZE // 2), LINE_WIDTH)
                return self.squares[row][0]

        
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[0][0] == 2 else CROSS_COLOR
                pygame.draw.line(screen, color, (20, 20), (WIDTH - 20, HEIGHT - 20), CROSS_WIDTH)
            return self.squares[0][0]

        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[2][0] == 2 else CROSS_COLOR
                pygame.draw.line(screen, color, (20, HEIGHT - 20), (WIDTH - 20, 20), CROSS_WIDTH)
            return self.squares[2][0]

        return 0

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        return [(r, c) for r in range(ROWS) for c in range(COLS) if self.empty_sqr(r, c)]

    def is_full(self):
        return self.marked_sqrs == 9


class AI:
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    def random_move(self, board):
        empty_sqrs = board.get_empty_sqrs()
        return random.choice(empty_sqrs)

    def minimax(self, board, maximizing):
        case = board.final_state()
        if case == 1:
            return 1, None
        if case == 2:
            return -1, None
        if board.is_full():
            return 0, None

        best_move = None
        if maximizing:
            max_eval = -float('inf')
            for (row, col) in board.get_empty_sqrs():
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval_score = self.minimax(temp_board, False)[0]
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = (row, col)
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for (row, col) in board.get_empty_sqrs():
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval_score = self.minimax(temp_board, True)[0]
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = (row, col)
            return min_eval, best_move

    def get_best_move(self, board):
        if self.level == 0:
            return self.random_move(board)
        else:
            return self.minimax(board, False)[1]


class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1
        self.gamemode = 'ai'
        self.running = True
        self.show_lines()

    def show_lines(self):
        screen.fill(BG_COLOR)
        for i in range(1, COLS):
            pygame.draw.line(screen, LINE_COLOR, (i * SQRSIZE, 0), (i * SQRSIZE, HEIGHT), LINE_WIDTH)
            pygame.draw.line(screen, LINE_COLOR, (0, i * SQRSIZE), (WIDTH, i * SQRSIZE), LINE_WIDTH)

    def draw_fig(self, row, col):
        if self.player == 1:
            pygame.draw.line(screen, CROSS_COLOR, (col * SQRSIZE + OFFSET, row * SQRSIZE + OFFSET),
                             (col * SQRSIZE + SQRSIZE - OFFSET, row * SQRSIZE + SQRSIZE - OFFSET), CROSS_WIDTH)
            pygame.draw.line(screen, CROSS_COLOR, (col * SQRSIZE + OFFSET, row * SQRSIZE + SQRSIZE - OFFSET),
                             (col * SQRSIZE + SQRSIZE - OFFSET, row * SQRSIZE + OFFSET), CROSS_WIDTH)
        else:
            pygame.draw.circle(screen, CIRC_COLOR, (col * SQRSIZE + SQRSIZE // 2, row * SQRSIZE + SQRSIZE // 2),
                               RADIUS, CIRC_WIDTH)

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.player = 3 - self.player

    def is_over(self):
        return self.board.final_state(show=True) or self.board.is_full()

    def reset(self):
        self.__init__()


def main():
    game = Game()
    board = game.board
    ai = game.ai

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

                if event.key == pygame.K_e:
                    ai.level = 0

                if event.key == pygame.K_h:
                    ai.level = 1

            if event.type == pygame.MOUSEBUTTONDOWN and game.running:
                row, col = event.pos[1] // SQRSIZE, event.pos[0] // SQRSIZE
                if board.empty_sqr(row, col):
                    game.make_move(row, col)
                    if game.is_over():
                        game.running = False

        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            pygame.display.update()
            row, col = ai.get_best_move(board)
            game.make_move(row, col)
            if game.is_over():
                game.running = False

        pygame.display.update()


main()