from ssl import HAS_NEVER_CHECK_COMMON_NAME


class table:
    def __init__(self, table):
        self.table = table;

def think(table, time):
    for i in range(0, 10):
        for j in range(0, 10):
            # print(f"i : {i} | j : {j} | value: {table[i][j]}")
            if table[i][j] != 0 and table[i][j] == time:
                hasAvailableMove(i, j, table)

def play():
    print("Playing")

def hasAvailableMove(i, j, table):
    team = table[i][j]
    possibleMovs = list()
    upDown = 0
    lastHouse = 0
    enemy = 0
    hasEnemy = False
    
    if team == 2:
        upDown = 1
        lastHouse = 9
        enemy = 1
    else:
        upDown = -1
        lastHouse = 0
        enemy = 2

    # Se for branca, e ja estiver na posicao 9, nao tem como "descer" mais.
    # Se for preta, e ja estiver na posicao 0, nao tem como "subir" mais.
    if i != lastHouse:
        # Se j > 0, verifica jogada para a esquerda.
        # Se o valor da casa seguinte for 0 ou inimigo, atribui como uma possivel jogada.
        if (j > 0) and ((table[i+upDown][j-1] == 0) or (table[i+upDown][j-1] == enemy)):
            if (table[i+upDown][j-1] == enemy):
                hasEnemy = True
            jogada = [i+upDown, j-1]
            possibleMovs.append(jogada)

        # Se j < 9, verifica jogada para a direita.
        if (j < 9) and ((table[i+upDown][j+1] == 0) or (table[i+upDown][j+1] == enemy)):
            if hasEnemy == True:
                if table[i+upDown][j+1] == enemy:
                    jogada = [i+upDown, j+1]
                    possibleMovs.append(jogada)
            else:
                jogada = [i+upDown, j+1]
                possibleMovs.append(jogada)

    if team == 2 and len(possibleMovs) > 0:
        print(f"Branca {i},{j}:")
    elif team == 1 and len(possibleMovs) > 0:
        print(f"Preta {i},{j}:")

    for i in range(0, len(possibleMovs)):
        print(f">> {possibleMovs[i][0]},{possibleMovs[i][1]}")
    
    return possibleMovs