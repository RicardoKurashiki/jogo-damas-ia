import coordinates
from enum import Enum


class pieceStatus(Enum):
    QUEEN = 1
    PAWN = 2


class Piece:
    def __init__(self, pieceTeam=coordinates.teams.BLACK, pieceStat = pieceStatus.PAWN, coordinate=coordinates.Coordinate()):
        # Time que a peca faz parte
        self.team = pieceTeam
        # Status da peca, peao ou rainha
        self.status = pieceStat
        # Coordenada atual do contexto.
        self.coord = coordinate
        # Sera populado com as coordenadas de todos os possiveis movimentos.
        self.posMovs = []

    def updatePosMovs(self):
        if self.status == pieceStatus.PAWN:
            if self.coord.line != 0 and self.coord.column != 0:
                
        else:
            