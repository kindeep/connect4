from display import *
import sys
import time


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
        if a_move:
            self.display.add_to_animate(Ball(start_rect_click, curr_color, a_move[1], num))
        if a_move:
            return True
        else:
            return False

    def move_player(self, num, player):
        print("Move", player)
        curr_color = Colors.get_tile_color(self.game.turn_count.get_curr_turn())
        a_move = self.click_exec(num, player)
        start_rect_click = pygame.Rect(*self.display.get_box(num, -1))
        if a_move:
            self.display.add_to_animate(Ball(start_rect_click, curr_color, a_move[1], num))
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
        if the_move:
            self.display.add_to_animate(Ball(start_rect_click, curr_color, the_move[1], num))
        if the_move:
            return True
        else:
            return False


def with_ai(ai_player, ply=4):
    curr_game = ConnectGame()

    controller = Controller(curr_game)

    display = Display(curr_game, controller)
    controller.display = display

    display.draw_loop()

    ai_movee = ai_player == Tile.player1

    me_tile = Tile.other_player(ai_player)

    print(ai_player, me_tile)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                click_pos = display.resolve_click(*pos)
                if controller.move_player(click_pos[0], me_tile):
                    ai_movee = True

        display.faster_draw()
        pygame.display.update()
        if ai_movee:
            ai = AIPlayer(curr_game, ply)
            start_time = time.time()
            controller.ai_move(ai.determine_move(), ai_player)
            print("Time taken: ", time.time() - start_time)
            ai_movee = False


def normal_mode():
    curr_game = ConnectGame()

    controller = Controller(curr_game)

    display = Display(curr_game, controller)
    controller.display = display

    display.draw_loop()

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
        with_ai(Tile.player2, ply)
    elif opt2 == 2:
        with_ai(Tile.player1, ply)
    elif opt2 == 3:
        stopgame = True
elif opt == 3:
    stopgame = True
