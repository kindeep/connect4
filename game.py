from enum import Enum
import copy
import numpy as np


# Enum to describe a player
class Tile(Enum):
    player1 = 0
    player2 = 1
    empty = 2
    out_of_bounds = 3

    # check if the provided input is a player tile
    @staticmethod
    def check_player(player_a):
        return Tile.player1 == player_a or Tile.player2 == player_a

    # get the opponent for the input player
    @staticmethod
    def other_player(player):
        if Tile.check_player(player):
            if player == Tile.player1:
                return Tile.player2
            else:
                return Tile.player1


# Main logic for the game
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

    # execute move at col=pos
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

    # check if the provided tile is part of a 4 connect
    def check_connected2(self, x, y):
        return \
            self.check4(x, y, *self.D1) or \
            self.check4(x, y, *self.D2) or \
            self.check4(x, y, *self.H) or \
            self.check4(x, y, *self.V)

    # helper method for check_connected, D1 D2 H and V defines what kind of 4 connect is being checked, Horizontal, vertical ..
    def check4(self, x, y, x_diff, y_diff):
        positions = self.find_num_connected_list(x, y, x_diff, y_diff)

        count = len(positions)
        result = count >= 4

        if result:
            self.victory_positions = positions
        return result

    # Returns a list of connected positions
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

    # returns how many pieces are connected in type of connect defined by diff
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

    # returns how many horizontal pieces are connected at given x y. other methods similar.
    def num_connected_h(self, x, y):
        return min(self.find_num_connected(x, y, *self.H) if self.check4_and_empty(x, y, *self.H) else 0, 4)

    def num_connected_v(self, x, y):
        return min(self.find_num_connected(x, y, *self.H) if self.check4_and_empty(x, y, *self.V) else 0, 4)

    def num_connected_d1(self, x, y):
        return min(self.find_num_connected(x, y, *self.D1) if self.check4_and_empty(x, y, *self.V) else 0, 4)

    def num_connected_d2(self, x, y):
        return min(self.find_num_connected(x, y, *self.D2) if self.check4_and_empty(x, y, *self.V) else 0, 4)

    # Checks if there is space to make a 4 connect with given x y and type of connect defined by diff.
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


# Admittedly unnecessary class to track current move. Literally just tracks current move.
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


# defins the structure that stores the connect4 board.
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

    # returns the first empty available position in a col
    def empty_pos(self, col):
        for i in range(self.get_height())[::-1]:
            if self.get(col, i) == Tile.empty:
                return col, i

    def get_width(self) -> int:
        return 7

    def get_height(self) -> int:
        return 6

    # checks if player 1 tile is at x y. following methods similar.
    def check_player1(self, x, y) -> bool:
        return self.array[y][x] == Tile.player1

    def check_player2(self, x, y) -> bool:
        return self.array[y][x] == Tile.player2

    def check_empty(self, x, y) -> bool:
        return self.array[y][x] == Tile.empty

    def set(self, x, y, val):
        self.array[y][x] = val

    # gets the tile at x, y
    def get(self, x, y):
        if x < self.get_width() and x >= 0 and y < self.get_height() and y >= 0:
            return self.array[y][x]
        else:
            return Tile.out_of_bounds

    def __str__(self):
        return str(self.array)
    # def __init__(self):


# Defines a player to make next move decisions.
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
        # returns (self heuristic vs heuristic for opponent) with self given preference. attack - defence, attack has preference.
        return 2 * self.wut_heuristic(game, self.playerType) - self.wut_heuristic(game,
                                                                                  Tile.other_player(self.playerType))

    # The actual heuristic calculation stuff. The heuristic takes into account size and number of connect series.
    def wut_heuristic(self, game: ConnectGame, player):
        if game.game_over:
            if Tile.check_player(game.victory_player):
                if game.victory_player != player:
                    return -10000000000000000000000
                else:
                    return 10000000000000000000000

        grid: Grid = game.get_grid()

        # upcoming matrix stores how many of size 1 2 3 and 4 connections are there of the types horizontal, vertical ...
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

        # actually fill up the matrix.
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

        # determine a max value, to later give preference to 4 connects without losing other connect data
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

    # max in minimax
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

    # mini in minimax
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
