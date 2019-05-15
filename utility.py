BOARD_WIDTH  = 7
BOARD_HEIGHT = 6 
AI_PLAYER    = 'o'
HUMAN_PLAYER = 'x'

def countSequence(board, player, length):
    """ Given the board state , the current player and the length of Sequence you want to count
        Return the count of Sequences that have the give length
    """
    def verticalSeq(row, col):
        """Return 1 if it found a vertical sequence with the required length 
        """
        count = 0
        for rowIndex in range(row, BOARD_HEIGHT):
            if board[rowIndex][col] == board[row][col]:
                count += 1
            else:
                break
        if count >= length:
            return 1
        else:
            return 0

    def horizontalSeq(row, col):
        """Return 1 if it found a horizontal sequence with the required length 
        """
        count = 0
        for colIndex in range(col, BOARD_WIDTH):
            if board[row][colIndex] == board[row][col]:
                count += 1
            else:
                break
        if count >= length:
            return 1
        else:
            return 0

    def negDiagonalSeq(row, col):
        """Return 1 if it found a negative diagonal sequence with the required length 
        """
        count = 0
        colIndex = col
        for rowIndex in range(row, -1, -1):
            if colIndex > BOARD_HEIGHT:
                break
            elif board[rowIndex][colIndex] == board[row][col]:
                count += 1
            else:
                break
            colIndex += 1 # increment column when row is incremented
        if count >= length:
            return 1
        else:
            return 0

    def posDiagonalSeq(row, col):
        """Return 1 if it found a positive diagonal sequence with the required length 
        """
        count = 0
        colIndex = col
        for rowIndex in range(row, BOARD_HEIGHT):
            if colIndex > BOARD_HEIGHT:
                break
            elif board[rowIndex][colIndex] == board[row][col]:
                count += 1
            else:
                break
            colIndex += 1 # increment column when row incremented
        if count >= length:
            return 1
        else:
            return 0

    totalCount = 0
    # for each piece in the board...
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            # ...that is of the player we're looking for...
            if board[row][col] == player:
                # check if a vertical streak starts at (row, col)
                totalCount += verticalSeq(row, col)
                # check if a horizontal four-in-a-row starts at (row, col)
                totalCount += horizontalSeq(row, col)
                # check if a diagonal (both +ve and -ve slopes) four-in-a-row starts at (row, col)
                totalCount += (posDiagonalSeq(row, col) + negDiagonalSeq(row, col))
    # return the sum of sequences of length 'length'
    return totalCount

def utilityValue(board, player):
    """ A utility fucntion to evaluate the state of the board and report it to the calling function,
        utility value is defined as the  score of the player who calles the function - score of opponent player,
        The score of any player is the sum of each sequence found for this player scalled by large factor for
        sequences with higher lengths.
    """
    if player == HUMAN_PLAYER: opponent = AI_PLAYER
    else: opponent = HUMAN_PLAYER

    playerfours    = countSequence(board, player, 4)
    playerthrees   = countSequence(board, player, 3)
    playertwos     = countSequence(board, player, 2)
    playerScore    = playerfours*99999 + playerthrees*999 + playertwos*99

    opponentfours  = countSequence(board, opponent, 4)
    opponentthrees = countSequence(board, opponent, 3)
    opponenttwos   = countSequence(board, opponent, 2)
    opponentScore  = opponentfours*99999 + opponentthrees*999 + opponenttwos*99

    if opponentfours > 0:
        #This means that the current player lost the game 
        #So return the biggest negative value => -infinity 
        return float('-inf')
    else:
        #Return the playerScore minus the opponentScore
        return playerScore - opponentScore


def gameIsOver(board):
    """Check if there is a winner in the current state of the board
    """
    if countSequence(board, HUMAN_PLAYER, 4) >= 1:
        return True
    elif countSequence(board, AI_PLAYER, 4) >= 1:
        return True
    else:
        return False
