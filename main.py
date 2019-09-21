import sys
import pygame
from pygame.locals import *
from enum import Enum


class Ball:
    rect: pygame.Rect
    color = (0, 0, 0)
    y: int
    x: int

    def __init__(self, rect, color, y, x):
        self.rect = rect
        self.color = color
        self.y = y
        self.x = x


class Display:
    info_padding: int = 0.01
    text_size = 30
    moving_ball_rects: [Ball] = []
    drawn_balls: [Ball] = []

    def __init__(self, game):
        pygame.init()
        pygame.font.init()  # you have to call this at the start,
        # if you want to use this module.
        self.font = pygame.font.SysFont('Times New Roman', self.text_size)

        self.game: ConnectGame = game

        # grid = Grid()

        self.size = self.width, self.height = 800, 600

        self.board_width = self.width
        self.board_height = self.height - 0.2 * self.height

        self.screen = pygame.display.set_mode(self.size)

        self.padding = 0.1

        self.box_width = self.board_width / grid.get_width()
        self.box_height = self.board_height / grid.get_height()

        self.draw()

    def highlight_col(self, num):
        pygame.draw.rect(self.screen, Colors.col_highlight,
                         (num * self.box_width, 0, self.box_width, self.board_height))

    # ball_rect: pygame.Rect = (0, 0, 0, 0)

    def animate_drop(self):
        for index, ball_rect in enumerate(self.moving_ball_rects):
            speed = [0, 10]
            # self.ball_rect = pygame.Rect(self.ball_rect)
            # print(ball_rect.rect)
            ball_rect.rect = ball_rect.rect.move(speed)
            pygame.draw.ellipse(self.screen, ball_rect.color, ball_rect.rect)
            # pygame.draw.ellipse(self.screen, Colors.white, self.get_box(ball_rect.y, ball_rect.x))
            center = self.get_center(*ball_rect.rect)
            if ball_rect.rect[1] > (ball_rect.y * self.box_height):
                self.drawn_balls.append(self.moving_ball_rects[index])
                del self.moving_ball_rects[index]

    def add_to_animate(self, ball: Ball):
        self.moving_ball_rects.append(ball)

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
        # cir_width = self.box_width - self.padding * self.box_width * 2
        # cir_width = radius
        # cir_height = self.box_height - self.padding * self.box_height * 2
        # cir_height = radius
        return (
            x - cir_width / 2,
            y - cir_height / 2,
            cir_width,
            cir_height
        )

    def draw_game_status(self):
        if self.game.game_over:
            padx = self.info_padding * self.width
            pady = self.info_padding * self.height
            info_rect = (padx, self.board_height + pady, self.width - (2 * padx),
                         self.height - self.board_height - (2 * pady))
            pygame.draw.rect(self.screen, Colors.info, info_rect)
            # if not self.text_drawn:
            text = "Game Over, winner: "
            self.screen.blit(self.font.render(text, False, (0, 0, 0)),
                             (info_rect[0] + padx, self.height - 2 * padx - self.text_size))
            font_rect = self.font.size(text)
            turn_rect = (
                info_rect[0] + padx + font_rect[0],
                self.height - 2 * padx - self.text_size,
                font_rect[1],
                font_rect[1])
            pygame.draw.ellipse(self.screen, Colors.get_tile_color(self.game.victory), turn_rect)

            for index, pos in enumerate(self.game.victory_positions):
                # print(index, pos)
                pygame.draw.ellipse(self.screen, Colors.victory_tile_highlight,
                                    self.get_box(pos[0], pos[1],
                                                 self.box_width * 0.6, self.box_height * 0.6))
                # pygame.draw.ellipse(self.screen, Colors.col_highlight, self.get_box(*pos))

    def resolve_click(self, x, y):
        # print(x, y)
        return int(x / self.box_width), int(y / self.box_height)

    def draw_info_screen(self):
        padx = self.info_padding * self.width
        pady = self.info_padding * self.height
        info_rect = (padx, self.board_height + pady, self.width - (2 * padx),
                     self.height - self.board_height - (2 * pady))
        pygame.draw.rect(self.screen, Colors.info, info_rect)
        # if not self.text_drawn:
        text = "Turn: "
        self.screen.blit(self.font.render(text, False, (0, 0, 0)),
                         (info_rect[0] + padx, self.height - 2 * padx - self.text_size))
        font_rect = self.font.size(text)
        turn_rect = (
            info_rect[0] + padx + font_rect[0],
            self.height - 2 * padx - self.text_size,
            font_rect[1],
            font_rect[1])
        pygame.draw.ellipse(self.screen, Colors.get_tile_color(self.game.turn_count.curr_player), turn_rect)

    def draw_board(self):
        for x in range(grid.get_width()):
            for y in range(grid.get_height()):
                pygame.draw.ellipse(self.screen,
                                    Colors.white
                                    , self.get_box(x, y))
                # pygame.draw.ellipse(self.screen,
                #                     Colours.get_tile_color(grid.get(x, y))
                #                     , self.get_box(x, y))

    def draw_balls(self):
        for ball in self.drawn_balls:
            # print("drawing ball")
            pygame.draw.ellipse(self.screen,
                                Colors.get_tile_color(grid.get(ball.x, ball.y))
                                , self.get_box(ball.x, ball.y))

    def draw(self):
        self.screen.fill(Colors.blue)
        if self.game.controller.selected != -1:
            self.highlight_col(self.game.controller.selected)

        self.draw_board()
        self.draw_info_screen()
        self.animate_drop()
        self.draw_balls()
        self.draw_game_status()


class Controller:
    selected = -1

    def __init__(self, game):
        self.game: ConnectGame = game
        self.reset_selection()

    def select(self, position: int) -> bool:
        if (position >= 0 and position < self.game.grid.get_width()):
            self.selected = position
            return True
        else:
            return False

    def reset_selection(self):
        self.selected = -1

    def execute_turn(self):
        # print(self.selected)
        result = False
        if self.selected != -1:
            # print("Selected not -1?")
            result = self.game.execute_move(self.selected)
        self.reset_selection()
        # print(self.selected)
        return result

    def set_selection(self, x) -> bool:
        # print("set?")
        if x >= 0 and x < self.game.get_grid().get_width():
            self.selected = x
            return True
        else:
            return False

    def click_exec(self, x):
        if x >= 0 and x < self.game.get_grid().get_width():
            if self.selected == x:
                return self.execute_turn()
            else:
                self.set_selection(x)
                return False
        else:
            return False


class ConnectGame:
    # controller: Controller
    victory = None
    game_over = False
    victory_positions = None

    def __init__(self):
        self.controller: Controller = Controller(self)
        self.grid = Grid()
        self.turn_count = MoveTracker()

    def execute_move(self, pos):
        if not self.game_over:
            result = False
            for i in range(grid.get_height())[::-1]:
                if grid.check_empty(pos, i):
                    # print("Set ", pos, i, " to ", self.turn_count.get_curr_turn())
                    grid.set(pos, i, self.turn_count.get_curr_turn())
                    self.turn_count.next_turn()
                    result = pos, i
                    break

            if result:
                if self.check_connected(*result):
                    self.game_over = True
                    self.victory = self.grid.get(*result)

            if (result):
                return result

    def check_connected(self, x, y):
        # bools[0] = True
        # bools[1] = True
        # bools[2] = True
        # bools[3] = True
        # bools[3] = True
        # bools[3] = True
        # bools[3] = True
        # bools[3] = True

        bools = [True] * 8
        positions = [[], [], [], [], [], [], [], []]

        check_against = self.grid.get(x, y)
        if check_against != Tile.empty:
            for i in range(4):
                tp = x + i, y
                bools[0] = bools[0] and self.grid.get(*tp) == check_against
                positions[0].append(tp)

                tp = x - i, y
                bools[1] = bools[1] and self.grid.get(*tp) == check_against
                positions[1].append(tp)

                tp = x, y + i
                bools[2] = bools[2] and self.grid.get(*tp) == check_against
                positions[2].append(tp)

                tp = x, y - i
                bools[3] = bools[3] and self.grid.get(*tp) == check_against
                positions[3].append(tp)

                tp = x + i, y + i
                bools[4] = bools[4] and self.grid.get(*tp) == check_against
                positions[4].append(tp)

                tp = x - i, y - i
                bools[5] = bools[5] and self.grid.get(*tp) == check_against
                positions[5].append(tp)

                tp = x - i, y + i
                bools[6] = bools[6] and self.grid.get(*tp) == check_against
                positions[6].append(tp)

                tp = x + i, y - i
                bools[7] = bools[7] and self.grid.get(*tp) == check_against
                positions[7].append(tp)

            result = False
            for index, b in enumerate(bools):
                result = result or b
                # print("Wut", index, positions[index])
                if b:
                    self.victory_positions = positions[index]

            return result

    def get_grid(self):
        return self.grid

    def check_victory(self):
        # vertical check
        found_chain = 0
        player = Tile.player1
        for x in range(self.grid.get_width()):
            for y in range(self.grid.get_height()):
                if self.grid.get(x, y) == player:
                    found_chain = found_chain + 1
                else:
                    found_chain = 0
                if found_chain == 4:
                    return True

        for y in range(self.grid.get_height()):
            for x in range(self.grid.get_width()):
                if self.grid.get(x, y) == player:
                    found_chain = found_chain + 1
                else:
                    found_chain = 0
                if found_chain == 4:
                    return True


class Tile(Enum):
    player1 = 0
    player2 = 1
    empty = 2
    out_of_bounds = 3


class MoveTracker:
    curr_player = Tile.player1

    def __init__(self, player2first=False):
        if player2first: self.curr_player = Tile.player2

    def next_turn(self):
        self.curr_player = Tile.player1 if self.curr_player == Tile.player2 else Tile.player2
        return self.curr_player

    def curr_turn_player1(self):
        return self.curr_player == Tile.player2

    def curr_turn_player2(self):
        return self.curr_player == Tile.player1

    def get_curr_turn(self):
        return self.curr_player


class Grid:
    array = [
        [Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty],
        [Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty],
        [Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty],
        [Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty],
        [Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty],
        [Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty],
    ]

    def get_width(self) -> int:
        return 7

    def get_height(self) -> int:
        return 6

    def check_player1(self, x, y) -> bool:
        return self.array[y][x] == Tile.player1

    def check_player2(self, x, y) -> bool:
        return self.array[y][x] == Tile.player2

    def check_empty(self, x, y) -> bool:
        return self.array[y][x] == Tile.empty

    def set(self, x, y, val):
        self.array[y][x] = val

    def get(self, x, y):
        if x < self.get_width() and y < self.get_height():
            return self.array[y][x]
        else:
            return Tile.out_of_bounds

    def __str__(self):
        return str(self.array)
    # def __init__(self):


class Colors:
    victory_tile_highlight = 0, 255, 255
    yellow = 255, 200, 0
    red = 200, 0, 0
    blue = 0, 0, 255
    black = 0, 0, 0
    white = 255, 255, 255
    info = 200, 200, 200
    col_highlight = 100, 100, 230

    def get_tile_color(tile: Tile):
        if tile == Tile.player2:
            return Colors.red
        if tile == Tile.player1:
            return Colors.yellow
        else:
            return Colors.white


# pygame.init()
# 
# # grid = Grid()
# 
# size = width, height = 800, 600
# 
# self.board_width = width
# board_height = height - 0.2 * height
# 
# screen = pygame.display.set_mode(size)
# 
# screen.fill(Colours.blue)
# self.padding = 0.1


curr_game = ConnectGame()

grid = curr_game.get_grid()

display = Display(curr_game)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            curr_color = Colors.get_tile_color(curr_game.turn_count.get_curr_turn())
            pos = pygame.mouse.get_pos()
            click_pos = display.resolve_click(*pos)
            # print(click_pos)
            # curr_game.controller.set_selection(click_pos[0])
            move = curr_game.controller.click_exec(click_pos[0])
            # start_rect_click = pygame.Rect(click_pos[0] * display.box_width, - display.box_width, display.box_width, display.box_height)
            start_rect_click = pygame.Rect(*display.get_box(click_pos[0], -1))
            # print(curr_game.get_grid())
            if move:
                display.add_to_animate(Ball(start_rect_click, curr_color, move[1], click_pos[0]))
    display.draw()
    pygame.display.update()
