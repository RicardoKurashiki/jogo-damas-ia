"""
Essa classe vai ser a responsável por ter os dados do ponto que está sendo analisado no tabuleiro
Piece([2,1]) -> Team = Team.WHITE | Type = Type.PEDRA

getString() -> Vai retornar o valor simbólico da peça analisada :: "w"
getValue() -> Vai retornar o valor real da peça analisada :: [2, 1]
"""


from definitions import *

class Piece:
    def __init__(self, data=[0, 0]):
        self.team = Definitions().intToTeam[data[0]]
        self.type = Definitions().intToType[data[1]]
    
    # values = {
    #         [Team.BLACK, Type.PEDRA]: (Team.BLACK, Type.PEDRA),
    #         [Team.WHITE, Type.PEDRA]: (Team.WHITE, Type.PEDRA),
    #         [Team.BLACK, Type.DAMA]: (Team.BLACK, Type.DAMA),
    #         [Team.WHITE, Type.DAMA]: (Team.WHITE, Type.DAMA),
    #     }

    # def getData(self, posData):
    #     (self.team, self.type) = self.values[posData]
    
    def getString(self):
        values = {
        (Team.BLANK, Type.NONE): " ",
        (Team.BLACK, Type.PEDRA): "b",
        (Team.WHITE, Type.PEDRA): "w",
        (Team.BLACK, Type.DAMA): "B",
        (Team.WHITE, Type.DAMA): "W",
        }
        return values[(self.team, self.type)]
    
    def getValue(self):
        return [self.team.value, self.type.value]