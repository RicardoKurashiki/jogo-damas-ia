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
            else:
                return "SW"
        else:
            if (self.nextPos[1] > self.currentPos[1]):
                return "NE"
            else:
                return "NW"