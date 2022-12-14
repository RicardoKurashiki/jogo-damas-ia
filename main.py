from table import Table
from context import Context
from piece import Piece
from player import Player
from definitions import *
from alfa_beta import AlphaBeta

definitions = Definitions()

def choosePiece():
    isValid = False
    while not isValid:
        print(" ------------------------")
        print("|         DAMAS          |")
        print(" ------------------------")
        print(f"|(1) Pretas              |")
        print(f"|(2) Brancas             |")
        print("  ------------------------")
        piece = input("Escolha sua peça: ")
        isValid = (piece.isnumeric() and int(piece) in [1,2])
        if (not isValid):
            print("Escolha inválida. Tente novamente.")
    return int(piece)

playerPiece = choosePiece()
player = Player(playerPiece)

table = Table()
table.start()

game = True

turn = player.team
enemy = Team.BLANK

if (player.team == Team.BLACK):
    enemy = Team.WHITE
else:
    enemy = Team.BLACK

controller = AlphaBeta(enemy)

while game:
    table.showPoints()
    if (turn == player.team):
        context = player.play(table)
        table.move(context, True)
        if (not context.capturing):
            turn = enemy
    else:
        context = controller.think(table)
        if (type(context) is list):
            for move in context:
                table.move(move, True)
        else:
            table.move(context, True)
        turn = player.team
    table.updatePoints()
    if (table.gameEnded()):
        game = False

if (table.blacks == 0):
    print("PEÇAS BRANCAS GANHARAM!")
elif (table.whites == 0):
    print("PEÇAS PRETAS GANHARAM!")