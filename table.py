from definitions import Definitions

definitions = Definitions()
# Para as rainhas, faz um .toupper()

class Table:
    def __init__(self):
        self.table = []
        self.blacks = 0
        self.whites = 0

    def generateTable(self):
        def generatePieces(type, rows):
            cont = 0
            for i in range(rows):
                spaces = []
                for j in range(10):
                    if (cont % 2 != 0):
                        spaces.append(0)
                    else:
                        spaces.append(type)
                    cont += 1
                self.table.append(spaces)
                cont -= 1
        
        generatePieces(2, 4)
        generatePieces(0, 2)
        generatePieces(1, 4)

    def showTable(self):
        print('\n\n')
        for i in range(10):
            print(f"{i} |", end=" ")
            for j in range(10):
                if (self.table[i][j] == 0):
                    print(definitions.emptyString, end=" ")
                elif (self.table[i][j] == 1):
                    print(definitions.blackPieceString, end=" ")
                else:
                    print(definitions.whitePieceString, end=" ")
            print()
        for i in range(12):
            print("--", end="")
        print()
        print("  |", end="")
        for i in range(10):
            print(f" {i}", end="")
        print('\n')

    def start(self):
        self.blacks = 20
        self.whites = 20
        self.generateTable()
        self.showTable()
        

    # =============================== #

    def move(self, context):

        def clearPlaces():
            for i in range(int(context.getDistance())):
                if (context.getDirection() == "SE"):
                    self.table[currentPos[0]+i][currentPos[1]+i] = definitions.emptyValue
                elif (context.getDirection() == "SW"):
                    self.table[currentPos[0]+i][currentPos[1]-i] = definitions.emptyValue
                elif (context.getDirection() == "NE"):
                    self.table[currentPos[0]-+i][currentPos[1]+i] = definitions.emptyValue
                elif (context.getDirection() == "NW"):
                    self.table[currentPos[0]-i][currentPos[1]-i] = definitions.emptyValue

        currentPos = context.current
        nextPos = context.next
        clearPlaces()
        self.table[nextPos[0]][nextPos[1]] = context.piece
        self.showTable()