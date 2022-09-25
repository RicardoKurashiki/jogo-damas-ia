from table import *
from context import *
from piece import *
from definitions import *
from alfa_beta import *
import time

t1 = Table()
t1.start()

t1.move(Context([3,1],[4,2],Piece([2,1])), True)
t1.move(Context([4,2],[5,1],Piece([2,1])), True)

controller = AlphaBeta(Team.BLACK)

controller.think(t1)