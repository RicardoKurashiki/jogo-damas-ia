from math import inf
from piece import Piece
from definitions import *
from context import Context
from table import Table
import time

class EvaluatedMove:
    def __init__(self, context = Context([0,0],[0,0],Piece([0,0])), evaluation = 0):
        self.context = context
        self.evaluation = evaluation

class PossibleMoves:
    def __init__(self, hasEnemy, movesBuffer):
        self.hasEnemy = hasEnemy
        self.movesBuffer = movesBuffer


class AlphaBeta:
    def __init__(self, team):
        self.team = team
        self.lastMove = EvaluatedMove()

    def checkIfHasCascade(self, tableClass):
        allMoves = getAvailableTeamMovements(tableClass.table, self.team)
        if allMoves.hasEnemy:
            for moveContext in allMoves.movesBuffer:
                eatCounter = getEatCounter(tableClass, moveContext)
                if (eatCounter > 1):
                    moveContext.capturing = True
                    return moveContext
        return None

    def playCascade(self, tableClass, move, listMoves=[]):
        movementList = listMoves
        movementList.append(move)
        tempTable = Table()
        tempTable.copy(tableClass)
        tempTable.move(move, False)
        posMoves = possibleMoves(move.nextPos, tempTable.table)
        eatValues = {}
        for coord in posMoves:
            context = Context(move.nextPos, coord, move.piece, True)
            counter = getEatCounter(tempTable, context)
            if (counter != 0):
                eatValues[f"{coord[0]},{coord[1]}"] = counter
        if (len(eatValues) == 0):
            movementList[-1].capturing = False
            return movementList
        maxEat = -inf
        c = ""
        for k in eatValues.keys():
            if (eatValues[k] >= maxEat):
                maxEat = eatValues[k]
                c = k
        selectedCoord = [int(c.split(',')[0]),int(c.split(',')[1])]
        context = Context(move.nextPos, selectedCoord, move.piece, True)
        
        return self.playCascade(tempTable, context, movementList)

    def think(self, tableClass):
        print("Pensando...")

        cascade = self.checkIfHasCascade(tableClass)

        if (cascade != None):
            move = self.playCascade(tableClass, cascade)
        else:
            self.lastMove = self.minimax(tableClass, -inf, inf, 2, self.team)
            move = self.lastMove.context
        
        if (type(move) is list):
            for m in move:
                print(f"Máquina joga: {m.currentPos[0]},{m.currentPos[1]} >> {m.nextPos[0]},{m.nextPos[1]}")
        else:
            print(f"Máquina joga: {move.currentPos[0]},{move.currentPos[1]} >> {move.nextPos[0]},{move.nextPos[1]}")

        return move

    def minimax(self, tableClass, alpha, beta, depth, team):
        currentEvaluation = EvaluatedMove()
        currentEvaluation.evaluation = getEvaluation(tableClass.table, self.team)
        enemyTeam = Team.WHITE if team == Team.BLACK else Team.BLACK

        if (depth == 0) or (currentEvaluation.evaluation == 0):
            return currentEvaluation

        if self.team == team:
            moveMaxEval = EvaluatedMove()
            moveMaxEval.context = Context([0,0],[0,0],Piece([0,0]))
            moveMaxEval.evaluation = -inf

            possibleMoves = getAvailableTeamMovements(tableClass.table, team)
            myTable = Table()
            
            for move in possibleMoves.movesBuffer:
                myTable.copy(tableClass)
                myTable.move(move, False)

                moveEval = EvaluatedMove()
                moveEval.context = move
                moveEval.evaluation = self.minimax(myTable, alpha, beta, depth-1, enemyTeam).evaluation

                if (moveMaxEval.evaluation < moveEval.evaluation):
                    moveMaxEval = moveEval

                if (alpha < moveEval.evaluation):
                    alpha = moveEval.evaluation
                
                if (beta <= alpha):
                    break;

            return moveMaxEval
        else:
            moveMinEval = EvaluatedMove()
            moveMinEval.context = Context([0,0],[0,0],Piece([0,0]))
            moveMinEval.evaluation = inf

            possibleMoves = getAvailableTeamMovements(tableClass.table, team)
            
            myTable = Table()

            for move in possibleMoves.movesBuffer:
    
                myTable.copy(tableClass)
                myTable.move(move, False)

                moveEval = EvaluatedMove()
                moveEval.context = move

                moveEval.evaluation = self.minimax(myTable, alpha, beta, depth-1, enemyTeam).evaluation

                if (moveMinEval.evaluation > moveEval.evaluation):
                    moveMinEval = moveEval
                
                if (beta > moveEval.evaluation):
                    beta = moveEval.evaluation
                
                if (beta <= alpha):
                    break;
            
            return moveMinEval


def getEvaluation(table, team):
    evaluation = 0
    blackPieces = getPiecesNumber(table, Team.BLACK)
    whitePieces = getPiecesNumber(table, Team.WHITE)

    if (team == Team.BLACK) and whitePieces != 0:
        evaluation = (blackPieces/whitePieces)*1000
    elif blackPieces != 0:
        evaluation = (whitePieces/blackPieces)*1000

    return evaluation

def getEatCounter(table, context):
    counter = 0
    
    myTable = Table()
    myTable.copy(table)

    currentPosition = context.currentPos
    availableMovements = getStoneAvailableMoves(currentPosition[0], currentPosition[1], myTable.table)

    while (availableMovements.hasEnemy == True and len(availableMovements.movesBuffer) > 0):
        counter += 1
        context = Context(currentPosition, availableMovements.movesBuffer[0], context.piece)
        myTable.move(context)
        currentPosition = availableMovements.movesBuffer[0]
        availableMovements = getStoneAvailableMoves(currentPosition[0], currentPosition[1], myTable.table)

    return counter

def getPiecesNumber(table, team):
    counter = 0
    for i in range(10):
        for j in range(10):
            if Piece(table[i][j]).team == team:
                if Piece(table[i][j]).type == Type.DAMA:
                    counter += 5
                else:
                    counter += 1
    return counter

def getAvailableTeamMovements(table, team):
    possibleFreeMoves = list()
    possibleEnemyMoves = list()

    for i in range(0, 10):
        for j in range(0, 10):
            piece = Piece(table[i][j]) 
            
            if (piece.team == team):
                plays = PossibleMoves(False, list())
                
                if (piece.type == Type.PEDRA):
                    plays = getStoneAvailableMoves(i, j, table)
                else:
                    plays = getDameAvailableMoves(i, j, table)

                if (plays.hasEnemy == True):
                    if (len(plays.movesBuffer) > 0):
                        for moves in plays.movesBuffer:
                            move = Context([i, j], [moves[0], moves[1]], piece)
                            possibleEnemyMoves.append(move)
                else:
                    if (len(plays.movesBuffer) > 0):
                        for moves in plays.movesBuffer:
                            move = Context([i, j], [moves[0], moves[1]], piece)
                            possibleFreeMoves.append(move)
    
    pieceTeam = "B" if team == Team.BLACK else "W"
    if (len(possibleEnemyMoves) > 0):
        # for move in possibleEnemyMoves:
        #     print(f"{pieceTeam}[{move.currentPos[0]},{move.currentPos[1]}] >> [{move.nextPos[0]},{move.nextPos[1]}]")
        return PossibleMoves(True, possibleEnemyMoves)
    else:
        # for move in possibleFreeMoves:
        #     print(f"{pieceTeam}[{move.currentPos[0]},{move.currentPos[1]}] >> [{move.nextPos[0]},{move.nextPos[1]}]")
        return PossibleMoves(False, possibleFreeMoves)

def getStoneAvailableMoves(i, j, table):
    piece = Piece(table[i][j])
    possibleFreeMoves = list() # Lista de movimentos possíveis de forma geral.
    possibleEnemyMoves = list() # Lista de movimentos possíveis para caso tenha um inimigo.
    upDown = 0
    lastHouse = 0
    canReverseEat = False
    enemy = 0
    
    if (piece.team == Team.WHITE):
        upDown = 1
        lastHouse = 9
        canReverseEat = i > 1
        enemy = Team.BLACK
    else:
        upDown = -1
        lastHouse = 0
        canReverseEat = i < 8
        enemy = Team.WHITE

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
        return PossibleMoves(True, possibleEnemyMoves)
    else:
        return PossibleMoves(False, possibleFreeMoves)

def getDameAvailableMoves(i, j, table):
    piece = Piece(table[i][j])
    possibleFreeMoves = list() # Lista de movimentos possíveis de forma geral.
    possibleEnemyMoves = list() # Lista de movimentos possíveis para caso tenha um inimigo.
    enemy = 0
    
    if (piece.team == Team.WHITE):
        enemy = Team.BLACK
    else:
        enemy = Team.WHITE

    # Movimento CIMA ESQUERDA
    if (i > 0) and (j > 0):
        delta = 1;
        while ((i - delta) > -1) and ((j - delta) >  -1):
            upLeft = [i - delta, j - delta]
            upLeftPiece = Piece(table[upLeft[0]][upLeft[1]])

            if (upLeftPiece.team == enemy) and (upLeft[0] != 0) and (upLeft[1] != 0) and (Piece(table[i - (delta+1)][j - (delta+1)]).team == Team.BLANK):
                upLeft = [i - (delta+1), j - (delta+1)]
                possibleEnemyMoves.append(upLeft)
                break
            elif (upLeftPiece.team == Team.BLANK):
                possibleFreeMoves.append(upLeft)
            elif (upLeftPiece.team == piece.team):
                break

            delta += 1
    
    # Movimento BAIXO DIREITA
    if (i < 9) and (j < 9):
        delta = 1;
        while ((i + delta) < 10) and ((j + delta) < 10):
            downRight = [i + delta, j + delta]
            downRightPiece = Piece(table[downRight[0]][downRight[1]])

            if (downRightPiece.team == enemy) and (downRight[0] != 9) and (downRight[1] != 9) and (Piece(table[i + (delta+1)][j + (delta+1)]).team == Team.BLANK):
                downRight = [i + (delta+1), j + (delta+1)]
                possibleEnemyMoves.append(downRight)
                break
            elif (downRightPiece.team == Team.BLANK):
                possibleFreeMoves.append(downRight)
            elif (downRightPiece.team == piece.team):
                break

            delta += 1

    # Movimento CIMA DIREITA
    if (i > 0) and (j < 9):
        delta = 1;
        while ((i - delta) > -1) and ((j + delta) < 10):
            upRight = [i - delta, j + delta]
            upRightPiece = Piece(table[upRight[0]][upRight[1]])

            if (upRightPiece.team == enemy) and (upRight[0] != 0) and (upRight[1] != 9) and (Piece(table[i - (delta+1)][j + (delta+1)]).team == Team.BLANK):
                upRight = [i - (delta+1), j + (delta+1)]
                possibleEnemyMoves.append(upRight)
                break
            elif (upRightPiece.team == Team.BLANK):
                possibleFreeMoves.append(upRight)
            elif (upRightPiece.team == piece.team):
                break

            delta += 1
    
    # Movimento BAIXO ESQUERDA
    if (i < 9) and (j > 0):
        delta = 1;
        while ((i + delta) < 10) and ((j - delta) != -1):
            downLeft = [i + delta, j - delta]
            downLeftPiece = Piece(table[downLeft[0]][downLeft[1]])

            if (downLeftPiece.team == enemy) and (downLeft[0] != 9) and (downLeft[1] != 0) and (Piece(table[i + (delta+1)][j - (delta+1)]).team == Team.BLANK):
                downLeft = [i + (delta+1), j - (delta+1)]
                possibleEnemyMoves.append(downLeft)
                break
            elif (downLeftPiece.team == Team.BLANK):
                possibleFreeMoves.append(downLeft)
            elif (downLeftPiece.team == piece.team):
                break

            delta += 1

    if (len(possibleEnemyMoves) > 0):
        return PossibleMoves(True, possibleEnemyMoves)
    else:
        return PossibleMoves(False, possibleFreeMoves)

def possibleMoves(currentPos, table):
    def stoneMoves():
        i = currentPos[0]
        j = currentPos[1]
        piece = Piece(table[i][j])
        possibleFreeMoves = list() # Lista de movimentos possíveis de forma geral.
        possibleEnemyMoves = list() # Lista de movimentos possíveis para caso tenha um inimigo.
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
            return possibleEnemyMoves
        else:
            return possibleFreeMoves

    def dameMoves():
        currentLine = currentPos[0]
        currentColumn = currentPos[1]
        piece = Piece(table[currentLine][currentColumn])
        possibleFreeMoves = list() # Lista de movimentos possíveis de forma geral.
        possibleEnemyMoves = list() # Lista de movimentos possíveis para caso tenha um inimigo.
        enemy = 0
        
        if (piece.team == Team.WHITE):
            enemy = Team.BLACK
        else:
            enemy = Team.WHITE

        # Movimento CIMA ESQUERDA
        if (currentLine > 0) and (currentColumn > 0):
            delta = 1;
            while ((currentLine - delta) > -1) and ((currentColumn - delta) >  -1):
                upLeft = [currentLine - delta, currentColumn - delta]
                upLeftPiece = Piece(table[upLeft[0]][upLeft[1]])

                if (upLeftPiece.team == enemy) and (upLeft[0] != 0) and (upLeft[1] != 0) and (Piece(table[currentLine - (delta+1)][currentColumn - (delta+1)]).team == Team.BLANK):
                    upLeft = [currentLine - (delta+1), currentColumn - (delta+1)]
                    possibleEnemyMoves.append(upLeft)
                    break
                elif (upLeftPiece.team == Team.BLANK):
                    possibleFreeMoves.append(upLeft)
                elif (upLeftPiece.team == piece.team):
                    break

                delta += 1
        
        # Movimento BAIXO DIREITA
        if (currentLine < 9) and (currentColumn < 9):
            delta = 1;
            while ((currentLine + delta) < 10) and ((currentColumn + delta) < 10):
                downRight = [currentLine + delta, currentColumn + delta]
                downRightPiece = Piece(table[downRight[0]][downRight[1]])

                if (downRightPiece.team == enemy) and (downRight[0] != 9) and (downRight[1] != 9) and (Piece(table[currentLine + (delta+1)][currentColumn + (delta+1)]).team == Team.BLANK):
                    downRight = [currentLine + (delta+1), currentColumn + (delta+1)]
                    possibleEnemyMoves.append(downRight)
                    break
                elif (downRightPiece.team == Team.BLANK):
                    possibleFreeMoves.append(downRight)
                elif (downRightPiece.team == piece.team):
                    break

                delta += 1

        # Movimento CIMA DIREITA
        if (currentLine > 0) and (currentColumn < 9):
            delta = 1;
            while ((currentLine - delta) > -1) and ((currentColumn + delta) < 10):
                upRight = [currentLine - delta, currentColumn + delta]
                upRightPiece = Piece(table[upRight[0]][upRight[1]])

                if (upRightPiece.team == enemy) and (upRight[0] != 0) and (upRight[1] != 9) and (Piece(table[currentLine - (delta+1)][currentColumn + (delta+1)]).team == Team.BLANK):
                    upRight = [currentLine - (delta+1), currentColumn + (delta+1)]
                    possibleEnemyMoves.append(upRight)
                    break
                elif (upRightPiece.team == Team.BLANK):
                    possibleFreeMoves.append(upRight)
                elif (upRightPiece.team == piece.team):
                    break

                delta += 1
        
        # Movimento BAIXO ESQUERDA
        if (currentLine < 9) and (currentColumn > 0):
            delta = 1;
            while ((currentLine + delta) < 10) and ((currentColumn - delta) != -1):
                downLeft = [currentLine + delta, currentColumn - delta]
                downLeftPiece = Piece(table[downLeft[0]][downLeft[1]])

                if (downLeftPiece.team == enemy) and (downLeft[0] != 9) and (downLeft[1] != 0) and (Piece(table[currentLine + (delta+1)][currentColumn - (delta+1)]).team == Team.BLANK):
                    downLeft = [currentLine + (delta+1), currentColumn - (delta+1)]
                    possibleEnemyMoves.append(downLeft)
                    break
                elif (downLeftPiece.team == Team.BLANK):
                    possibleFreeMoves.append(downLeft)
                elif (downLeftPiece.team == piece.team):
                    break

                delta += 1

        if (len(possibleEnemyMoves) > 0):
            return possibleEnemyMoves
        else:
            return possibleFreeMoves

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
