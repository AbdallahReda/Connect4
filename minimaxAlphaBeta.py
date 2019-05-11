from connect4board import *

def MiniMaxAlphaBeta(board, depth, player):
    # get array of possible moves 
    validMoves = getValidMoves(board)
    #bestMove = validMoves[randint(0,BOARD_WIDTH-1)]
    bestMove  = validMoves[0]
    bestScore = float("-inf")

    # initial alpha & beta values for alpha-beta pruning
    alpha = float("-inf")
    beta = float("inf")

    if player == AI_PLAYER:
        opponent = HUMAN_PLAYER
    else:
        opponent = AI_PLAYER

  
    # go through all of those boards
    for move in validMoves:
    
        # create new board from move
        tempBoard = makeMove(board, move, player)[0]

        # call min on that new board
        boardScore = minAlphaBeta(tempBoard, depth - 1, alpha, beta, player, opponent)
        if boardScore > bestScore:
            bestScore = boardScore
            bestMove = move
    #print("Alpha: ",alpha,"Beta: ",beta)
    return bestMove


def minAlphaBeta(board, depth, a, b, player, opponent):
    validMoves = []
    for i in range(7):
        # if column i is a legal move...
        if isLegalMove(i, board):
            # make the move in column i for curr_player
            temp = makeMove(board, i, player)[2]
            validMoves.append(temp)

    # check to see if game over
    if depth == 0 or len(validMoves) == 0 or gameIsOver(board):
        return heuristicValue(board, player)
    
    else:
        validMoves = getValidMoves(board) 
        beta = b
        
        #printBoard(board,depth)
        # if end of tree evaluate scores
        for move in validMoves:
            boardScore = float("inf")
            # else continue down tree as long as ab conditions met
            if a < beta:
                tempBoard = makeMove(board, move, opponent)[0]
                boardScore = maxAlphaBeta(tempBoard, depth - 1, a, beta, player, opponent)

            if boardScore < beta:
                beta = boardScore
        #print('betaMin: ',beta)
        return beta


def maxAlphaBeta(board, depth, a, b, player, opponent):
    validMoves = []
    for i in range(7):
        # if column i is a legal move...
        if isLegalMove(i, board):
            # make the move in column i for curr_player
            temp = makeMove(board, i, player)[2]
            validMoves.append(temp)

    # check to see if game over
    if depth == 0 or len(validMoves) == 0 or gameIsOver(board):
        return heuristicValue(board, player)
    
    else:
        alpha = a        
        # if end of tree, evaluate scores
        for move in validMoves:
            boardScore = float("-inf")
            if alpha < b:
                tempBoard = makeMove(board, move, player)[0]
                boardScore = minAlphaBeta(tempBoard, depth - 1, alpha, b, player, opponent)

            if boardScore > alpha:
                alpha = boardScore
        return alpha