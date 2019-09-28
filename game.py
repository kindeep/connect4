from enum import Enum
import random
import copy
import numpy as np


class ConnectGame:
    victory_player = None
    game_over = False
    victory_positions = None
    D1 = 1, 1
    D2 = -1, 1
    H = 0, 1
    V = 1, 0

    def __copy__(self):
        result = ConnectGame()
        result.turn_count = copy.copy(self.turn_count)
        result.grid = copy.copy(self.grid)
        result.game_over = self.game_over
        result.victory_player = self.victory_player
        result.victory_positions = self.victory_positions
        return result

    def __init__(self):
        # self.controller: Controller = Controller(self)
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
                # print("resutl in exec move", result)
                if self.check_connected2(*result):
                    self.game_over = True
                    self.victory_player = self.grid.get(*result)
                    # self.victory_player =

            if (result):
                return result
        else:
            # still does next turn, remove this later.
            self.turn_count.next_turn()

    def check_connected2(self, x, y):
        # print("check connected 2 at ", x,y)
        return \
            self.check4(x, y, *self.D1) or \
            self.check4(x, y, *self.D2) or \
            self.check4(x, y, *self.H) or \
            self.check4(x, y, *self.V)

    def check4(self, x, y, x_diff, y_diff):
        positions = self.find_num_connected(x, y, x_diff, y_diff)

        count = len(positions)
        result = count >= 4

        if result:
            self.victory_positions = positions
        # # print("count", count)
        return result

    def find_num_connected(self, x, y, x_diff, y_diff):
        # print("find num connect ", x, y, self.grid.get(x, y))
        # return [] instead of None
        check_against = self.grid.get(x, y)
        if not (check_against == Tile.empty or check_against == Tile.out_of_bounds):

            direction = 1

            i, j = x, y

            count = 0
            # # print(self.grid.get(i, j))
            # # print(check_against)

            positions = []

            while self.grid.get(i, j) == check_against:
                # print("fnc c1")
                positions.append((i, j))
                i, j = i + direction * x_diff, j + direction * y_diff
                count = count + 1

            direction = - direction
            i, j = x, y
            i, j = i + direction * x_diff, j + direction * y_diff

            while self.grid.get(i, j) == check_against:
                # print("fnc c2")
                positions.append((i, j))
                i, j = i + direction * x_diff, j + direction * y_diff
                count = count + 1

            # print("num connected from ", x, y, " at diff", x_diff, y_diff, ": ", len(positions))
            return positions

    # def find_total_num_connected_and_free(self, x, y):
    # print("finding num connected and free at", x, y, self.grid.get(x, y))
    # return max(
    #     (len(self.find_num_connected(x, y, *self.D2)) if self.check4_and_empty(x, y, *self.D2) else 0) * 20,
    #     (len(self.find_num_connected(x, y, *self.D1)) if self.check4_and_empty(x, y, *self.D1) else 0) * 10,
    #     (len(self.find_num_connected(x, y, *self.V)) if self.check4_and_empty(x, y, *self.V) else 0) * 60,
    #     (len(self.find_num_connected(x, y, *self.H)) if self.check4_and_empty(x, y, *self.H) else 0) * 70,
    # )
    # return \
    # (len(self.find_num_connected(x, y, *self.D2)) if self.check4_and_empty(x, y, *self.D2) else 0) * 20 + \
    # (len(self.find_num_connected(x, y, *self.D1)) if self.check4_and_empty(x, y, *self.D1) else 0) * 10 + \
    # return \
    #     (len(self.find_num_connected(x, y, *self.V)) if self.check4_and_empty(x, y, *self.V) else 0) + \
    #     (len(self.find_num_connected(x, y, *self.H)) if self.check4_and_empty(x, y, *self.H) else 0)

    def num_connected_H(self, x, y):
        return len(self.find_num_connected(x, y, *self.H)) if self.check4_and_empty(x, y, *self.H) else 0

    def num_connected_V(self, x, y):
        return len(self.find_num_connected(x, y, *self.H)) if self.check4_and_empty(x, y, *self.V) else 0

    def num_connected_D1(self, x, y):
        return len(self.find_num_connected(x, y, *self.D1)) if self.check4_and_empty(x, y, *self.V) else 0

    def num_connected_D2(self, x, y):
        return len(self.find_num_connected(x, y, *self.D2)) if self.check4_and_empty(x, y, *self.V) else 0

    def check4_and_empty(self, x, y, x_diff, y_diff):
        # print("check4empty called")
        check_against = self.grid.get(x, y)
        if not (check_against == Tile.empty or check_against == Tile.out_of_bounds):
            direction = 1

            i, j = x, y

            count = 0
            # # print(self.grid.get(i, j))
            # # print(check_against)

            positions = []

            while self.grid.get(i, j) == check_against or self.grid.get(i, j) == Tile.empty:
                # print("c4e c1", i,j, self.grid.get(i,j))
                positions.append((i, j))
                i, j = i + direction * x_diff, j + direction * y_diff
                count = count + 1

            direction = - direction
            i, j = x, y
            i, j = i + direction * x_diff, j + direction * y_diff

            while self.grid.get(i, j) == check_against or self.grid.get(i, j) == Tile.empty:
                # print("c4e c2", i,j)
                positions.append((i, j))
                i, j = i + direction * x_diff, j + direction * y_diff
                count = count + 1

            # print("count in check4 and empty ", count)
            return count >= 4
        else:
            # print("invalid tile for check4, tile", check_against)
            return None

    def get_grid(self):
        return self.grid


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
        # # print(self.selected)
        result = False
        if self.selected != -1:
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

    @staticmethod
    def check_player(player_a):
        return Tile.player1 == player_a or Tile.player2 == player_a


class MoveTracker:
    curr_player = Tile.player1

    def __copy__(self):
        return MoveTracker(player2first=self.curr_player == Tile.player2)

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
    # array = [
    #     [Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty],
    #     [Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty],
    #     [Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty],
    #     [Tile.empty, Tile.player2, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty],
    #     [Tile.empty, Tile.player2, Tile.empty, Tile.empty, Tile.empty, Tile.player1, Tile.empty],
    #     [Tile.empty, Tile.player2, Tile.empty, Tile.empty, Tile.empty, Tile.player1, Tile.empty],
    # ]

    array = [
        [Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty],
        [Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty],
        [Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty],
        [Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty],
        [Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty],
        [Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty],
    ]

    def to_string(self):
        result = ""
        for y in range(self.get_height()):
            for x in range(self.get_width()):
                result = result + str(self.get(x, y)) + " , "
            result = result + "\n"
        return result

    def __copy__(self):
        # self.array = []
        result = Grid()
        resarray = []
        for arr in self.array:
            anarr = []
            for val in arr:
                anarr.append(val)
            resarray.append(anarr)
        result.array = resarray
        return result

    def empty_pos(self, col):
        # # print("check in col: ", col)
        for i in range(self.get_height())[::-1]:
            # # print("checking empty", col, i, self.get(col, i))
            # # print(self.array)
            if self.get(col, i) == Tile.empty:
                return col, i
        # # print("should return none")

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
        # # print("Query index: ", x, y)
        if x < self.get_width() and x >= 0 and y < self.get_height() and y >= 0:
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


class Player:
    game: ConnectGame

    def __init__(self, game):
        self.game = game

    def determine_move(self) -> int:
        return 0


class TreeNode:
    game: ConnectGame
    hval = 0.0

    def __init__(self, *argv):
        self.children: [TreeNode] = [arg for arg in argv]


class AIPlayer(Player):
    playerType = Tile.player2
    tree = None
    maxLevels = 6

    # curr_depth = 0

    def heuristic(self, game: ConnectGame):
        if game.game_over:
            if Tile.check_player(game.victory_player):
                if game.victory_player != game.turn_count.curr_player:
                    return 0
                else:
                    return 10000
        grid: Grid = game.get_grid()

        # h
        # v
        # d1
        # d2

        connected_matrix = np.array([
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])

        # normalize this matrix later
        connected_count_matrix = np.array([
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])

        num_connected_weights = np.array([1, 2, 3, 4])

        type_connected_weights = np.array([1, 2, 3, 4])

        for col in range(grid.get_width()):
            # print("getting val for col ", col)
            top_pos = grid.empty_pos(col)
            # print("top pos is ", top_pos)

            if top_pos is not None:
                top_pos_fill = top_pos[0], top_pos[1] + 1
                # attack
                if (grid.get(*top_pos_fill) != game.turn_count.curr_player) or \
                        (grid.get(*top_pos_fill) != Tile.empty) or \
                        (grid.get(*top_pos_fill) != Tile.out_of_bounds):
            # print("num_connect_calc start")
            # maxha = max(maxha, game.find_total_num_connected_and_free(*top_pos_fill))

            # print("num_connect_calc end")

            # defence
            # if (grid.get(*top_pos_fill) == game.turn_count.curr_player) or \
            #         (grid.get(*top_pos_fill) != Tile.empty) or \
            #         (grid.get(*top_pos_fill) != Tile.out_of_bounds):
            #     # print("num_connect_calc start")
            #     maxhb = max(maxhb, game.find_total_num_connected_and_free(*top_pos_fill))
            #     # print("num_connect_calc end")

        return 100 * maxha - maxhb

    def ai_max(self, game, depth=0):
        # pick worst option for min. i.e. least heur.
        # print("Max started at depth: ", depth)
        if depth >= self.maxLevels:
            heur = self.heuristic(game)
            # print("max base", heur)
            return heur, -1
        else:
            # pick max of 7 mins
            maximum = None
            index = -1
            dbres = ""
            for i in range(self.game.get_grid().get_width()):
                # print("checking index i in max ", i, "current max", maximum)
                newgame: ConnectGame = copy.copy(game)
                # print("Exec a move max in " , i)
                move_status = newgame.execute_move(i)
                # move status returns a boolean false only on fail.
                # probably not a good design but it is what it is now...

                # if not not move_status:
                next_move = self.ai_mini(newgame, depth + 1)
                # print(next_move, end='')
                dbres = dbres + str(next_move)
                # print("mini found: ", next_move)
                if maximum is None:
                    maximum = next_move[0]
                    index = i
                elif next_move[0] > maximum:
                    maximum = next_move[0]
                    index = i

            # print("Max at depth: ", depth, " Trying to pick between: -", dbres)
            # print("Max picked value", maximum, "at", index)
            return maximum, index

    def ai_mini(self, game, depth):
        # pick best option for yourself. i.e. pick max heur
        # print("Mini started at depth: ", depth)
        minimum = None
        index = -1
        dbres = ""
        for i in range(self.game.get_grid().get_width()):
            newgame: ConnectGame = copy.copy(game)
            # print("Exec a move mini in ", i)
            newgame.execute_move(i)
            next_move = self.ai_max(newgame, depth + 1)
            dbres = dbres + str(next_move)
            # print(next_move, end='')
            if minimum is None:
                minimum = next_move[0]
                index = i
            elif next_move[0] < minimum:
                minimum = next_move[0]
                index = i

            # minimum = min(minimum, next_move[0]) if minimum is not None else next_move[0]
        # print("mini at depth: ", depth, " Trying to pick between: -", dbres)
        # print("mini picked value", minimum, "at", index)
        return minimum, index

    # def expandTree(self):

    def determine_move(self) -> int:
        # if self.game.turn_count.curr_player == self.playerType:
        choice = self.ai_max(self.game)[1]
        # tree = self.expandTree()
        # it's AI's turn
        # # print("recursion exit", choice)
        return choice
    # else:
    #     return 0

    # return random.randint(0, self.game.get_grid().get_width() - 1)
