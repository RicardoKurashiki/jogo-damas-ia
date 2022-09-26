"""
Essa classe vai ser responsável por administrar toda a informação do tabuleiro.
Ou seja, criação das peças, movimentação etc.

!!! -> Não vai ser feita validações para ver se o movimento é válido, mas sim só realizar este
       e atualizar a visualização, assim como os pontos

Exemplo de tabuleiro:
[2, 1][0, 0][2, 1][0, 0][2, 1][0, 0][2, 1][0, 0][2, 1][0, 0]
[0, 0][2, 1][0, 0][2, 1][0, 0][2, 1][0, 0][2, 1][0, 0][2, 1]
[2, 1][0, 0][2, 1][0, 0][2, 1][0, 0][2, 1][0, 0][2, 1][0, 0]
[0, 0][2, 1][0, 0][2, 1][0, 0][2, 1][0, 0][2, 1][0, 0][2, 1]
[0, 0][0, 0][0, 0][0, 0][0, 0][0, 0][0, 0][0, 0][0, 0][0, 0]
[0, 0][0, 0][0, 0][0, 0][0, 0][0, 0][0, 0][0, 0][0, 0][0, 0]
[1, 1][0, 0][1, 1][0, 0][1, 1][0, 0][1, 1][0, 0][1, 1][0, 0]
[0, 0][1, 1][0, 0][1, 1][0, 0][1, 1][0, 0][1, 1][0, 0][1, 1]
[1, 1][0, 0][1, 1][0, 0][1, 1][0, 0][1, 1][0, 0][1, 1][0, 0]
[0, 0][1, 1][0, 0][1, 1][0, 0][1, 1][0, 0][1, 1][0, 0][1, 1]
"""

from definitions import *
from piece import Piece
import copy

class Table:
    def __init__(self, table=[], blacks=0, whites=0):
        self.table = copy.deepcopy(table)
        self.blacks = copy.deepcopy(blacks)
        self.whites = copy.deepcopy(whites)

    def copy(self, table):
        self.table = copy.deepcopy(table.table)
        self.blacks = copy.deepcopy(table.blacks)
        self.whites = copy.deepcopy(table.whites)

    def generateTable(self):
        def generatePieces(type, rows):
            cont = 0
            for i in range(rows):
                spaces = []
                for j in range(10):
                    if (cont % 2 != 0):
                        spaces.append([0,0])
                    else:
                        spaces.append(type)
                    cont += 1
                self.table.append(spaces)
                cont -= 1
        
        # generatePieces([2,1], 4)
        generatePieces([0,0], 10)
        # generatePieces([1,1], 4)

    def showTable(self):
        for i in range(10):
            print(f"{i} |", end=" ")
            for j in range(10):
                print(Piece(self.table[i][j]).getString(), end=" ")
            print()
        for i in range(12):
            print("--", end="")
        print()
        print("  |", end="")
        for i in range(10):
            print(f" {i}", end="")
        print()

    def start(self):
        self.blacks = 20
        self.whites = 20
        self.generateTable()
        self.showTable()
        
    # =============================== #

    def move(self, context, show=False):
        def clearPlaces():
            for i in range(int(context.getDistance())):
                if (context.getDirection() == "SE"):
                    self.table[currentPos[0]+i][currentPos[1]+i] = [0,0]
                elif (context.getDirection() == "SW"):
                    self.table[currentPos[0]+i][currentPos[1]-i] = [0,0]
                elif (context.getDirection() == "NE"):
                    self.table[currentPos[0]-+i][currentPos[1]+i] = [0,0]
                elif (context.getDirection() == "NW"):
                    self.table[currentPos[0]-i][currentPos[1]-i] = [0,0]

        currentPos = context.currentPos
        nextPos = context.nextPos
        clearPlaces()
        self.table[nextPos[0]][nextPos[1]] = context.piece.getValue()
        piece = context.piece
        lastHouse = -1
        if (piece.team == Team.BLACK):
            lastHouse = 0
        else:
            lastHouse = 9
        if (not context.capturing):
            if (nextPos[0] == lastHouse):
                self.promote(context)
        if (show):
            self.showTable()


    def updatePoints(self):
        b = 0
        w = 0
        for i in range(10):
            for j in range(10):
                if (self.table[i][j][0] == Team.BLACK.value):
                    b += 1
                elif (self.table[i][j][0] == Team.WHITE.value):
                    w += 1
        self.blacks = b
        self.whites = w

    def showPoints(self):
        print(f"Peças pretas: {self.blacks} x Peças brancas: {self.whites}")

    def gameEnded(self):
        v1 = self.blacks == 0
        v2 = self.whites == 0
        return (v1 or v2)

    def promote(self, context):
        nextPos = context.nextPos
        pieceValue = context.piece.getValue()
        pieceValue[1] = Type.DAMA.value
        self.table[nextPos[0]][nextPos[1]] = pieceValue