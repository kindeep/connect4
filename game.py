from enum import Enum
import random
import copy
import numpy


class ConnectGame:
    victory = None
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
                    self.victory = self.grid.get(*result)

            if (result):
                return result

    def check_connected2(self, x, y):
        # print("check connected 2 at ", x,y)
        return \
            self.check4(x, y, *self.D1) or \
            self.check4(x, y, *self.D2) or \
            self.check4(x, y, *self.H) or \
            self.check4(x, y, *self.V)

    def check4(self, x, y, x_diff, y_diff):
        # print("check4 at ", x, y)
        # check_against = self.grid.get(x, y)
        # direction = 1
        #
        # i, j = x, y
        #
        # count = 0
        # # print(self.grid.get(i, j))
        # # print(check_against)
        #
        # positions = []
        #
        # while self.grid.get(i, j) == check_against:
        #     positions.append((i, j))
        #     i, j = i + direction * x_diff, j + direction * y_diff
        #     count = count + 1
        #
        # direction = - direction
        # i, j = x, y
        #
        #
        # while self.grid.get(i, j) == check_against:
        #     positions.append((i, j))
        #     i, j = i + direction * x_diff, j + direction * y_diff
        #     count = count + 1

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

            # print("num connected ", len(positions))
            return positions

    def find_total_num_connected_and_free(self, x, y):
        # print("num connected and free at", x, y, self.grid.get(x, y))
        return max(
            len(self.find_num_connected(x, y, *self.D2)) if self.check4_and_empty(x, y, *self.D2) else 0,
            len(self.find_num_connected(x, y, *self.D1)) if self.check4_and_empty(x, y, *self.D1) else 0,
            len(self.find_num_connected(x, y, *self.V)) if self.check4_and_empty(x, y, *self.V) else 0,
            len(self.find_num_connected(x, y, *self.H)) if self.check4_and_empty(x, y, *self.H) else 0,
        )

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
        # else:
            # print("invalid tile for check4")

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
                # # print("Wut", index, positions[index])
                if b:
                    self.victory_positions = positions[index]

            return result

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
    maxLevels = 1
    curr_depth = 0

    def heuristic(self, game: ConnectGame):
        # print("Calculating heur")
        grid: Grid = game.get_grid()

        maxh = 0
        for col in range(grid.get_width()):
            # print("getting val for col ", col)
            top_pos = grid.empty_pos(col)
            # print("top pos is ", top_pos)
            if top_pos is not None:
                # print("num_connect_calc start")
                maxh = max(maxh, game.find_total_num_connected_and_free(top_pos[0], top_pos[1] + 1))
                # print("num_connect_calc end")

        print("Heur val: ", maxh)
        return maxh

    def stupid_heuristic(self, game: ConnectGame):
        check_against = game.turn_count.curr_player
        grid = game.get_grid()
        results = [False, False, False, False]

        for col in range(game.get_grid().get_width()):
            pos = grid.empty_pos(col)
            if pos is not None:

                x, y = pos
                if y >= grid.get_height() - 1 or check_against == grid.get(x, y + 1):
                    # check_against = grid.get(x, y)
                    if check_against != Tile.empty:
                        # results = [True, True, True, True]
                        for j in range(4):
                            bools = [True, True, True, True, True, True, True, True]
                            bools2 = [True, True, True, True, True, True, True, True]
                            # bools = [True] * 8
                            # positions = [[], [], [], [], [], [], [], []]
                            # Check how many circles the move leadds to
                            for index in range(j):
                                i = index + 1
                                tp = x + i, y
                                bools[0] = bools[0] and grid.get(*tp) == check_against
                                # positions[0].append(tp)

                                tp = x - i, y
                                bools[1] = bools[1] and grid.get(*tp) == check_against
                                # positions[1].append(tp)

                                tp = x, y + i
                                bools[2] = bools[2] and grid.get(*tp) == check_against
                                # positions[2].append(tp)

                                tp = x, y - i
                                bools[3] = bools[3] and grid.get(*tp) == check_against
                                # positions[3].append(tp)

                                tp = x + i, y + i
                                bools[4] = bools[4] and grid.get(*tp) == check_against
                                # positions[4].append(tp)

                                tp = x - i, y - i
                                bools[5] = bools[5] and grid.get(*tp) == check_against
                                # positions[5].append(tp)

                                tp = x - i, y + i
                                bools[6] = bools[6] and grid.get(*tp) == check_against
                                # positions[6].append(tp)

                                tp = x + i, y - i
                                bools[7] = bools[7] and grid.get(*tp) == check_against
                                # positions[7].append(tp)

                            # check if circles have space for a win
                            for index in range(4):
                                i = index + 1
                                tp = x + i, y
                                bools2[0] = bools2[0] and grid.get(*tp) == check_against or grid.get(*tp) == Tile.empty
                                # positions[0].append(tp)

                                tp = x - i, y
                                bools2[1] = bools2[1] and grid.get(*tp) == check_against or grid.get(*tp) == Tile.empty
                                # positions[1].append(tp)

                                tp = x, y + i
                                bools2[2] = bools2[2] and grid.get(*tp) == check_against or grid.get(*tp) == Tile.empty
                                # positions[2].append(tp)

                                tp = x, y - i
                                bools2[3] = bools2[3] and grid.get(*tp) == check_against or grid.get(*tp) == Tile.empty
                                # positions[3].append(tp)

                                tp = x + i, y + i
                                bools2[4] = bools2[4] and grid.get(*tp) == check_against or grid.get(*tp) == Tile.empty
                                # positions[4].append(tp)

                                tp = x - i, y - i
                                bools2[5] = bools2[5] and grid.get(*tp) == check_against or grid.get(*tp) == Tile.empty
                                # positions[5].append(tp)

                                tp = x - i, y + i
                                bools2[6] = bools2[6] and grid.get(*tp) == check_against or grid.get(*tp) == Tile.empty
                                # positions[6].append(tp)

                                tp = x + i, y - i
                                bools2[7] = bools2[7] and grid.get(*tp) == check_against or grid.get(*tp) == Tile.empty
                                # positions[7].append(tp)

                            for index, bl in enumerate(bools):
                                bools[index] = bl and bools2[index]

                            result = False
                            for index, b in enumerate(bools):
                                result = result or b

                            if result:
                                results[j] = True

        # # print(results)

        hval = 0

        for index, bl in enumerate(results):
            if bl:
                hval = index + 1

        # # print((grid.to_string()))
        # # print(hval, "resutl")
        return hval

    def ai_max(self, game, depth=0):
        print(depth, "call max")
        if depth >= self.maxLevels:
            heur = self.heuristic(game)
            # print("max base", heur)
            return heur, -1
        else:
            # pick max of 7 mins
            maximum = None
            index = -1

            for i in range(self.game.get_grid().get_width()):
                print("checking index i in max ", i, "current max", maximum)
                newgame: ConnectGame = copy.copy(game)
                # print("Exec a move max in " , i)
                move_status = newgame.execute_move(i)
                # move status returns a boolean false only on fail.
                # probably not a good design but it is what it is now...
                if not not move_status:
                    next_move = self.ai_mini(newgame, depth + 1)
                    print("mini found: ", next_move)
                    if maximum is None:
                        maximum = next_move[0]
                        index = i
                    elif next_move[0] > maximum:
                        maximum = next_move[0]
                        index = i
            print("max ret", maximum, index)
            return maximum, index

    def ai_mini(self, game, depth):
        print(depth, "call min")
        minimum = None
        index = -1
        for i in range(self.game.get_grid().get_width()):
            newgame: ConnectGame = copy.copy(game)
            # print("Exec a move mini in ", i)
            newgame.execute_move(i)
            next_move = self.ai_max(newgame, depth + 1)

            if minimum is None:
                minimum = next_move[0]
                index = i
            elif next_move[0] < minimum:
                minimum = next_move[0]
                index = i

            # minimum = min(minimum, next_move[0]) if minimum is not None else next_move[0]
        print("min ret", minimum, index)
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
