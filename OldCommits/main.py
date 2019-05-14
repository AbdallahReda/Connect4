from minimaxAlphaBeta import *

dir_path = os.path.dirname(os.path.realpath(__file__))

def saveParser(board, filename):
    def parseRow(row):
        return str(row).strip(']').strip('[').replace("' '",'.').replace(',','').replace("'",'')

    with open(dir_path +"\\" +  filename + '.txt', 'w') as f:
        for row in board:
            f.write(parseRow(row)+'\n')

    return True

def saveBoard(board):
    saveFile = True if input('DO YOU WANT TO SAVE BOARD(y/n)? ') == 'y' else False
    if saveFile:
        filename = input('ENTER FILE NAME: ')
        saveParser(board,filename)

def loadParser(filename):
    def parseBoard(board):
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                if board[row][col]=='.':
                    board[row][col]=' '
        return board

    f = open(dir_path +"\\" +  filename + '.txt')
    result = [[c.replace(' ',' ').lower()for c in l.strip('\n').split(' ')] for l in f.readlines()]
    board = parseBoard(result)
    return board

def loadBoard():
    loadFile = True if input('DO YOU WANT TO LOAD A BOARD(y/n)? ') == 'y' else False
    if loadFile:
        filename = input('ENTER FILE NAME: ')
        board = loadParser(filename)
        return board, loadFile
    else:
        return None, loadFile


def playerTurn(board):
    Col = input("Choose a Column between 1 and 7: ")
    if not(Col.isdigit()):
        print("Input must be integer!")
        return playerTurn(board)

    playerMove = int(Col) - 1

    if playerMove < 0 or playerMove > 6:
        print("Column must be between 1 and 7!")
        return playerTurn(board)

    if not(isColumnValid(board, playerMove)):
        print("The Column you select is full!")
        return playerTurn(board)


    board = makeMove(board, playerMove, HUMAN_PLAYER)[0]
    playerFourInRow  = findFours(board)
    return board, playerFourInRow

def playerWins(board):
    printBoard(board)
    print('                    '+'\033[0;34;40m'+"HUMAN WINS !!\n" +'\033[1;37;40m')
    playagain = True if input('\033[1;33;40m'+'DO YOU WANT TO PLAY AGAIN(y/n)?'+'\033[1;37;40m') == 'y' else False
    saveBoard(board)
    if playagain:
        mainFucntion()
    return 0

def aiTurn(board,depth):
    aiMove  = MiniMaxAlphaBeta(board, depth, AI_PLAYER)
    board = makeMove(board, aiMove, AI_PLAYER)[0]
    aiFourInRow  = findFours(board)

    return  board, aiFourInRow

def aiWins(board):
    printBoard(board)
    print('                     '+'\033[0;31;40m'+"AI WINS !!!!\n" +'\033[1;37;40m')
    playagain = True if input('\033[1;33;40m'+'DO YOU WANT TO PLAY AGAIN(y/n)?'+'\033[1;37;40m') == 'y' else False
    saveBoard(board)
    if playagain:
        mainFucntion()
    return 0


def whomTurn(board):
    playerCount = 0
    aiCount = 0
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            if board[row][col] == 'o' or board[row][col] == 'O':
                aiCount +=1
            elif board[row][col] == 'x' or board[row][col] == 'X':
                playerCount +=1
    if playerCount > aiCount:
        return False
    elif playerCount == aiCount:
        return True
    #elif playerCount <




def mainFucntion():
    #board = initializeBoard()
    board, loadFlag = loadBoard()
    if board == None:
        board = initializeBoard()
    printBoard(board)
    
    depth = int(input('ENTER DIFFICULTY(1-7): '),10)
    whileCondition = 1
    whomStart = True if input('DO YOU WANT TO START(y/n)? ') == 'y' else False
    if board == None:
        board = initializeBoard()

    while(whileCondition):
        if isBoardFilled(board) : 
            print("GAME OVER")
            break

        if whomStart:
            #Human
            board, playerFourInRow = playerTurn(board)
            if playerFourInRow:
                whileCondition = playerWins(board)
                if whileCondition ==0:
                    break

            #AI
            board, aiFourInRow = aiTurn(board,depth)
            if aiFourInRow:
                whileCondition = aiWins(board)
                if whileCondition ==0:
                    break
            printBoard(board)

        else:
            #AI
            board, aiFourInRow = aiTurn(board,depth)
            if aiFourInRow:
                whileCondition = aiWins(board)
                if whileCondition ==0:    
                    break
            printBoard(board)
            #Human
            board, playerFourInRow = playerTurn(board)
            if playerFourInRow:
                whileCondition = playerWins(board)
                
                if whileCondition ==0:                    
                    break

            printBoard(board)




mainFucntion()


'''
    if Col == 's':
        filename = input('Enter FileName to save:')
        saveBoard(Board, 'testfile')
        return human(Board)

    if Col == 'l':
        filename = input('Enter FileName to load:')
        Board = loadBoard(filename)
        emptyLocations = 42 - getEmptyLocations(Board)
        if emptyLocations %2 == 1:
            return human(Board)



            def mainFucntion():
    board = initializeBoard()
    printBoard(board)
    depth = int(input("Enter Diff: "),10)

    while(1):
        if isBoardFilled(board) :
            print("GAME OVER")
            break
 
        HumanTurnCol = playerTurn(board)
        HumanMove    = 'x'
        board, _ , _ = makeMove(board, HumanTurnCol, HumanMove)
        FourInRow  = findFours(board)
        if FourInRow:
            printBoard(board)
            print('                    '+'\033[0;34;47m'+"HUMAN WINS !!\n" +'\033[1;37;40m')
            playagain = True if input('\033[1;33;40m'+'DO YOU WANT TO PLAY AGAIN(y/n)?'+'\033[1;37;40m') == 'y' else False
            if playagain:
                mainFucntion()
            break

        #AI
        board, aiFourInRow = aiTurn(board,depth)
        if aiFourInRow:
            aiWins(board)

        printBoard(board)
'''