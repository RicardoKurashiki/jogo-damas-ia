from piece import Piece
from definitions import *

class table:
    def __init__(self, table):
        self.table = table;

def think(table, team):
    
    if (team == Team.BLACK):
        print("\nBlack Moves:")
    else:
        print("\nWhite Moves:")

    for i in range(0, 10):
        for j in range(0, 10):
            # Pega as informacoes da posicao i, j do tabuleiro.
            piece = Piece(table[i][j]) 
            # Se o time da posicao i, j for o mesmo time passado para o alfabeta.
            if (piece.team == team):
                plays = list()

                if (piece.type == Type.PEDRA):
                    plays = getStoneAvailableMoves(i, j, table)
                else:
                    plays = getDameAvailableMoves(i, j, table)

                if (len(plays) > 0):
                    debugString = f"{i},{j} >> " 
                    for moves in plays:
                        debugString += (f"[{moves[0]},{moves[1]}]  ")

                    print(debugString)

def play():
    print("Playing")

def getStoneAvailableMoves(i, j, table):
    piece = Piece(table[i][j])
    possibleFreeMoves = list() # Lista de movimentos possíveis de forma geral.
    possibleEnemyMoves = list() # Lista de movimentos possíveis para caso tenha um inimigo.
    upDown = 0
    lastHouse = 0
    enemy = 0
    
    if (piece.team == Team.WHITE):
        upDown = 1
        lastHouse = 9
        enemy = Team.BLACK
    else:
        upDown = -1
        lastHouse = 0
        enemy = Team.WHITE

    # -------------- Verificacao de Possivel Jogada --------------
    # Se for branca, e ja estiver na posicao 9, nao tem como "descer" mais.
    # Se for preta, e ja estiver na posicao 0, nao tem como "subir" mais.
    if (i != lastHouse):

        # Se j > 0, verifica jogada para a esquerda.
        if (j > 0) and (Piece(table[i+upDown][j-1]).team != piece.team):
            leftMove = [i + upDown, j - 1]
            leftMovePiece = Piece(table[leftMove[0]][leftMove[1]]) 

            if (leftMovePiece.team == enemy) and (leftMove[0] != lastHouse) and (leftMove[1] != 0) and (Piece(table[i + 2*upDown][j - 2]).team == Team.BLANK):
                leftMove = [i + 2*upDown, j - 2]
                possibleEnemyMoves.append(leftMove)
            elif leftMovePiece.team == Team.BLANK:
                possibleFreeMoves.append(leftMove)

        # Se j < 9, verifica jogada para a direita.
        if (j < 9) and (Piece(table[i+upDown][j+1]).team != piece.team):
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
        return possibleEnemyMoves
    else:
        return possibleFreeMoves