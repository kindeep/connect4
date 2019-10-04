from enum import Enum
import copy
import numpy as np


class Tile(Enum):
    player1 = 0
    player2 = 1
    empty = 2
    out_of_bounds = 3

    @staticmethod
    def check_player(player_a):
        return Tile.player1 == player_a or Tile.player2 == player_a

    @staticmethod
    def other_player(player):
        if Tile.check_player(player):
            if player == Tile.player1:
                return Tile.player2
            else:
                return Tile.player1


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

    def __init__(self, player_first=Tile.player1):
        self.grid = Grid()
        self.turn_count = MoveTracker(player_first)

    def execute_move(self, pos, player=None):
        if not player:
            player = self.turn_count.curr_player
        if not self.game_over:
            if self.turn_count.curr_player == player:
                result = False
                for i in range(self.grid.get_height())[::-1]:
                    if self.grid.check_empty(pos, i):
                        self.grid.set(pos, i, self.turn_count.get_curr_turn())
                        self.turn_count.next_turn()
                        result = pos, i
                        break

                if result:
                    if self.check_connected2(*result):
                        self.game_over = True
                        self.victory_player = self.grid.get(*result)

                if (result):
                    return result
        else:
            self.turn_count.next_turn()

    def check_connected2(self, x, y):
        return \
            self.check4(x, y, *self.D1) or \
            self.check4(x, y, *self.D2) or \
            self.check4(x, y, *self.H) or \
            self.check4(x, y, *self.V)

    def check4(self, x, y, x_diff, y_diff):
        positions = self.find_num_connected_list(x, y, x_diff, y_diff)

        count = len(positions)
        result = count >= 4

        if result:
            self.victory_positions = positions
        return result

    def find_num_connected_list(self, x, y, x_diff, y_diff):
        check_against = self.grid.get(x, y)
        if not (check_against == Tile.empty or check_against == Tile.out_of_bounds):

            direction = 1

            i, j = x, y

            count = 0

            positions = []

            while self.grid.get(i, j) == check_against:
                positions.append((i, j))
                i, j = i + direction * x_diff, j + direction * y_diff
                count = count + 1

            direction = - direction
            i, j = x, y
            i, j = i + direction * x_diff, j + direction * y_diff

            while self.grid.get(i, j) == check_against:
                positions.append((i, j))
                i, j = i + direction * x_diff, j + direction * y_diff
                count = count + 1

            return positions

    def find_num_connected(self, x, y, x_diff, y_diff):
        check_against = self.grid.get(x, y)
        if not (check_against == Tile.empty or check_against == Tile.out_of_bounds):

            direction = 1

            i, j = x, y

            count = 0

            while self.grid.get(i, j) == check_against:
                i, j = i + direction * x_diff, j + direction * y_diff
                count = count + 1

            direction = - direction
            i, j = x, y
            i, j = i + direction * x_diff, j + direction * y_diff

            while self.grid.get(i, j) == check_against:
                i, j = i + direction * x_diff, j + direction * y_diff
                count = count + 1

            return count

    def num_connected_h(self, x, y):
        return min(self.find_num_connected(x, y, *self.H) if self.check4_and_empty(x, y, *self.H) else 0, 4)

    def num_connected_v(self, x, y):
        return min(self.find_num_connected(x, y, *self.H) if self.check4_and_empty(x, y, *self.V) else 0, 4)

    def num_connected_d1(self, x, y):
        return min(self.find_num_connected(x, y, *self.D1) if self.check4_and_empty(x, y, *self.V) else 0, 4)

    def num_connected_d2(self, x, y):
        return min(self.find_num_connected(x, y, *self.D2) if self.check4_and_empty(x, y, *self.V) else 0, 4)

    def check4_and_empty(self, x, y, x_diff, y_diff):
        check_against = self.grid.get(x, y)
        if not (check_against == Tile.empty or check_against == Tile.out_of_bounds):
            direction = 1

            i, j = x, y

            count = 0

            positions = []

            while self.grid.get(i, j) == check_against or self.grid.get(i, j) == Tile.empty:
                positions.append((i, j))
                i, j = i + direction * x_diff, j + direction * y_diff
                count = count + 1

            direction = - direction
            i, j = x, y
            i, j = i + direction * x_diff, j + direction * y_diff

            while self.grid.get(i, j) == check_against or self.grid.get(i, j) == Tile.empty:
                positions.append((i, j))
                i, j = i + direction * x_diff, j + direction * y_diff
                count = count + 1

            return count >= 4
        else:
            return None

    def get_grid(self):
        return self.grid


class MoveTracker:
    curr_player = Tile.player1

    def __copy__(self):
        return MoveTracker(player_first=self.curr_player)

    def __init__(self, player_first=Tile.player1):
        if Tile.check_player(player_first):
            self.curr_player = player_first

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
        for i in range(self.get_height())[::-1]:
            if self.get(col, i) == Tile.empty:
                return col, i

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
        if x < self.get_width() and x >= 0 and y < self.get_height() and y >= 0:
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

    @staticmethod
    def get_tile_color(tile: Tile):
        if tile == Tile.player2:
            return Colors.red
        if tile == Tile.player1:
            return Colors.yellow
        else:
            return Colors.white


class TreeNode:
    game: ConnectGame
    hval = 0.0

    def __init__(self, *argv):
        self.children: [TreeNode] = [arg for arg in argv]


class AIPlayer:
    game: ConnectGame
    tree = None
    maxLevels: int

    # 6 - 30-50 s
    # 7 - 250-300 s
    # 8 - >800 s

    def __init__(self, game: ConnectGame, ply=4, playerType=None):
        self.playerType = playerType
        self.game = game
        self.maxLevels = ply

    def heuristic(self, game: ConnectGame):
        return 2 * self.wut_heuristic(game, self.playerType) - self.wut_heuristic(game, Tile.other_player(self.playerType))

    def wut_heuristic(self, game: ConnectGame, player):
        if game.game_over:
            if Tile.check_player(game.victory_player):
                if game.victory_player != player:
                    return -10000000000000000000000
                else:
                    return 10000000000000000000000

        grid: Grid = game.get_grid()

        # h
        # v
        # d1
        # d2

        connected_count_matrix = np.array([
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
        ])

        for col in range(grid.get_width()):
            top_pos = grid.empty_pos(col)
            if top_pos is not None:
                top_pos_fill = top_pos[0], top_pos[1] + 1
                if (grid.get(*top_pos_fill) == player) and \
                        (grid.get(*top_pos_fill) != Tile.empty) and \
                        (grid.get(*top_pos_fill) != Tile.out_of_bounds):
                    hc = game.num_connected_h(*top_pos_fill)
                    if hc != 0:
                        connected_count_matrix[0][hc - 1] = connected_count_matrix[0][hc - 1] + 1

                    vc = game.num_connected_v(*top_pos_fill)
                    if vc != 0:
                        connected_count_matrix[1][vc - 1] = connected_count_matrix[0][vc - 1] + 1

                    d1c = game.num_connected_d1(*top_pos_fill)
                    if d1c != 0:
                        connected_count_matrix[2][d1c - 1] = connected_count_matrix[0][d1c - 1] + 1

                    d2c = game.num_connected_d2(*top_pos_fill)
                    if d2c != 0:
                        connected_count_matrix[3][d2c - 1] = connected_count_matrix[0][d2c - 1] + 1

        cap = 0
        start = 3
        while cap == 0 and start >= 0:
            cap = max(cap, max([connected_count_matrix[i][start] for i in range(4)]))
            start = start - 1
        if cap != 0:
            for ri, r in enumerate(connected_count_matrix):
                for ci, c in enumerate(r):
                    val = min(1.0, c / cap)
                    connected_count_matrix[ri][ci] = val

            num_connected_weights = np.transpose(np.array([1.0, 2.0, 3.0, 4.0]))

            heuristic = connected_count_matrix @ num_connected_weights
            return np.sum(heuristic)
        else:
            return 0

    def ai_max(self, game, depth=0, won_depth=None):
        # pick worst option for min. i.e. least heur.
        if depth >= self.maxLevels:
            mul = 1
            if not not won_depth:
                mul = won_depth
            heur = self.heuristic(game) * mul
            return heur, -1
        else:
            # pick max of 7 mins
            maximum = None
            index = -1
            dbres = ""
            for i in range(self.game.get_grid().get_width()):
                if game.grid.empty_pos(i) is not None:
                    newgame: ConnectGame = copy.copy(game)
                    move_status = newgame.execute_move(i)
                    if not not won_depth and newgame.game_over:
                        won_depth = depth
                    next_move = self.ai_mini(newgame, depth + 1)
                    dbres = dbres + str(next_move)
                    if maximum is None:
                        maximum = next_move[0]
                        index = i
                    elif next_move[0] > maximum:
                        maximum = next_move[0]
                        index = i

            return maximum, index

    def ai_mini(self, game, depth, won_depth=None):
        if depth >= self.maxLevels:
            mul = 1
            if not not won_depth:
                mul = won_depth
            heur = self.heuristic(game) * mul
            return heur, -1
        else:
            minimum = None
            index = -1
            dbres = ""
            for i in range(self.game.get_grid().get_width()):
                newgame: ConnectGame = copy.copy(game)
                newgame.execute_move(i)
                if not not won_depth and newgame.game_over:
                    won_depth = depth
                next_move = self.ai_max(newgame, depth + 1, won_depth)
                dbres = dbres + str(next_move)
                if minimum is None:
                    minimum = next_move[0]
                    index = i
                elif next_move[0] < minimum:
                    minimum = next_move[0]
                    index = i

            return minimum, index

    def determine_move(self) -> int:
        choice = self.ai_max(self.game)[1]
        return choice
