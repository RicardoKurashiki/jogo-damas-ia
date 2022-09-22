import table as t
import coordinates as c

table = t.Table()
gameIsOn = True
turn = 0


def getPlayerMove():
    def getPlayerPosition():
        playerInputValid = False
        playerPosition = (0, 0)
        playerPieces = table.getPiecePositions('w')
        while not playerInputValid:
            for piece in playerPieces:
                if (piece == playerPieces[-1]):
                    print(f"({piece[0]}, {piece[1]})")
                else:
                    print(f"({piece[0]}, {piece[1]})", end=", ")
            try:
                userI = int(input("Escolha a linha: "))
                userJ = int(input("Escolha a coluna: "))
                playerPosition = (userI, userJ)
                if (playerPosition not in playerPieces):
                    raise
                playerInputValid = True
            except:
                print("Jogada inválida, tente novamente.")
                playerInputValid = False
        return (playerPosition, table.places[playerPosition[0]][playerPosition[1]])

    def getPlayerNextMove(possibleMovements=[]):
        playerInputValid = False
        nextMove = (0, 0)
        while not playerInputValid:
            print(possibleMovements)
            try:
                userI = int(input("Escolha a linha: "))
                userJ = int(input("Escolha a coluna: "))
                nextMove = (userI, userJ)
                if nextMove not in possibleMovements:
                    raise
                playerInputValid = True
            except:
                print("Jogada inválida, tente novamente.")
                playerInputValid = False
        return nextMove

    possibleMovements = []
    while len(possibleMovements) == 0:
        (playerPos, pieceType) = getPlayerPosition()
        possibleMovements = table.getPossibleMovements(playerPos)
        if (len(possibleMovements) == 0):
            print("Escolha uma peça válida")
    print(f"Posição escolhida: {playerPos[0]}, {playerPos[1]}")

    nextMove = getPlayerNextMove(possibleMovements)
    return {"current": playerPos, "next": nextMove, "piece": pieceType}


table.start()

while gameIsOn:
    if turn == 0:
        move = getPlayerMove()
        turn = 1
        table.movePiece(move["current"], move["next"], move["piece"])
        table.showTable()
    else:
        # move = getAIMove()
        turn = 0
