"""
Esta classe vai ser o intermediador entre o tabuleiro e os movimentos.
Ele vai ter todos os dados do movimento escolhido e da peça escolhida.

Tabuleiro -> Context -> Player (A escolha vai ser feita, o tabuleiro vai mandar a situação atual para os validadores)
Player -> Context -> Tabuleiro (Se os validadores derem OK, o contexto é passado para o tabuleiro que vai atualizar )
"""

import math
from piece import Piece

class Context:
    def __init__(self, currentPos, nextPos, piece):
        self.currentPos = currentPos
        self.nextPos = nextPos
        self.piece = piece
    
    def getDistance(self):
        x = self.nextPos[1] - self.currentPos[1]
        y = self.nextPos[0] - self.nextPos[0]
        return math.sqrt((x**2)+(y**2))

    def getDirection(self):
        if (self.nextPos[0] > self.currentPos[0]):
            if (self.nextPos[1] > self.currentPos[1]):
                return "SE"
            elif (self.nextPos[1] == self.currentPos[1]):
                return "ER"
            else:
                return "SW"
        else:
            if (self.nextPos[1] > self.currentPos[1]):
                return "NE"
            elif (self.nextPos[1] == self.currentPos[1]):
                return "ER"
            else:
                return "NW"