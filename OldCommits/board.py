import os
import math
import random
from copy import deepcopy
from utility import *


def initializeBoard():
    Board = []
    for i in range(BOARD_HEIGHT):
        Board.append([])
        for j in range(BOARD_WIDTH):
            Board[i].append(' ')
    return Board

def isColumnValid(Board, Col):
    #Check if the column is valid to make the move or not
    if Board[0][Col] == ' ':
        return True
    return False
    
def isRangeValid(row, col):
    #Check if  the processed row and col are in range of Board width and height
    if row >= 0 and col >= 0 and row < BOARD_HEIGHT and col < BOARD_WIDTH:
        return True
    return False 

def getValidMoves(Board):
    Columns = []
    for Col in range(BOARD_WIDTH):
        if isColumnValid(Board, Col):
            Columns.append(Col)
    return Columns

def makeMove(board, col, player):
    """ Change the board state by placing the player move in the selected 'col'
        Returns a copy of the board after making the required move, the row and col where the move played
    """
    #deepcopy is used to take acopy of current board and not affecting the original one 
    tempBoard = deepcopy(board)
    for row in range(5,-1,-1):
        if tempBoard[row][col] == ' ':
            tempBoard[row][col] = player
            return tempBoard, row, col   


def isValidMove(col, board):
    """ Boolean function to check if a move  is valid to make or not
    """
    for row in range(BOARD_HEIGHT):
        if board[row][col] == ' ':
            return True
    return False

def isBoardFilled(board):
    #Check the first row and Selected colmun if it filled or not
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            if board[row][col]==' ': return False
    return True

def findFours(board):

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

    def capitalizeFourInARow(row, col, dir):
        """ This function enunciates four-in-a-rows by capitalizing
            the character for those pieces on the board
        """
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


    FourInRowFlag = False
    slope = None
    verticalCount   = 0
    horizontalCount = 0
    positiveCount   = 0
    negativeCount   = 0
    for rowIndex in range(BOARD_HEIGHT):
        for colIndex in range(BOARD_WIDTH):
            if board[rowIndex][colIndex] != ' ':
                # check if a vertical four-in-a-row starts at (rowIndex, colIndex)
                fourInARow, verticalCount = verticalCheck(rowIndex, colIndex)
                if fourInARow:
                    capitalizeFourInARow(rowIndex, colIndex, 'vertical')
                    FourInRowFlag = True

                fourInARow, horizontalCount = horizontalCheck(rowIndex, colIndex)
                # check if a horizontal four-in-a-row starts at (rowIndex, colIndex)
                if fourInARow:
                    capitalizeFourInARow(rowIndex, colIndex, 'horizontal')
                    FourInRowFlag = True

                # check if a diagonal (either way) four-in-a-row starts at (rowIndex, colIndex)
                # also, get the slope of the four if there is one
                fourInARow, slope , positiveCount, negativeCount = diagonalCheck(rowIndex, colIndex)
                if fourInARow:
                    capitalizeFourInARow(rowIndex, colIndex, 'diagonal')
                    FourInRowFlag = True

    return FourInRowFlag 


def getEmptyLocations(board):
    emptyLocations = 0
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            if board[row][col] == ' ':
                emptyLocations += 1
    return emptyLocations

def printBoard(Board):
    #clear console/terminal screen
    #os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )
    os.system('cls' if os.name == 'nt' else 'clear')
    emptyLocations = 42 - getEmptyLocations(Board)
    print('')
    print('\033[1;33;40m' + '         ROUND #' + str(emptyLocations) + '\033[1;37;40m', end=" ")
    print('')
    print('')
    print("\t      1   2   3   4   5   6   7 ")
    print("\t      -   -   -   -   -   -   - ") 
    for i in range(0, BOARD_HEIGHT, 1):
        print('\033[1;37;40m'+"\t",i+1,' ',end="")        
        for j in range(BOARD_WIDTH):
            if str(Board[i][j]) == 'x':
                print("| " + '\033[1;34;40m' + str(Board[i][j]) +'\033[1;37;40m', end=" ")
            elif str(Board[i][j]) == 'o':
                print("| " + '\033[1;31;40m' + str(Board[i][j]) +'\033[1;37;40m', end=" ")
            elif str(Board[i][j]) == 'X':
                print("| " + '\033[0;34;47m' + str(Board[i][j]) +'\033[1;37;40m', end=" ")
            elif str(Board[i][j]) == 'O':
                print("| " + '\033[0;31;47m' + str(Board[i][j]) +'\033[1;37;40m', end=" ")
            else:
                print("| " + str(Board[i][j]), end=" ")

        print("|")
    print('')