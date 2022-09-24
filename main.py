from table import Table
from context import Context
from piece import Piece
from player import Player
from definitions import Definitions

definitions = Definitions()

def choosePiece():
    print(" ------------------------- ")
    print(f"|(1) Pretas               |")
    print(f"|(2) Brancas              |")
    print(" ------------------------- ")
    return int(input("Escolha sua peça: "))

playerPiece = choosePiece()
p = Player(playerPiece)

t = Table()
t.start()

game = True

while game:
    context = p.play(t.table)
    t.move(context)
