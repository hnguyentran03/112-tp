from cmu_112_graphics import *
import random

def appStarted(app):
    app.cols = 40
    app.rows = 40
    app.board = [[None]*app.cols for _ in range(app.rows)]
    pass

def keyPressed(app, event):
    pass

def timerFiredd(app):
    pass

def redrawAll(app, canvas):
    pass

###############################################################################
#                                                                             #
#                        Helper Functions                                     #
#                                                                             #
###############################################################################
def print2dList(a):
    if (a == []): print([]); return
    rows, cols = len(a), len(a[0])
    colWidths = [0] * cols
    for col in range(cols):
        colWidths[col] = max([len(str(a[row][col])) for row in range(rows)])
    print('[')
    for row in range(rows):
        print(' [ ', end='')
        for col in range(cols):
            if (col > 0): print(', ', end='')
            print(str(a[row][col]).ljust(colWidths[col]), end='')
        print(' ]')
    print(']')


def repr2dList(L):
    if (L == []): return '[]'
    output = [ ]
    rows = len(L)
    cols = max([len(L[row]) for row in range(rows)])
    M = [['']*cols for row in range(rows)]
    for row in range(rows):
        for col in range(len(L[row])):
            M[row][col] = repr(L[row][col])
    colWidths = [0] * cols
    for col in range(cols):
        colWidths[col] = max([len(M[row][col]) for row in range(rows)])
    output.append('[\n')
    for row in range(rows):
        output.append(' [ ')
        for col in range(cols):
            if (col > 0):
                output.append(', ' if col < len(L[row]) else '  ')
            output.append(M[row][col].rjust(colWidths[col]))
        output.append((' ],' if row < rows-1 else ' ]') + '\n')
    output.append(']')
    return ''.join(output)

def print2dList(L):
    print(repr2dList(L))






#https://en.wikipedia.org/wiki/Maze_generation_algorithm
def isLegalMove(board, row, col, visited):
    numRows = len(board)
    numCols = len(board[0])
    if 0 <= row < numRows and 0 <= col < numCols:
        if (row, col) not in visited:
            return True
    return False

def dfsMazeHelper(board, row, col, visited):
    if len(visited) == len(board)*len(board[0]):
        return board
    else:
        moves = [(0,1), (0,-1), (1, 0), (-1, 0)]
        random.shuffle(moves)
        for move in moves:
            drow, dcol = move
            newRow = row + drow
            newCol = col + dcol
            if isLegalMove(board, newRow, newCol, visited):
                print2dList(board)
                board[newRow][newCol] = 0
                visited.add((newRow, newCol))
                repr2dList(board)
                result = dfsMazeHelper(board, newRow, newCol, visited)
                if result != None:
                    return result
        return None


def dfsMaze(board):
    board[0][0] = 0
    return dfsMazeHelper(board, 0, 0, set())


#Idea from https://en.wikipedia.org/wiki/Maze_generation_algorithm
#Add the recursion
def recursiveDivisionMaze(board, row, col, numRows, numCols, direction):
    if numRows <= 1 or numCols <= 1:
        return
    else:
        
        if direction == 'vertical': 
            wallRow = row
            wallCol = col + random.randint(0,numCols-1)

            holeRow = random.randint(0, numRows-1)
            holeCol = -1

            drow = 1
            dcol = 0

            length = numRows
        
        elif direction == 'horizontal':
            wallRow = row + random.randint(0, numRows-1)
            wallCol = col

            holeRow = -1
            holeCol = random.randint(0, numCols-1)

            drow = 0
            dcol = 1

            length = numCols

        for _ in range(length):
            if holeRow != wallRow and holeCol != wallCol:
                board[wallRow][wallCol] = 1
            wallRow += drow
            wallCol += dcol
        
        return board



        



def runCode():
    rows = cols = 5
    

    # board = [[0]*cols for _ in range(rows)]
    # board = recursiveDivisionMaze(board, 0, 0, rows, cols, 'vertical')

    board = [[1]*cols for _ in range(rows)]
    board = dfsMaze(board)
    
    print2dList(board)

runCode()