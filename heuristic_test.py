from game import *


def heur(arr, player):
    game = ConnectGame(player_first=player)
    game.grid.array = arr
    return AIPlayer(game, playerType=player).heuristic(game)


print("Heuristic: ", heur([
    [Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty],
    [Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty],
    [Tile.player1, Tile.player2, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty],
    [Tile.player1, Tile.player2, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty],
    [Tile.player1, Tile.player2, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty],
    [Tile.player1, Tile.player2, Tile.empty, Tile.empty, Tile.empty, Tile.empty, Tile.empty],
], player=Tile.player2))
