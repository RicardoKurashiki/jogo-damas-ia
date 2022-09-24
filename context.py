import math

class Context:
    def __init__(self, current, next, piece):
        self.current = current
        self.next = next
        self.piece = piece
    
    def getDistance(self):
        x = self.next[1] - self.current[1]
        y = self.next[0] - self.next[0]
        return math.sqrt((x**2)+(y**2))

    def getDirection(self):
        if (self.next[0] > self.current[0]):
            if (self.next[1] > self.current[1]):
                return "SE"
            else:
                return "SW"
        else:
            if (self.next[1] > self.current[1]):
                return "NE"
            else:
                return "NW"