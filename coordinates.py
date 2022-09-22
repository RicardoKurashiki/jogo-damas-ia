class Coordinate:
    def __init__(self, coordLine=0, coordColumn=0):
        self.line = coordLine
        self.column = coordColumn

    def isEquals(self, otherCoord):
        return (self.line == otherCoord.line and self.column == otherCoord.column)
