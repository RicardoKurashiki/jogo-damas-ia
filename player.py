"""
Esta classe será responsável pelas jogadas do player, assim como validações
Seguir o design de Factory, na main chamar apenas .play() --return-> Context()
"""
from definitions import *
from context import Context
from piece import Piece

class Player:
    def __init__(self, team):
        self.team = Definitions().intToTeam[team]

    def validateInput(self, playerInput):
        v1 = playerInput.isnumeric()
        if (not v1):
            print("Escolha inválida. Tente novamente.")
        return v1

    def validatePosByPiece(self, position, table):
        v1 = (Piece(table[position[0]][position[1]]).team == self.team)
        if (not v1):
            print("Peça inválida. Tente novamente.")
        return v1

    def getCurrentPos(self, table):
        currentPos = [0,0]
        posValid = False
        while not posValid:
            lineValid = False
            while not lineValid:
                userLine = input("Entre a linha atual: ")
                lineValid = self.validateInput(userLine)

            columnValid = False
            while not columnValid:
                userColumn = input("Entre a coluna atual: ")
                columnValid = self.validateInput(userColumn)

            currentPos = [int(userLine), int(userColumn)]
            posValid = self.validatePosByPiece(currentPos, table)
        return currentPos

    def getNextPos(self, currentPos, possibleMoves, table):
        def showPossibleMoves():
            print(f"{currentPos[0]}, {currentPos[1]}", end=" >> ")
            for m in possibleMoves:
                print(f"[{m[0]}, {m[1]}]", end=" ")
            print()
        
        nextPos = [0,0]
        moveValid = False
        while not moveValid:
            showPossibleMoves()
            lineValid = False
            while not lineValid:
                userLine = input("Entre a próxima linha: ")
                lineValid = self.validateInput(userLine)

            columnValid = False
            while not columnValid:
                userColumn = input("Entre a próxima coluna: ")
                columnValid = self.validateInput(userColumn)

            nextPos = [int(userLine),int(userColumn)]
            piece = Piece(table[currentPos[0]][currentPos[1]])
            context = Context(currentPos, nextPos, piece)
            moveValid = (nextPos in possibleMoves)
            if (not moveValid):
                print("Escolha um dos movimentos listados.")
        return context

    def possibleMoves(self, currentPos, table):
        def stoneMoves():
            possibleEnemyMoves=[]
            possibleFreeMoves=[]
            currentLine = currentPos[0]
            currentColumn = currentPos[1]
            upDown = 0
            lastHouse = 0
            
            if (piece.team == Team.WHITE):
                upDown = 1
                lastHouse = 9
            else:
                upDown = -1
                lastHouse = 0
                
            if (currentLine != lastHouse):
                if (currentColumn > 0) and (Piece(table[currentLine+upDown][currentColumn-1]).team != piece.team):
                    leftMove = [currentLine+ upDown, currentColumn - 1]
                    leftMovePiece = Piece(table[leftMove[0]][leftMove[1]]) 

                    if (leftMovePiece.team == enemy) and (leftMove[0] != lastHouse) and (leftMove[1] != 0) and (Piece(table[currentLine + 2*upDown][currentColumn - 2]).team == Team.BLANK):
                        leftMove = [currentLine + 2*upDown, currentColumn - 2]
                        possibleEnemyMoves.append(leftMove)
                    elif leftMovePiece.team == Team.BLANK:
                        possibleFreeMoves.append(leftMove)

                if (currentColumn < 9) and (Piece(table[currentLine+upDown][currentColumn+1]).team != piece.team):
                    rightMove = [currentLine + upDown, currentColumn + 1]
                    rightMovePiece = Piece(table[rightMove[0]][rightMove[1]])

                    if (rightMovePiece.team == enemy) and (rightMove[0] != lastHouse) and (rightMove[1] != 9) and (Piece(table[currentLine + 2*upDown][currentColumn + 2]).team == Team.BLANK):
                        rightMove = [currentLine + 2*upDown, currentColumn + 2]
                        possibleEnemyMoves.append(rightMove)
                    elif rightMovePiece.team == Team.BLANK:
                        possibleFreeMoves.append(rightMove)

            if (len(possibleEnemyMoves) > 0):
                return possibleEnemyMoves
            else:
                return possibleFreeMoves

        def dameMoves():
            def topLeft():
                pass
            def topRight():
                pass
            def bottomLeft():
                pass
            def bottomRight():
                pass

        piece = Piece(table[currentPos[0]][currentPos[1]])
        enemy = Team.BLANK
        if (piece.team == Team.BLACK):
            enemy = Team.WHITE
        else:
            enemy = Team.BLACK

        if (piece.type == Type.PEDRA):
            return stoneMoves()
        else:
            return dameMoves()

    def play(self, table):
        possibleMoves=[]
        currentPos=[0,0]
        while (len(possibleMoves) == 0):
            currentPos = self.getCurrentPos(table)
            possibleMoves = self.possibleMoves(currentPos, table)
            if (len(possibleMoves) == 0):
                print("Esta peça não possui movimentos válidos.")
        context = self.getNextPos(currentPos, possibleMoves, table)
        return context