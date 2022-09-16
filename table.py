import coordinates as c


class Table:
    def __init__(self):
        self.places = []
        self.black = 0
        self.whites = 0

    def showTable(self) -> None:
        print('  | 0 1 2 3 4 5 6 7 8 9\n-----------------------')
        for i in range(10):
            print(i, '|', end=' ')
            for j in range(10):
                if (j+i) % 2 == 0:
                    print(' ', end=' ')
                else:
                    print(self.places[i][j], end=' ')
            print()

    def generatePieces(self, char) -> None:
        cont = 0
        for i in range(4):
            valores = []
            for j in range(10):
                cont += 1
                if (cont % 2 == 0):
                    valores.append(char)
                else:
                    valores.append(" ")
            cont -= 1
            self.places.append(valores)

    def generateEmptyPlaces(self) -> None:
        valores = [" " for i in range(10)]
        for i in range(2):
            self.places.append(valores)

    def generatePlaces(self) -> None:
        self.generatePieces('b')
        self.generateEmptyPlaces()
        self.generatePieces('w')

    def getPiecePositions(self, type) -> list:
        coords = []
        for i in range(10):
            for j in range(10):
                if (self.places[i][j] == type):
                    if (type == 'b'):
                        coords.append(c.Coordinate(i, j, 1))
                    elif (type == 'w'):
                        coords.append(c.Coordinate(i, j, 2))
        return coords

    def start(self):
        print("-------------------------\n     JOGO DAS DAMAS\n-------------------------\n")
        self.generatePlaces()
        self.showTable()
