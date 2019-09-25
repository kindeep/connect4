import sys
import pygame
from pygame.locals import *
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
    moving_ball_rects: [Ball] = []
    drawn_balls: [Ball] = []

    def __init__(self, game, controller):

        pygame.init()
        pygame.font.init()  # you have to call this at the start,
        # if you want to use this module.
        self.font = pygame.font.SysFont('Times New Roman', self.text_size)

        self.game: ConnectGame = game
        # Change this to just assign to display
        self.controller = controller
        # grid = Grid()

        self.size = self.width, self.height = 800, 600

        self.board_width = self.width
        self.board_height = self.height - 0.2 * self.height

        self.screen = pygame.display.set_mode(self.size)

        self.padding = 0.1

        self.box_width = self.board_width / self.game.get_grid().get_width()
        self.box_height = self.board_height / self.game.get_grid().get_height()

        self.draw_loop()

    def highlight_col(self, num):
        pygame.draw.rect(self.screen, Colors.col_highlight,
                         (num * self.box_width, 0, self.box_width, self.board_height))

    def to_animate(self):
        return len(self.moving_ball_rects) > 0

    # ball_rect: pygame.Rect = (0, 0, 0, 0)

    def animate_drop(self):
        for index, ball_rect in enumerate(self.moving_ball_rects):
            speed = [0, 100]
            ball_rect.rect = ball_rect.rect.move(speed)
            pygame.draw.ellipse(self.screen, ball_rect.color, ball_rect.rect)
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

    def draw_balls(self):
        for ball in self.drawn_balls:
            # print("drawing ball")
            pygame.draw.ellipse(self.screen,
                                Colors.get_tile_color(self.game.get_grid().get(ball.x, ball.y))
                                , self.get_box(ball.x, ball.y))

    def draw_loop(self):
        self.screen.fill(Colors.blue)
        if self.controller.selected != -1:
            self.highlight_col(self.controller.selected)
        self.draw_board()
        self.animate_drop()
        self.draw_info_screen()
        self.draw_balls()
        self.draw_game_status()

    def faster_draw(self):
        # gettting rid of animate...
        for index, ball_rect in enumerate(self.moving_ball_rects):
            self.drawn_balls.append(self.moving_ball_rects[index])
            del self.moving_ball_rects[index]
        self.screen.fill(Colors.blue)
        if self.controller.selected != -1:
            self.highlight_col(self.controller.selected)
        self.draw_grid()
        # self.draw_balls()
        self.draw_info_screen()
        self.draw_game_status()


def move(num, controller):
    move = controller.click_exec(num)
    start_rect_click = pygame.Rect(*display.get_box(num, -1))
    if move:
        display.add_to_animate(Ball(start_rect_click, curr_color, move[1], num))
    if move:
        return True
    else:
        return False


def ai_move(num):
    print("main, determined move: ", num)
    the_move = curr_game.execute_move(int(num))
    start_rect_click = pygame.Rect(*display.get_box(num, -1))
    if the_move:
        display.add_to_animate(Ball(start_rect_click, curr_color, the_move[1], num))
    if the_move:
        return True
    else:
        return False


curr_game = ConnectGame()

controller = Controller(curr_game)

display = Display(curr_game, controller)

ai = AIPlayer(curr_game)

# class ClickPlayer(Player):
#
#
# player1 = ClickPlayer(curr_game)
# player2 = AIPlayer(curr_game)

display.draw_loop()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            curr_color = Colors.get_tile_color(curr_game.turn_count.get_curr_turn())
            pos = pygame.mouse.get_pos()
            click_pos = display.resolve_click(*pos)
            if move(click_pos[0], controller):
                ai_move(ai.determine_move())

    display.faster_draw()
    # display.draw()
    # if display.to_animate():
    # display.draw_loop()
    pygame.display.update()
