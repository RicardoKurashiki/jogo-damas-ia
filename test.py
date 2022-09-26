from table import *
from context import *
from piece import *
from definitions import *
from alfa_beta import *
import time

t1 = Table()
t1.start()

t1.move(Context([5,2],[5,2],Piece([1,1])), False)
t1.move(Context([3,8],[3,8],Piece([1,1])), False)
t1.move(Context([5,8],[5,8],Piece([1,1])), False)

t1.move(Context([6,1],[6,1],Piece([2,1])), False)
t1.move(Context([6,7],[6,7],Piece([2,1])), True)

controller = AlphaBeta(Team.WHITE)

context = controller.think(t1)
t1.move(context, True)
context = controller.think(t1)
t1.move(context, True)