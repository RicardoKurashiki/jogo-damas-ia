from table import Table
from context import Context
from definitions import Definitions

definitions = Definitions()

def choosePiece():
    print(" ------------------------- ")
    print(f"|({definitions.blackPieceValue}) Pretas               |")
    print(f"|({definitions.whitePieceValue}) Brancas              |")
    print(" ------------------------- ")
    return int(input("Escolha sua peça: "))

def playerMove(table, playerPiece):
    def getCurrentPosition():
        isValid = False
        while not isValid:
            userLine = input("Escolha a linha da peça: ")
            userColumn = input("Escolha a coluna da peça: ")
            currentPos = (userLine, userColumn)
            inputValid = validateInput(currentPos)
            if (inputValid):
                currentPos = (int(userLine), int(userColumn))
                isValid = validatePiece(currentPos)
            else:
                print("Entrada inválida. Tente novamente.")
        return currentPos

    def getNextPosition():
        isValid = False
        while not isValid:
            nextLine = input("Escolha a linha: ")
            nextColumn = input("Escolha a coluna: ")
            nextPos = (nextLine, nextColumn)
            inputValid = validateInput(nextPos)
            if (inputValid):
                nextPos = (int(nextLine), int(nextColumn))
                isValid = validateMove(nextPos)
            else:
                print("Entrada inválida. Tente novamente.")
        return nextPos

    def validateInput(position):
        return (position[0].isnumeric() and position[1].isnumeric())

    def validatePiece(position):
        return table[position[0]][position[1]] == playerPiece

    def validateMove(position):
        return table[position[0]][position[1]] != playerPiece

    currentPos = getCurrentPosition()
    nextPos = getNextPosition()
    return Context(currentPos, nextPos, playerPiece)

playerPiece = choosePiece()

t = Table()
t.start()

game = True

while game:
    context = playerMove(t.table, playerPiece)
    t.move(context)
