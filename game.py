from enum import Enum


class ConnectGame:
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
            for i in range(self.grid.get_height())[::-1]:
                if self.grid.check_empty(pos, i):
                    self.grid.set(pos, i, self.turn_count.get_curr_turn())
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


class Colors():
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
