# 0 - Espaco vazio
# 1 - Peca preta
# 2 - Peca branca

emptySpace = " "
blackPiece = "b"
whitePiece = "w"
# Para as rainhas, faz um .toupper()
class Table:
    def __init__(self):
        self.table = []
        self.blacks = 0
        self.whites = 0

    def generateTable(self):
        def generatePieces(type, rows, inverted=False):
            cont = 0
            for i in range(rows):
                spaces = []
                for j in range(10):
                    if (inverted):
                        if (cont % 2 == 0):
                            spaces.append(0)
                        else:
                            spaces.append(type)
                    else:
                        if (cont % 2 != 0):
                            spaces.append(0)
                        else:
                            spaces.append(type)
                    cont += 1
                self.table.append(spaces)
                cont -= 1
        
        generatePieces(2, 4)
        generatePieces(0, 2)
        generatePieces(1, 4, True)

    def showTable(self):
        for i in range(10):
            print("__", end="")
        print()
        for i in range(10):
            print("|", end=" ")
            for j in range(10):
                if (self.table[i][j] == 0):
                    print(emptySpace, end=" ")
                elif (self.table[i][j] == 1):
                    print(blackPiece, end=" ")
                else:
                    print(whitePiece, end=" ")
            print("|")

    def start(self):
        self.generateTable()
        self.showTable()