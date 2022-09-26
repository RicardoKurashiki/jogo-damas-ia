from table import *
from context import *
from piece import *
from definitions import *
from alfa_beta import *
from player import *
import time

t1 = Table()
t1.start()


t1.move(Context([7,0],[7,0],Piece([2,1]),False), False)

t1.move(Context([8,1],[8,1],Piece([1,1]),False), False)
t1.move(Context([8,3],[8,3],Piece([1,1]),False), False)
t1.move(Context([6,5],[6,5],Piece([1,1]),False), False)
t1.move(Context([8,5],[8,5],Piece([1,1]),False), False)
t1.move(Context([8,7],[8,7],Piece([1,1]),False), False)
t1.move(Context([8,7],[8,7],Piece([1,1]),False), False)
t1.move(Context([6,7],[6,7],Piece([1,1]),False), True)

player = Player(Team.WHITE.value)

controller = AlphaBeta(Team.BLACK)
turn = player.team
game = True

while game:
    t1.showPoints()
    if (turn == player.team):
        context = player.play(t1)
        t1.move(context, True)
        if (not context.capturing):
            turn = Team.BLACK
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