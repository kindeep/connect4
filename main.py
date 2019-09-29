from display import *
import sys
import time


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

    def execute_turn(self, player=None):
        if not player:
            player = self.game.turn_count.curr_player
        # # print(self.selected)
        result = False
        if self.selected != -1:
            if self.game.turn_count.curr_player == player:
                # print("Selected not -1?")
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


def move(num, controller):
    a_move = controller.click_exec(num)
    start_rect_click = pygame.Rect(*display.get_box(num, -1))
    if a_move:
        display.add_to_animate(Ball(start_rect_click, curr_color, a_move[1], num))
    if a_move:
        return True
    else:
        return False


def move_player(num, controller, player):
    a_move = controller.click_exec(num, player)
    start_rect_click = pygame.Rect(*display.get_box(num, -1))
    if a_move:
        display.add_to_animate(Ball(start_rect_click, curr_color, a_move[1], num))
    if a_move:
        return True
    else:
        return False


def ai_move(num, player):
    print("main, determined move: ", num)
    print("main, board before move: ", curr_game.grid.to_string())
    the_move = curr_game.execute_move(int(num), player)
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

display.draw_loop()

ai_movee = False

ai_tile = Tile.player2

me_tile = Tile.player1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            curr_color = Colors.get_tile_color(curr_game.turn_count.get_curr_turn())
            pos = pygame.mouse.get_pos()
            click_pos = display.resolve_click(*pos)
            if move_player(click_pos[0], controller, me_tile):
                ai_movee = True

    display.faster_draw()
    pygame.display.update()
    if ai_movee:
        ai = AIPlayer(curr_game)
        start_time = time.time()
        ai_move(ai.determine_move(), ai_tile)
        print("Time taken: ", time.time() - start_time)
        ai_movee = False
