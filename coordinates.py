from enum import Enum


class teams(Enum):
    BLACK = 1   # Time preto
    WHITE = 2   # Time branco


class Coordinate:
    def __init__(self, coordLine=0, coordColumn=0, coordStatus=0):
        self.line = coordLine
        self.column = coordColumn
        self.status = coordStatus  # Valor 0 indica que a casa esta desocupada
