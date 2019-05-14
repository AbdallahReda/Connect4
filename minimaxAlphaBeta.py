from board import *
from random import shuffle

def MiniMaxAlphaBeta(board, depth, player):
    # get array of possible moves 
    validMoves = getValidMoves(board)
    shuffle(validMoves)
    bestMove  = validMoves[0]
    bestScore = float("-inf")

    # initial alpha & beta values for alpha-beta pruning
    alpha = float("-inf")
    beta = float("inf")

    if player == AI_PLAYER: opponent = HUMAN_PLAYER
    else: opponent = AI_PLAYER
  
    # go through all of those boards
    for move in validMoves:
        # create new board from move
        tempBoard = makeMove(board, move, player)[0]
        # call min on that new board
        boardScore = minimizeBeta(tempBoard, depth - 1, alpha, beta, player, opponent)
        if boardScore > bestScore:
            bestScore = boardScore
            bestMove = move
    return bestMove

def minimizeBeta(board, depth, a, b, player, opponent):
    validMoves = []
    for col in range(7):
        # if column col is a legal move...
        if isValidMove(col, board):
            # make the move in column col for curr_player
            temp = makeMove(board, col, player)[2]
            validMoves.append(temp)

    # check to see if game over
    if depth == 0 or len(validMoves) == 0 or gameIsOver(board):
        return utilityValue(board, player)
    
    validMoves = getValidMoves(board) 
    beta = b
    
    # if end of tree evaluate scores
    for move in validMoves:
        boardScore = float("inf")
        # else continue down tree as long as ab conditions met
        if a < beta:
            tempBoard = makeMove(board, move, opponent)[0]
            boardScore = maximizeAlpha(tempBoard, depth - 1, a, beta, player, opponent)

        if boardScore < beta:
            beta = boardScore
    return beta

def maximizeAlpha(board, depth, a, b, player, opponent):
    validMoves = []
    for col in range(7):
        # if column col is a legal move...
        if isValidMove(col, board):
            # make the move in column col for curr_player
            temp = makeMove(board, col, player)[2]
            validMoves.append(temp)
    # check to see if game over
    if depth == 0 or len(validMoves) == 0 or gameIsOver(board):
        return utilityValue(board, player)

    alpha = a        
    # if end of tree, evaluate scores
    for move in validMoves:
        boardScore = float("-inf")
        if alpha < b:
            tempBoard = makeMove(board, move, player)[0]
            boardScore = minimizeBeta(tempBoard, depth - 1, alpha, b, player, opponent)

        if boardScore > alpha:
            alpha = boardScore
    return alpha