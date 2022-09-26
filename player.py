"""
Esta classe será responsável pelas jogadas do player, assim como validações
Seguir o design de Factory, na main chamar apenas .play() --return-> Context()
"""
from definitions import *
from context import Context
from piece import Piece
from table import Table


class Player:
    def __init__(self, team):
        self.team = Definitions().intToTeam[team]
        self.capturing = False
        self.logs = []

    def validateInput(self, playerInput):
        if (playerInput == ''):
            return False
        v1 = playerInput.isnumeric()
        if (not v1):
            print("Escolha inválida. Tente novamente.")
        v2 = int(playerInput) >= 0 and int(playerInput) < 10
        if (not v2):
            print("Valor inválido. Tente novamente.")
        return (v1 and v2)

    def validatePosByPiece(self, position, table):
        v1 = (Piece(table[position[0]][position[1]]).team == self.team)
        if (not v1):
            print("Peça inválida. Tente novamente.")
        return v1

    def getCurrentPos(self, table):
        currentPos = [0, 0]
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

        nextPos = [0, 0]
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

            nextPos = [int(userLine), int(userColumn)]
            piece = Piece(table[currentPos[0]][currentPos[1]])
            context = Context(currentPos, nextPos, piece)
            moveValid = (nextPos in possibleMoves)
            if (not moveValid):
                print("Escolha um dos movimentos listados.")
        return context

    def possibleMoves(self, currentPos, table):
        def stoneMoves():
            i = currentPos[0]
            j = currentPos[1]
            piece = Piece(table[i][j])
            # Lista de movimentos possíveis de forma geral.
            possibleFreeMoves = list()
            # Lista de movimentos possíveis para caso tenha um inimigo.
            possibleEnemyMoves = list()
            upDown = 0
            lastHouse = 0
            canReverseEat = False

            if (piece.team == Team.WHITE):
                upDown = 1
                lastHouse = 9
                canReverseEat = i > 1
            else:
                upDown = -1
                lastHouse = 0
                canReverseEat = i < 8

            # -------------- Verificacao de Possivel Jogada --------------
            # Se for branca, e ja estiver na posicao 9, nao tem como "descer" mais.
            # Se for preta, e ja estiver na posicao 0, nao tem como "subir" mais.

            if (canReverseEat == True) and (j > 1) and (Piece(table[i-upDown][j-1]).team == enemy) and (Piece(table[i - 2*upDown][j - 2]).team == Team.BLANK):
                revMove = [i - 2*upDown, j - 2]
                possibleEnemyMoves.append(revMove)

            if (canReverseEat == True) and (j < 8) and (Piece(table[i-upDown][j+1]).team == enemy) and (Piece(table[i - 2*upDown][j + 2]).team == Team.BLANK):
                revMove = [i - 2*upDown, j + 2]
                possibleEnemyMoves.append(revMove)

            if (i != lastHouse) and (j > 0) and (Piece(table[i+upDown][j-1]).team != piece.team):
                leftMove = [i + upDown, j - 1]
                leftMovePiece = Piece(table[leftMove[0]][leftMove[1]])

                if (leftMovePiece.team == enemy) and (leftMove[0] != lastHouse) and (leftMove[1] != 0) and (Piece(table[i + 2*upDown][j - 2]).team == Team.BLANK):
                    leftMove = [i + 2*upDown, j - 2]
                    possibleEnemyMoves.append(leftMove)
                elif leftMovePiece.team == Team.BLANK:
                    possibleFreeMoves.append(leftMove)

            if (i != lastHouse) and (j < 9) and (Piece(table[i+upDown][j+1]).team != piece.team):
                rightMove = [i + upDown, j + 1]
                rightMovePiece = Piece(table[rightMove[0]][rightMove[1]])

                if (rightMovePiece.team == enemy) and (rightMove[0] != lastHouse) and (rightMove[1] != 9) and (Piece(table[i + 2*upDown][j + 2]).team == Team.BLANK):
                    rightMove = [i + 2*upDown, j + 2]
                    possibleEnemyMoves.append(rightMove)
                elif rightMovePiece.team == Team.BLANK:
                    possibleFreeMoves.append(rightMove)

            if (len(possibleEnemyMoves) > 0):
                self.capturing = True
                return possibleEnemyMoves
            else:
                self.capturing = False
                return possibleFreeMoves

        def dameMoves():
            currentLine = currentPos[0]
            currentColumn = currentPos[1]
            piece = Piece(table[currentLine][currentColumn])
            # Lista de movimentos possíveis de forma geral.
            possibleFreeMoves = list()
            # Lista de movimentos possíveis para caso tenha um inimigo.
            possibleEnemyMoves = list()
            enemy = 0

            if (piece.team == Team.WHITE):
                enemy = Team.BLACK
            else:
                enemy = Team.WHITE

            # Movimento CIMA ESQUERDA
            if (currentLine > 0) and (currentColumn > 0):
                delta = 1
                while ((currentLine - delta) > -1) and ((currentColumn - delta) > -1):
                    upLeft = [currentLine - delta, currentColumn - delta]
                    upLeftPiece = Piece(table[upLeft[0]][upLeft[1]])

                    if (upLeftPiece.team == enemy) and (upLeft[0] != 0) and (upLeft[1] != 0):
                        if (Piece(table[currentLine - (delta+1)][currentColumn - (delta+1)]).team == Team.BLANK):
                            upLeft = [currentLine -
                                      (delta+1), currentColumn - (delta+1)]
                            possibleEnemyMoves.append(upLeft)
                        break
                    elif (upLeftPiece.team == Team.BLANK):
                        possibleFreeMoves.append(upLeft)
                    elif (upLeftPiece.team == piece.team):
                        break

                    delta += 1

            # Movimento BAIXO DIREITA
            if (currentLine < 9) and (currentColumn < 9):
                delta = 1
                while ((currentLine + delta) < 10) and ((currentColumn + delta) < 10):
                    downRight = [currentLine + delta, currentColumn + delta]
                    downRightPiece = Piece(table[downRight[0]][downRight[1]])

                    if ((downRightPiece.team == enemy) and (downRight[0] != 9) and (downRight[1] != 9)):
                        if Piece(table[currentLine + (delta+1)][currentColumn + (delta+1)]).team == Team.BLANK:
                            downRight = [currentLine +
                                         (delta+1), currentColumn + (delta+1)]
                            possibleEnemyMoves.append(downRight)
                        break
                    elif (downRightPiece.team == Team.BLANK):
                        possibleFreeMoves.append(downRight)
                    elif (downRightPiece.team == piece.team):
                        break

                    delta += 1

            # Movimento CIMA DIREITA
            if (currentLine > 0) and (currentColumn < 9):
                delta = 1
                while ((currentLine - delta) > -1) and ((currentColumn + delta) < 10):
                    upRight = [currentLine - delta, currentColumn + delta]
                    upRightPiece = Piece(table[upRight[0]][upRight[1]])

                    if (upRightPiece.team == enemy) and (upRight[0] != 0) and (upRight[1] != 9):
                        if (Piece(table[currentLine - (delta+1)][currentColumn + (delta+1)]).team == Team.BLANK):
                            upRight = [currentLine -
                                       (delta+1), currentColumn + (delta+1)]
                            possibleEnemyMoves.append(upRight)
                        break
                    elif (upRightPiece.team == Team.BLANK):
                        possibleFreeMoves.append(upRight)
                    elif (upRightPiece.team == piece.team):
                        break

                    delta += 1

            # Movimento BAIXO ESQUERDA
            if (currentLine < 9) and (currentColumn > 0):
                delta = 1
                while ((currentLine + delta) < 10) and ((currentColumn - delta) != -1):
                    downLeft = [currentLine + delta, currentColumn - delta]
                    downLeftPiece = Piece(table[downLeft[0]][downLeft[1]])

                    if (downLeftPiece.team == enemy) and (downLeft[0] != 9) and (downLeft[1] != 0):
                        if (Piece(table[currentLine + (delta+1)][currentColumn - (delta+1)]).team == Team.BLANK):
                            downLeft = [currentLine +
                                        (delta+1), currentColumn - (delta+1)]
                            possibleEnemyMoves.append(downLeft)
                        break
                    elif (downLeftPiece.team == Team.BLANK):
                        possibleFreeMoves.append(downLeft)
                    elif (downLeftPiece.team == piece.team):
                        break

                    delta += 1

            if (len(possibleEnemyMoves) > 0):
                self.capturing = True
                return possibleEnemyMoves
            else:
                self.capturing = False
                return possibleFreeMoves

        piece = Piece(table[currentPos[0]][currentPos[1]])
        enemy = Team.BLANK
        if (piece.team == Team.BLACK):
            enemy = Team.WHITE
        else:
            enemy = Team.BLACK

        if (piece.type == Type.PEDRA):
            return stoneMoves()
        elif (piece.type == Type.DAMA):
            return dameMoves()

    def play(self, tableClass):
        table = tableClass.table
        possibleMoves = []
        currentPos = [0, 0]
        if (len(self.logs) > 0 and self.logs[-1].capturing):
            currentPos = self.logs[-1].nextPos
            possibleMoves = self.possibleMoves(currentPos, table)
            if (len(possibleMoves) == 0):
                print("Esta peça não possui movimentos válidos.")
        else:
            while (len(possibleMoves) == 0):
                currentPos = self.getCurrentPos(table)
                possibleMoves = self.possibleMoves(currentPos, table)
                if (len(possibleMoves) == 0):
                    print("Esta peça não possui movimentos válidos.")
        if (len(possibleMoves) > 0):
            context = self.getNextPos(currentPos, possibleMoves, table)
            tempTable = Table()
            tempTable.copy(tableClass)
            captured = tempTable.move(context, False)
            self.possibleMoves(context.nextPos, tempTable.table)
            context.capturing = captured and self.capturing
            self.logs.append(context)
            return context
        else:
            captured = False
            self.capturing = False
