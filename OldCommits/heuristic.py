BOARD_WIDTH  = 7
BOARD_HEIGHT = 6 
AI_PLAYER    = 'o'
HUMAN_PLAYER = 'x'

def heuristicValue(board, player):
    """ Simple heuristic to evaluate board configurations
        Heuristic is (num of 4-in-a-rows)*99999 + (num of 3-in-a-rows)*100 + 
        (num of 2-in-a-rows)*10 - (num of opponent 4-in-a-rows)*99999 - (num of opponent
        3-in-a-rows)*100 - (num of opponent 2-in-a-rows)*10
    """
    if player == HUMAN_PLAYER: o_color = AI_PLAYER
    else: o_color = HUMAN_PLAYER

    my_fours   = checkSequence(board, player, 4)
    my_threes  = checkSequence(board, player, 3)
    my_twos    = checkSequence(board, player, 2)
    opp_fours  = checkSequence(board, o_color, 4)
    opp_threes = checkSequence(board, o_color, 3)
    opp_twos   = checkSequence(board, o_color, 2)

    if opp_fours > 0:
        return -100000
    else:
        return my_fours*100000 + my_threes*100 + my_twos*10 - opp_fours*100000 - opp_threes*100 - opp_twos*10
        
def checkSequence(board, player, length):

    def verticalSeq(row, col):
        consecutiveCount = 0
        for i in range(row, 6):
            if board[i][col] == board[row][col]:
                consecutiveCount += 1
            else:
                break
        if consecutiveCount >= length:
            return 1
        else:
            return 0

    def horizontalSeq(row, col):
        consecutiveCount = 0
        for j in range(col, 7):
            if board[row][j] == board[row][col]:
                consecutiveCount += 1
            else:
                break
        if consecutiveCount >= length:
            return 1
        else:
            return 0

    def diagonalSeq(row, col):
        total = 0
        # check for diagonals with positive slope
        consecutiveCount = 0
        j = col
        for i in range(row, 6):
            if j > 6:
                break
            elif board[i][j] == board[row][col]:
                consecutiveCount += 1
            else:
                break
            j += 1 # increment column when row is incremented
        if consecutiveCount >= length:
            total += 1

        # check for diagonals with negative slope
        consecutiveCount = 0
        j = col
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif board[i][j] == board[row][col]:
                consecutiveCount += 1
            else:
                break
            j += 1 # increment column when row is incremented
        if consecutiveCount >= length:
            total += 1

        return total

    count = 0
    # for each piece in the board...
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            # ...that is of the player we're looking for...
            if board[row][col] == player:
                # check if a vertical streak starts at (i, j)
                count += verticalSeq(row, col)
                
                # check if a horizontal four-in-a-row starts at (i, j)
                count += horizontalSeq(row, col)
                
                # check if a diagonal (either way) four-in-a-row starts at (i, j)
                count += diagonalSeq(row, col)
    # return the sum of streaks of length 'streak'
    return count
