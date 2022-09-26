from table import *
from context import *
from piece import *
from definitions import *
from alfa_beta import *
from player import *
import time

t1 = Table()
t1.start()

blacksSpots = [
    [9,1], [9,3], [9,5], [9,7], [9,9],
    [8,2], [8,4], [2,2]
]

whiteSpots = [
    [2,0], [0,8], [1,5], [1,7], [1,9],
    [2,6], [2,8], [3,3], [3,5], [4,8],
    [5,5], [1,3]
]

for coord in blacksSpots:
    t1.move(Context(coord, coord, Piece([1,1]), False), False)

for coord in whiteSpots:
    t1.move(Context(coord, coord, Piece([2,1]), False), False)

t1.showTable()

player = Player(Team.BLACK.value)

controller = AlphaBeta(Team.WHITE)
turn = Team.BLACK
enemy = Team.WHITE
game = True

while game:
    t1.showPoints()
    if (turn == player.team):
        context = player.play(t1)
        t1.move(context, True)
        if (not context.capturing):
            turn = enemy
    else:
        context = controller.think(t1)
        if (type(context) is list):
            for move in context:
                t1.move(move, True)
        else:
            t1.move(context, True)
        turn = player.team
    t1.updatePoints()
    if (t1.gameEnded()):
        game = False





# context = controller.think(t1)

# if (type(context) is list):
#     for move in context:
#         t1.move(move, True)
# else:
#     t1.move(context, True)

# context = controller.think(t1)
# t1.move(context, True)