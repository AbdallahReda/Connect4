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


def mainFucntion():
    emptyBoard = []
    Board = initializeBoard(emptyBoard)
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
        FourInRow , _ = findFours(Board)
        if FourInRow:
            printBoard(Board)
            print('                   '+'\033[0;34;47m'+"HUMAN WINS!!!" +'\033[1;37;40m')
            playagain = True if input('Do you want to play again (y/n)?') == 'y' else False
            if playagain:
                mainFucntion()
            break

        #AI
        aiMove    = 'o'
        aiTurnCol  = MiniMaxAlphaBeta(Board, depth, aiMove)
        Board ,row , col = makeMove(Board, aiTurnCol, aiMove)
        FourInRow , _ = findFours(Board)
        if FourInRow:
            printBoard(Board)
            print('                   '+'\033[0;31;47m'+"AI WINS!!!" +'\033[1;37;40m')
            playagain = True if input('Do you want to play again (y/n)?') == 'y' else False
            if playagain:
                mainFucntion()
            break

        printBoard(Board)



mainFucntion()





'''
emptyBoard = []
Board = initializeBoard(emptyBoard)
printBoard(Board)
depth = int(input("Enter Diff: "),10)

playagain = False
while(1):

    if isBoardFilled(Board) :
        print("GAME OVER")
        break


    #HUMAN
    HumanTurnCol = human(Board)
    HumanMove    = 'x'
    Board, row , col = makeMove(Board, HumanTurnCol, HumanMove)
    FourInRow , _ = findFours(Board)
    if FourInRow:
        printBoard(Board)
        print('                   '+'\033[0;34;47m'+"HUMAN WINS!!!" +'\033[1;37;40m')
        playagain = True if input('Do you want to play again (y/n)?') == 'y' else False

        if playagain:

        break

    #AI
    aiMove    = 'o'
    aiTurnCol  = MiniMaxAlphaBeta(Board, depth, aiMove)
    Board ,row , col = makeMove(Board, aiTurnCol, aiMove)
    FourInRow , _ = findFours(Board)
    if FourInRow:
        printBoard(Board)
        print('                   '+'\033[0;31;47m'+"AI WINS!!!" +'\033[1;37;40m')
        break

    printBoard(Board)


'''