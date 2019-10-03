# from display import *
import sys
import time
from multiprocessing import Process, Pool

import pygame
# from pygame.locals import *
from game import *


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
    # moving_ball_rects: [Ball] = []
    # drawn_balls: [Ball] = []
    width = 500
    height = 400

    def __init__(self, game, controller):
        pygame.init()
        pygame.font.init()  # you have to call this at the start,
        # if you want to use this module.
        self.font = pygame.font.SysFont('Times New Roman', self.text_size)

        self.game: ConnectGame = game
        # Change this to just assign to display
        self.controller = controller
        # grid = Grid()

        self.size = self.width, self.height
        # self.size = self.width, self.height = 800, 600

        self.board_width = self.width
        self.board_height = self.height - 0.2 * self.height

        self.screen = pygame.display.set_mode(self.size)

        self.padding = 0.1

        self.box_width = self.board_width / self.game.get_grid().get_width()
        self.box_height = self.board_height / self.game.get_grid().get_height()

        # self.draw_loop()

    def highlight_col(self, num):
        pygame.draw.rect(self.screen, Colors.col_highlight,
                         (num * self.box_width, 0, self.box_width, self.board_height))

    # def to_animate(self):
    #     return len(self.moving_ball_rects) > 0

    # ball_rect: pygame.Rect = (0, 0, 0, 0)

    # def animate_drop(self):
    # for index, ball_rect in enumerate(self.moving_ball_rects):
    #     speed = [0, 100]
    #     ball_rect.rect = ball_rect.rect.move(speed)
    #     pygame.draw.ellipse(self.screen, ball_rect.color, ball_rect.rect)
    #     if ball_rect.rect[1] > (ball_rect.y * self.box_height):
    #         self.drawn_balls.append(self.moving_ball_rects[index])
    #         del self.moving_ball_rects[index]
    #
    # def add_to_animate(self, ball: Ball):
    #     self.moving_ball_rects.append(ball)

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
                # print(index, pos)
                pygame.draw.ellipse(self.screen, Colors.victory_tile_highlight,
                                    self.get_box(pos[0], pos[1],
                                                 self.box_width * 0.6, self.box_height * 0.6))
                # pygame.draw.ellipse(self.screen, Colors.col_highlight, self.get_box(*pos))

    def resolve_click(self, x, y):
        # print(x, y)
        return int(x / self.box_width), int(y / self.box_height)

    def draw_info_screen(self):
        self.padx = self.info_padding * self.width
        self.pady = self.info_padding * self.height
        self.info_rect = (self.padx, self.board_height + self.pady, self.width - (2 * self.padx),
                          self.height - self.board_height - (2 * self.pady))
        pygame.draw.rect(self.screen, Colors.info, self.info_rect)
        # if not self.text_drawn:
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

    # def draw_balls(self):
    #     for ball in self.drawn_balls:
    #         # print("drawing ball")
    #         pygame.draw.ellipse(self.screen,
    #                             Colors.get_tile_color(self.game.get_grid().get(ball.x, ball.y))
    #                             , self.get_box(ball.x, ball.y))

    # def draw_loop(self):
    #     self.screen.fill(Colors.blue)
    #     if self.controller.selected != -1:
    #         self.highlight_col(self.controller.selected)
    #     self.draw_board()
    #     # self.animate_drop()
    #     self.draw_info_screen()
    #     # self.draw_balls()
    #     self.draw_game_status()

    def faster_draw(self):
        # gettting rid of animate...
        # for index, ball_rect in enumerate(self.moving_ball_rects):
        #     self.drawn_balls.append(self.moving_ball_rects[index])
        #     del self.moving_ball_rects[index]
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
        # # print(self.selected)
        result = False
        if self.selected != -1:
            print("Selected not -1?")
            print(self.game.turn_count.curr_player, player)
            if self.game.turn_count.curr_player == player:
                result = self.game.execute_move(self.selected)
        self.reset_selection()
        # # print(self.selected)
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
        # if a_move:
        # self.display.add_to_animate(Ball(start_rect_click, curr_color, a_move[1], num))
        if a_move:
            return True
        else:
            return False

    def move_player(self, num, player):
        print("Move", player)
        curr_color = Colors.get_tile_color(self.game.turn_count.get_curr_turn())
        a_move = self.click_exec(num, player)
        start_rect_click = pygame.Rect(*self.display.get_box(num, -1))
        # if a_move:
        # self.display.add_to_animate(Ball(start_rect_click, curr_color, a_move[1], num))
        if a_move:
            return True
        else:
            return False

    def ai_move(self, num, player):
        curr_color = Colors.get_tile_color(self.game.turn_count.get_curr_turn())
        print("main, determined move: ", num)
        print("main, board before move: ", self.game.grid.to_string())
        the_move = self.game.execute_move(int(num), player)
        start_rect_click = pygame.Rect(*self.display.get_box(num, -1))
        # if the_move:
        #     self.display.add_to_animate(Ball(start_rect_click, curr_color, the_move[1], num))
        if the_move:
            return True
        else:
            return False


def with_ai(ai_player, ply=4):
    curr_game = ConnectGame()

    controller = Controller(curr_game)

    display = Display(curr_game, controller)
    controller.display = display

    # display.draw_loop()

    ai_movee = ai_player == Tile.player1

    me_tile = Tile.other_player(ai_player)

    print(ai_player, me_tile)

    pygame.display.flip()
    display.faster_draw()
    display.faster_draw()
    pygame.display.flip()
    display.faster_draw()
    pygame.display.flip()

    while True:
        if ai_movee:
            ai = AIPlayer(curr_game, ply)
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

        print("Should update display...")
        print(curr_game.grid.to_string())


def normal_mode():
    curr_game = ConnectGame()

    controller = Controller(curr_game)

    display = Display(curr_game, controller)
    controller.display = display

    # display.draw_loop()

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
# opt = int(input("1. PvP, 2. Play against AI, 3. Exit: "))
if opt == 1:
    normal_mode()
elif opt == 2:
    ply = int_input("Select difficulty (ply): ", 4)
    if not ply > 0:
        ply = 4
    opt2 = int_input("1. player first, 2. AI first, 3. Exit: ")
    if opt2 == 1:
        # Process(target=with_ai(Tile.player2, ply)).start()
        with_ai(Tile.player2, ply)
    elif opt2 == 2:
        # Process(target=with_ai(Tile.player1, ply)).start()
        with_ai(Tile.player1, ply)
    elif opt2 == 3:
        stopgame = True
elif opt == 3:
    stopgame = True
