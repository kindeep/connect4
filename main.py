# from display import *
import sys
import time

import pygame
from game import *


# this file mostly just had display stuff. Actual heuristic, minmax algo and game logic is in game.py

# Just stores rgb values for colours.
class Colors:
    victory_tile_highlight = 0, 255, 255
    yellow = 255, 200, 0
    red = 200, 0, 0
    blue = 0, 0, 255
    black = 0, 0, 0
    white = 255, 255, 255
    info = 200, 200, 200
    col_highlight = 100, 100, 230

    @staticmethod
    def get_tile_color(tile: Tile):
        if tile == Tile.player2:
            return Colors.red
        if tile == Tile.player1:
            return Colors.yellow
        else:
            return Colors.white


class Display:
    info_padding: int = 0.01
    text_size = 30
    width = 500
    height = 400

    def __init__(self, game, controller):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont('Times New Roman', self.text_size)
        self.game: ConnectGame = game
        self.controller = controller
        self.size = self.width, self.height
        self.board_width = self.width
        self.board_height = self.height - 0.2 * self.height
        self.screen = pygame.display.set_mode(self.size)
        self.padding = 0.1
        self.box_width = self.board_width / self.game.get_grid().get_width()
        self.box_height = self.board_height / self.game.get_grid().get_height()

    def highlight_col(self, num):
        pygame.draw.rect(self.screen, Colors.col_highlight,
                         (num * self.box_width, 0, self.box_width, self.board_height))

    def get_center(self, left, top, width, height):
        return left + width / 2, top + height / 2

    def get_box(self, x_grid, y_grid, width=None, height=None):
        if not width:
            width = self.box_width - self.padding * self.box_width * 2
        if not height:
            height = self.box_height - self.padding * self.box_height * 2
        return (
            x_grid * self.box_width + (self.box_width - width) / 2,
            y_grid * self.box_height + (self.box_height - height) / 2,
            width, height)

    def get_ball_rect(self, x, y, cir_width, cir_height):
        return (
            x - cir_width / 2,
            y - cir_height / 2,
            cir_width,
            cir_height
        )

    def draw_game_status(self):
        if self.game.game_over:
            # if not self.text_drawn:
            text = "Game Over, winner: "
            self.screen.blit(self.font.render(text, False, (0, 0, 0)),
                             (self.info_rect[0] + self.padx, self.height - 2 * self.padx - self.text_size))
            font_rect = self.font.size(text)
            turn_rect = (
                self.info_rect[0] + self.padx + font_rect[0],
                self.height - 2 * self.padx - self.text_size,
                font_rect[1],
                font_rect[1])
            pygame.draw.ellipse(self.screen, Colors.get_tile_color(self.game.victory_player), turn_rect)

            for index, pos in enumerate(self.game.victory_positions):
                pygame.draw.ellipse(self.screen, Colors.victory_tile_highlight,
                                    self.get_box(pos[0], pos[1],
                                                 self.box_width * 0.6, self.box_height * 0.6))

    def resolve_click(self, x, y):
        # print(x, y)
        return int(x / self.box_width), int(y / self.box_height)

    def draw_info_screen(self):
        self.padx = self.info_padding * self.width
        self.pady = self.info_padding * self.height
        self.info_rect = (self.padx, self.board_height + self.pady, self.width - (2 * self.padx),
                          self.height - self.board_height - (2 * self.pady))
        pygame.draw.rect(self.screen, Colors.info, self.info_rect)
        text = "Turn: "
        self.screen.blit(self.font.render(text, False, (0, 0, 0)),
                         (self.info_rect[0] + self.padx, self.height - 2 * self.padx - self.text_size))
        font_rect = self.font.size(text)
        turn_rect = (
            self.info_rect[0] + self.padx + font_rect[0],
            self.height - 2 * self.padx - self.text_size,
            font_rect[1],
            font_rect[1])
        pygame.draw.ellipse(self.screen, Colors.get_tile_color(self.game.turn_count.curr_player), turn_rect)

    def draw_board(self):
        for x in range(self.game.get_grid().get_width()):
            for y in range(self.game.get_grid().get_height()):
                pygame.draw.ellipse(self.screen,
                                    Colors.white
                                    , self.get_box(x, y))

    def draw_grid(self):
        for x in range(self.game.get_grid().get_width()):
            for y in range(self.game.get_grid().get_height()):
                pygame.draw.ellipse(self.screen,
                                    Colors.get_tile_color(self.game.grid.get(x, y))
                                    , self.get_box(x, y))

    def faster_draw(self):
        self.screen.fill(Colors.blue)
        if self.controller.selected != -1:
            self.highlight_col(self.controller.selected)
        self.draw_grid()
        # self.draw_balls()
        self.draw_info_screen()
        self.draw_game_status()
        self.padx = self.info_padding * self.width
        pady = self.info_padding * self.height
        info_rect = (self.padx, self.board_height + pady, self.width - (2 * self.padx),
                     self.height - self.board_height - (2 * pady))
        pygame.draw.rect(self.screen, Colors.info, info_rect)


class Controller:
    selected = -1

    def __init__(self, game, display=None):
        self.display: Display = display
        self.game: ConnectGame = game
        self.reset_selection()

    def select(self, position: int) -> bool:
        if position >= 0 and position < self.game.grid.get_width():
            self.selected = position
            return True
        else:
            return False

    def reset_selection(self):
        self.selected = -1

    def execute_turn(self, player=None):
        if not player:
            player = self.game.turn_count.curr_player
        result = False
        if self.selected != -1:
            if self.game.turn_count.curr_player == player:
                result = self.game.execute_move(self.selected)
        self.reset_selection()
        return result

    def set_selection(self, x) -> bool:
        # # print("set?")
        if x >= 0 and x < self.game.get_grid().get_width():
            self.selected = x
            return True
        else:
            return False

    def click_exec(self, x, player=None):
        if not player:
            player = self.game.turn_count.curr_player
        if x >= 0 and x < self.game.get_grid().get_width():
            if self.selected == x:
                return self.execute_turn(player)
            else:
                self.set_selection(x)
                return False
        else:
            return False

    def move(self, num):
        curr_color = Colors.get_tile_color(self.game.turn_count.get_curr_turn())
        a_move = self.click_exec(num)
        start_rect_click = pygame.Rect(*self.display.get_box(num, -1))
        if a_move:
            return True
        else:
            return False

    def move_player(self, num, player):
        curr_color = Colors.get_tile_color(self.game.turn_count.get_curr_turn())
        a_move = self.click_exec(num, player)
        start_rect_click = pygame.Rect(*self.display.get_box(num, -1))
        if a_move:
            return True
        else:
            return False

    def ai_move(self, num, player):
        curr_color = Colors.get_tile_color(self.game.turn_count.get_curr_turn())
        the_move = self.game.execute_move(int(num), player)
        start_rect_click = pygame.Rect(*self.display.get_box(num, -1))
        if the_move:
            return True
        else:
            return False


def with_ai(ai_player, ply=4):
    curr_game = ConnectGame()
    controller = Controller(curr_game)
    display = Display(curr_game, controller)
    controller.display = display
    ai_movee = ai_player == Tile.player1
    me_tile = Tile.other_player(ai_player)

    pygame.display.flip()
    display.faster_draw()

    while True:
        if ai_movee:
            ai = AIPlayer(curr_game, ply, playerType=ai_player)
            start_time = time.time()
            controller.ai_move(ai.determine_move(), ai_player)
            print("Time taken: ", time.time() - start_time)
            ai_movee = False
            display.faster_draw()
            pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and not ai_movee:
                display.faster_draw()
                pygame.display.flip()
                pos = pygame.mouse.get_pos()
                click_pos = display.resolve_click(*pos)
                if controller.move_player(click_pos[0], me_tile):
                    ai_movee = True
                display.faster_draw()
                pygame.display.flip()


def normal_mode():
    curr_game = ConnectGame()

    controller = Controller(curr_game)

    display = Display(curr_game, controller)
    controller.display = display

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                click_pos = display.resolve_click(*pos)
                controller.click_exec(click_pos[0])

        display.faster_draw()
        pygame.display.update()


def int_input(str, default=None):
    while True:
        try:
            return int(input(str))
        except:
            if not default:
                print("Invalid input, expected integer. Please try again. ")
                continue
            else:
                return default


opt = int_input("1. PvP, 2. Play against AI, 3. Exit: ")
if opt == 1:
    normal_mode()
elif opt == 2:
    ply = int_input("Select difficulty (ply): ", 4)
    if not ply > 0:
        ply = 4
    opt2 = int_input("1. player first, 2. AI first, 3. Exit: ")
    if opt2 == 1:
        with_ai(Tile.player2, ply)
    elif opt2 == 2:
        with_ai(Tile.player1, ply)
    elif opt2 == 3:
        stopgame = True
elif opt == 3:
    stopgame = True
