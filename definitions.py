from enum import Enum

class Team(Enum):
    BLANK = 0
    BLACK = 1
    WHITE = 2

class Type(Enum):
    NONE = 0
    PEDRA = 1
    DAMA = 2

class Definitions:
    intToTeam = {
        Team.BLANK.value: Team.BLANK,
        Team.BLACK.value: Team.BLACK,
        Team.WHITE.value: Team.WHITE,
    }
    intToType = {
        Type.NONE.value: Type.NONE,
        Type.PEDRA.value: Type.PEDRA,
        Type.DAMA.value: Type.DAMA,
    }