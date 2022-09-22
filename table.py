import coordinates as c


class Table:
    def __init__(self):
        self.places = []
        self.black = 20
        self.whites = 20

    def showTable(self):
        print('  | 0 1 2 3 4 5 6 7 8 9\n-----------------------')
        for i in range(10):
            print(i, '|', end=' ')
            for j in range(10):
                if (j+i) % 2 == 0:
                    print(' ', end=' ')
                else:
                    print(self.places[i][j], end=' ')
            print()

    def generatePieces(self, char):
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

    def generateEmptyPlaces(self):
        valores = [" " for i in range(10)]
        for i in range(2):
            self.places.append(valores)

    def generatePlaces(self):
        self.generatePieces('b')
        self.generateEmptyPlaces()
        self.generatePieces('w')

    def start(self):
        print("-------------------------\n     JOGO DAS DAMAS\n-------------------------\n")
        self.generatePlaces()
        self.showTable()

    # ================================ #

    def getPiecePositions(self, type):
        coords = []
        for i in range(10):
            for j in range(10):
                if (self.places[i][j] == type):
                    if (type == 'b'):
                        coords.append((i, j))
                    elif (type == 'w'):
                        coords.append((i, j))
        return coords

    def getPossibleMovements(self, selectedCoord):
        def getRainhaMovements(table, selectedPlace):
            pass

        def getDamaMovements(table, selectedPlace):
            pieceMovements = []
            moves = []
            if (selectedPlace == 'b'):
                if (selectedCoord[0] < 9 and selectedCoord[1] < 9):
                    pieceMovements.append((
                        selectedCoord[0]+1, selectedCoord[1]+1))
                if (selectedCoord[0] < 9 and selectedCoord[1] > 0):
                    pieceMovements.append((
                        selectedCoord[0]+1, selectedCoord[1]-1))
            elif (selectedPlace == 'w'):
                if (selectedCoord[0] > 0 and selectedCoord[1] < 9):
                    pieceMovements.append((
                        selectedCoord[0]-1, selectedCoord[1]+1))
                if (selectedCoord[0] > 0 and selectedCoord[1] > 0):
                    pieceMovements.append((
                        selectedCoord[0]-1, selectedCoord[1]-1))
            for m in pieceMovements:
                if (table[m[0]][m[1]] == " "):
                    moves.append(m)
            return moves

        table = self.places
        selectedPlace = table[selectedCoord[0]][selectedCoord[1]]
        if (selectedPlace.isupper()):  # RAINHA
            return getRainhaMovements(table, selectedPlace)
        else:  # DAMA
            return getDamaMovements(table, selectedPlace)

    def movePiece(self, pieceCoord, selectedCoord, pieceType):
        self.places[selectedCoord[0]][selectedCoord[1]] = pieceType
        self.places[pieceCoord[0]][pieceCoord[1]] = " "
        print(self.places[pieceCoord[0]][pieceCoord[1]])
