import table as t
import coordinates as c

table = t.Table()

table.start()

gameIsOn = True
turn = 'w'


def getPlayerMove(possibleMovements=[]) -> int:
    playerInputValid = False
    while not playerInputValid:
        try:
            userInput = int(input("Digite qual jogada deseja fazer: "))
            # if not (userInput in possibleMovements):
            #     raise
            playerInputValid = True
        except:
            print("Jogada inválida, tente novamente.")
            playerInputValid = False
    return userInput


def getAIMove(possibleMovements=[]) -> int:
    # passa uma lista de movimentos para a IA
    # A IA escolhe o movimento que possui a melhor chance de vitoria
    # retorna a opcao que referencia aquele movimento
    pass


def play(table, turn):
    print("PLACAR: ", table.black, " x ", table.whites)
    if (turn == 'b'):
        print("\nit's black's turn")
        turn == 'w'
    else:
        print("\nit's white's turn")
        turn == 'b'
    table.showTable()
    if (table.black == 0 or table.whites == 0):
        print("END GAME")
        return

    if (turn == 'b'):
        pass

blacks = table.getPiecePositions('b')
for b in blacks:
    print(f"{b.line} - {b.column}")

# while (gameIsOn):
#     play(table, turn)
