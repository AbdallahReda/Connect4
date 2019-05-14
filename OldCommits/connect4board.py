import os
import math
import random
from copy import deepcopy
from heuristic import *

BOARD_WIDTH  = 7
BOARD_HEIGHT = 6 
DIFFICULLTY  = 12
AI_PLAYER    = 'o'
HUMAN_PLAYER = 'x' 

def initializeBoard(Board):
    for i in range(6):
        Board.append([])
        for j in range(7):
            Board[i].append(' ')
    return Board

def printBoard(Board):
    # cross-platform clear screen
    os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )
    print('')
    print("\t      1   2   3   4   5   6   7 ")
    print("\t      -   -   -   -   -   -   - ") 
    for i in range(0, 6, 1):
        print('\033[1;37;40m'+"\t",i+1,' ',end="")        
        for j in range(7):
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

def isColumnFilled(Board, Col):
    #Check the first row and Selected colmun if it filled or not
    if Board[0][Col] == ' ':
        return False
    return True 

def isColumnValid(Board, Col):
    #Check the first row and Selected colmun if it filled or not
    if Board[0][Col] == ' ':
        return True
    
def isRangeValid(row, col):
    if row >= 0 and col >= 0 and row < 6 and col < 7:
        return True
    return False 

def getValidMoves(Board):
    Columns = []
    for Col in range(BOARD_WIDTH):
        if isColumnValid(Board, Col):
            Columns.append(Col)
    return Columns


def gameIsOver(state):
    if checkSequence(state, HUMAN_PLAYER, 4) >= 1:
        return True
    elif checkSequence(state, AI_PLAYER, 4) >= 1:
        return True
    else:
        return False

def isBoardFilled(Board):
    #Check the first row and Selected colmun if it filled or not
    for i in range(6):
        for j in range(7):
            if Board[i][j]==' ': return False
    return True

def makeMove(board, col, player):
    """ Change a state object to reflect a player, denoted by color,
        making a move at column 'column'
        
        Returns a copy of new state array with the added move
    """
    #tempBoard = [i[:] for i in board]
    tempBoard = deepcopy(board)
    for row in range(5,-1,-1):
        if tempBoard[row][col] == ' ':
            tempBoard[row][col] = player
            return tempBoard,row,col   


def isLegalMove(column, board):
    """ Boolean function to check if a move (column) is a legal move
    """
    for row in range(6):
        if board[row][column] == ' ':
            # once we find the first empty, we know it's a legal move
            return True
    # if we get here, the column is full
    return False


def findFours(board):
    winner = None

    def verticalCheck(row, col):
        fourInARow = False
        consecutiveCount = 0
        winner = None
        for rowIndex in range(row, BOARD_HEIGHT):
            if board[rowIndex][col] == board[row][col]:
                consecutiveCount += 1
            else:
                break
    
        if consecutiveCount >= 4:
            fourInARow = True
            if HUMAN_PLAYER.lower() == board[row][col].lower():
                winner = HUMAN_PLAYER
            else:
                winner = AI_PLAYER
    
        return fourInARow , winner
    
    def horizontalCheck( row, col):
        fourInARow = False
        consecutiveCount = 0
        winner = None
        for colIndex in range(col, BOARD_WIDTH):
            if board[row][colIndex].lower() == board[row][col].lower():
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= 4:
            fourInARow = True
            if HUMAN_PLAYER.lower() == board[row][col].lower():
                winner = HUMAN_PLAYER
            else:
                winner = AI_PLAYER

        return fourInARow , winner
    
    def diagonalCheck(row, col):
        fourInARow = False
        count = 0
        slope = None
        winner = None
        # check for diagonals with positive slope
        consecutiveCount = 0
        colIndex = col
        for rowIndex in range(row, BOARD_HEIGHT):
            if colIndex > BOARD_HEIGHT:
                break
            elif board[rowIndex][colIndex].lower() == board[row][col].lower():
                consecutiveCount += 1
            else:
                break
            colIndex += 1 # increment column when row is incremented
            
        if consecutiveCount >= 4:
            count += 1
            slope = 'positive'
            if HUMAN_PLAYER.lower() == board[row][col].lower():
                winner = HUMAN_PLAYER
            else:
                winner = AI_PLAYER

        # check for diagonals with negative slope
        consecutiveCount = 0
        colIndex = col
        for rowIndex in range(row, -1, -1):
            if colIndex > 6:
                break
            elif board[rowIndex][colIndex].lower() == board[row][col].lower():
                consecutiveCount += 1
            else:
                break
            colIndex += 1 # increment column when row is decremented

        if consecutiveCount >= 4:
            count += 1
            slope = 'negative'
            if HUMAN_PLAYER.lower() == board[row][col].lower():
                winner = HUMAN_PLAYER
            else:
                winner = AI_PLAYER

        if count > 0:
            fourInARow = True
        if count == 2:
            slope = 'both'
        return fourInARow, slope , winner


    magical = False
    """ Finds start i,j of four-in-a-row
        Calls highlightFours
    """
    for rowIndex in range(BOARD_HEIGHT):
        for colIndex in range(BOARD_WIDTH):
            if board[rowIndex][colIndex] != ' ':
                # check if a vertical four-in-a-row starts at (i, colIndex)
                fourInARow , winner = verticalCheck(rowIndex, colIndex)
                if fourInARow:
                    highlightFour(board, rowIndex, colIndex, 'vertical')
                    magical = True
                    
                fourInARow , winner = horizontalCheck(rowIndex, colIndex)
                # check if a horizontal four-in-a-row starts at (i, colIndex)
                if fourInARow:
                    highlightFour(board, rowIndex, colIndex, 'horizontal')
                    magical = True
                
                # check if a diagonal (either way) four-in-a-row starts at (i, colIndex)
                # also, get the slope of the four if there is one
                fourInARow, slope , winner = diagonalCheck(rowIndex, colIndex)
                if fourInARow:
                    highlightFour(board, rowIndex, colIndex, 'diagonal', slope)
                    magical = True

    return magical , winner


def highlightFour(board,row, col, direction, slope=None):
    """ This function enunciates four-in-a-rows by capitalizing
        the character for those pieces on the board
    """
    if direction == 'vertical':
        for rowIndex in range(4):
            board[row+rowIndex][col] = board[row+rowIndex][col].upper()

    
    elif direction == 'horizontal':
        for colIndex in range(4):
            board[row][col+colIndex] = board[row][col+colIndex].upper()
    
    elif direction == 'diagonal':
        if slope == 'positive' or slope == 'both':
            for diagIndex in range(4):
                board[row+diagIndex][col+diagIndex] = board[row+diagIndex][col+diagIndex].upper()
    
        elif slope == 'negative' or slope == 'both':
            for diagIndex in range(4):
                board[row-diagIndex][col+diagIndex] = board[row-diagIndex][col+diagIndex].upper()
    
    else:
        print("Error - Cannot enunciate four-of-a-kind")


def check4InARow(board):
    tempBoard = deepcopy(board)
    fourInARow , winner = findFours(tempBoard)
    return fourInARow , winner


def checkFours(Board, row, col):
    piece = Board[row][col]
    if piece == ' ':
        return False # Shouldn't happen but just as a precaution

    # Lengths of the horizontal, vertical, positive, and negative sloped chains, in that order
    lengths = [0, 0, 0, 0]
    index = 0

    # Represent movement along horizontal, vertical pos, and neg chains
    directions = [[0, 1], [1, 0], [-1, 1], [-1, -1]]

    for direction in directions:

        # Positive slope direction
        indexRow = row + direction[0]
        indexCol = col + direction[1]
        while isRangeValid(indexRow, indexCol) and Board[indexRow][indexCol] == piece:
            lengths[index] += 1
            indexRow += direction[0]
            indexCol += direction[1]

        #Negative slope direction
        indexRow = row - direction[0]
        indexCol = col - direction[1]
        while isRangeValid(indexRow, indexCol) and Board[indexRow][indexCol] == piece:
            lengths[index] += 1
            indexRow -= direction[0]
            indexCol -= direction[1]
        index +=1

    for length in lengths:
        if length >= 3: 
            return True , piece
    return False , None