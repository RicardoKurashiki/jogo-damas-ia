from table import *
from context import *
from piece import *
from definitions import *
from alfa_beta import *

t1 = Table()
t2 = Table()

print("TABLE 1")
t1.start()
print("TABLE 2")
t2.start()

print("MOVENDO NA TABLE 1")
t1.move(Context([6,0], [0,6], Piece([1,1])))

print("MOSTRANDO TABLE 2")
t2.showTable()

print("COPY TABLE 1 TO TABLE 2")
t2.copy(t1)

print("MOVENDO NA TABLE 1")
t1.move(Context([0,6], [3,9], Piece([1,1])))

print("MOSTRANDO TABLE 2")
t2.showTable()