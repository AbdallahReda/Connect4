from minimaxAlphaBeta import *
from connect4board import *

def human(Board):
    Col = input("Choose a Column between 1 and 7: ")
    
    if not(Col.isdigit()):
        print("Input must be integer!")
        return human(Board)

    Col = int(Col) - 1
    if Col < 0 or Col > 6:
        print("Column must be between 1 and 7!")
        return human(Board)
    if isColumnFilled(Board, Col):
        print("The Column you select is full!")
        return human(Board)
    return Col




emptyBoard = []
Board = initializeBoard(emptyBoard)
#Board[0][0] = 'x'
#oard[1][0] = 'x'
#Board[2][0] = 'x'
#Board[3][0] = 'x'
#Board[4][0] = 'x'
#Board[5][0] = 'x'
#Board[5][1] = 'x'
#Board[4][1] = 'o'
printBoard(Board)
depth = int(input("Enter Diff: "),10)


while(1):

    if isBoardFilled(Board) :
        print("GAME OVER")
        break

    #HUMAN
    HumanTurnCol = human(Board)
    HumanMove    = 'x'
    Board, row , col = makeMove(Board, HumanTurnCol, HumanMove)
    if checkFours(Board, row, col)[0]:
        findFours(Board)
        printBoard(Board)
        print('                   '+'\033[0;34;47m'+"HUMAN WINS!!!" +'\033[1;37;40m')        
        break


    #AI
    aiMove    = 'o'
    aiTurnCol  = MiniMaxAlphaBeta(Board, depth, aiMove)
    Board ,row , col = makeMove(Board, aiTurnCol, aiMove)
    if checkFours(Board, row, col)[0]:
        findFours(Board)[0]
        printBoard(Board)
        print('                   '+'\033[0;31;47m'+"AI WINS!!!" +'\033[1;37;40m')
        #piece1  = checkFours(Board, row, col)[1]
        break


    printBoard(Board)