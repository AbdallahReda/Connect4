import os
import math
from copy import deepcopy
from utility import *

RED     = '\033[1;31;40m'
RED_BG  = '\033[0;31;47m'
BLUE_BG = '\033[0;34;47m'
YELLOW  = '\033[1;33;40m'
BLUE    = '\033[1;34;40m'
MAGENTA = '\033[1;35;40m'
CYAN    = '\033[1;36;40m'
WHITE   = '\033[1;37;40m'



#make an empty board
def initializeBoard():
    Board = []
    for i in range(BOARD_HEIGHT):
        Board.append([])
        for j in range(BOARD_WIDTH):
            Board[i].append(' ')
    return Board

#check if the column is filled or not
def isColumnValid(Board, Col):
    if Board[0][Col] == ' ':
        return True
    return False


#check the search range for rows and columns
def isRangeValid(row, col):
    if row >= 0 and col >= 0 and row < BOARD_HEIGHT and col < BOARD_WIDTH:
        return True
    return False

#return all valid moves (empty columns) from the board
def getValidMoves(Board):
    Columns = []
    for Col in range(BOARD_WIDTH):
        if isColumnValid(Board, Col):
            Columns.append(Col)
    return Columns

#places the current move's player ['x'|'o'] in the referenced column in the board
def makeMove(board, col, player):
    #deepcopy is used to take acopy of current board and not affecting the original one
    tempBoard = deepcopy(board)
    for row in range(5,-1,-1):
        if tempBoard[row][col] == ' ':
            tempBoard[row][col] = player
            return tempBoard, row, col

#check if the played move is in empty column or not
def isValidMove(col, board):
    for row in range(BOARD_HEIGHT):
        if board[row][col] == ' ':
            return True
    return False

#check if the board is filled with players' moves
def isBoardFilled(board):
    #Check the first row and Selected colmun if it filled or not
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            if board[row][col]==' ': return False
    return True

#find four or more of ('x'|'o') in arow in any direction
def findFours(board):

    #find four or more of ('x'|'o') in arow in vertical direction
    def verticalCheck(row, col):
        fourInARow = False
        count = 0
        for rowIndex in range(row, BOARD_HEIGHT):
            if board[rowIndex][col] == board[row][col]:
                count += 1
            else:
                break

        if count >= 4:
            fourInARow = True

        return fourInARow, count
    #find four or more of ('x'|'o') in arow in horizontal direction
    def horizontalCheck(row, col):
        fourInARow = False
        count = 0
        for colIndex in range(col, BOARD_WIDTH):
            if board[row][colIndex] == board[row][col]:
                count += 1
            else:
                break

        if count >= 4:
            fourInARow = True

        return fourInARow, count

    #find four or more of ('x'|'o') in arow in postive diagonal direction
    def posDiagonalCheck(row,col):
        # check for diagonals with positive slope
        slope = None
        count = 0
        colIndex = col
        for rowIndex in range(row, BOARD_HEIGHT):
            if colIndex > BOARD_HEIGHT:
                break
            elif board[rowIndex][colIndex] == board[row][col]:
                count += 1
            else:
                break
            colIndex += 1 # increment column when row is incremented

        if count >= 4:
            slope = 'positive'

        return slope, count

    #find four or more of ('x'|'o') in arow in negative diagonal direction
    def negDiagonalCheck(row, col):
        # check for diagonals with positive slope
        slope = None
        count = 0
        colIndex = col
        for rowIndex in range(row, -1, -1):
            if colIndex > 6:
                break
            elif board[rowIndex][colIndex] == board[row][col]:
                count += 1
            else:
                break
            colIndex += 1 # increment column when row is decremented

        if count >= 4:
            slope = 'negative'

        return slope, count

    #find four or more of ('x'|'o') in arow in any diagonal direction
    def diagonalCheck(row,col):
        positiveSlop , positiveCount = posDiagonalCheck(row,col)
        negativeSlop , negativeCount = negDiagonalCheck(row,col)

        if   positiveSlop == 'positive' and negativeSlop == 'negative':
            fourInARow = True
            slope = 'both'
        elif positiveSlop == None and negativeSlop == 'negative':
            fourInARow = True
            slope = 'negative'
        elif positiveSlop == 'positive' and negativeSlop == None:
            fourInARow = True
            slope = 'positive'
        else:
            fourInARow = False
            slope = None

        return fourInARow, slope, positiveCount, negativeCount

    #make the winning moves in uppercase
    def capitalizeFourInARow(row, col, dir):
        if dir == 'vertical':
            for rowIndex in range(verticalCount):
                board[row+rowIndex][col] = board[row+rowIndex][col].upper()


        elif dir == 'horizontal':
            for colIndex in range(horizontalCount):
                board[row][col+colIndex] = board[row][col+colIndex].upper()

        elif dir == 'diagonal':
            if slope == 'positive' or slope == 'both':
                for diagIndex in range(positiveCount):
                    board[row+diagIndex][col+diagIndex] = board[row+diagIndex][col+diagIndex].upper()

            elif slope == 'negative' or slope == 'both':
                for diagIndex in range(negativeCount):
                    board[row-diagIndex][col+diagIndex] = board[row-diagIndex][col+diagIndex].upper()

    #initialize the variables
    FourInRowFlag = False
    slope = None
    verticalCount   = 0
    horizontalCount = 0
    positiveCount   = 0
    negativeCount   = 0
    for rowIndex in range(BOARD_HEIGHT):
        for colIndex in range(BOARD_WIDTH):
            if board[rowIndex][colIndex] != ' ':
                # check for a vertical match starts at (rowIndex, colIndex)
                fourInARow, verticalCount = verticalCheck(rowIndex, colIndex)
                if fourInARow:
                    capitalizeFourInARow(rowIndex, colIndex, 'vertical')
                    FourInRowFlag = True

                fourInARow, horizontalCount = horizontalCheck(rowIndex, colIndex)
                # check for horizontal match starts at (rowIndex, colIndex)
                if fourInARow:
                    capitalizeFourInARow(rowIndex, colIndex, 'horizontal')
                    FourInRowFlag = True

                # check for diagonal match starts at (rowIndex, colIndex)
                # also, get the slope of the four if there is one
                fourInARow, slope , positiveCount, negativeCount = diagonalCheck(rowIndex, colIndex)
                if fourInARow:
                    capitalizeFourInARow(rowIndex, colIndex, 'diagonal')
                    FourInRowFlag = True

    return FourInRowFlag

#gets number of the empty valid locations in the board
def getEmptyLocations(board):
    emptyLocations = 0
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            if board[row][col] == ' ':
                emptyLocations += 1
    return emptyLocations

def printBoard(Board):
    #clear console/terminal screen
    os.system('cls' if os.name == 'nt' else 'clear')
    emptyLocations = 42 - getEmptyLocations(Board) #get empty locations
    print('')
    print(YELLOW + '         ROUND #' + str(emptyLocations) + WHITE, end=" ")   #print round number
    print('')
    print('')
    print("\t      1   2   3   4   5   6   7 ")
    print("\t      -   -   -   -   -   -   - ")

    for i in range(0, BOARD_HEIGHT, 1):
        print(WHITE+"\t",i+1,' ',end="")
        for j in range(BOARD_WIDTH):
            if str(Board[i][j]) == 'x':
                print("| " + BLUE + str(Board[i][j]) +WHITE, end=" ")   #print colored 'x'
            elif str(Board[i][j]) == 'o':
                print("| " + RED + str(Board[i][j]) +WHITE, end=" ")   #print colored 'o'
            elif str(Board[i][j]) == 'X':
                print("| " + BLUE_BG + str(Board[i][j]) +WHITE, end=" ")   #print colored 'X'
            elif str(Board[i][j]) == 'O':
                print("| " + RED_BG + str(Board[i][j]) +WHITE, end=" ")   #print colored 'O'
            else:
                print("| " + str(Board[i][j]), end=" ")

        print("|")
    print('')
