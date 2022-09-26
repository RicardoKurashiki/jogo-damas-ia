from table import *
from context import *
from piece import *
from definitions import *
from alfa_beta import *
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

controller = AlphaBeta(Team.WHITE)

context = controller.think(t1)

if (type(context) is list):
    for move in context:
        t1.move(move, True)
else:
    t1.move(context, True)

context = controller.think(t1)
t1.move(context, True)