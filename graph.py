import random
from cmu_112_graphics import *

#Idea for graph class (and some funcitons) from Graph Algorithm Mini-Lecture
class Graph():
    def __init__(self):
        self.table = {}
    
    def __repr__(self):
        return f'{self.table}'
    
    def addEdge(self, nodeA, nodeB, weight=1):
        if nodeA not in self.table:
            self.table[nodeA] = {}
        if nodeB not in self.table:
            self.table[nodeB] = {}
        self.table[nodeA][nodeB] = weight
        self.table[nodeB][nodeA] = weight
    
    def getNodes(self):
        return list(self.table)
    
    def getNeighbors(self, node):
        return set(self.table[node])
    
    #dfs
    def getPath(self, nodeA, nodeB):
        path = self.getPathHelper(nodeA, nodeB, dict())
        newPath = {}
        #ASK KIAN ABOUT WHY MY DFS HAS THE NONES IN IT
        for node in path:
            if path[node] != None:
                newPath[node] = path[node]

        return newPath

    def getPathHelper(self, nodeA, nodeB, visited):
        if nodeA == nodeB:
            return visited
        else:
            visited[nodeA] = None
            #Search neighbors
            for neighbor in self.getNeighbors(nodeA):
                if neighbor not in visited:
                    
                    visited[nodeA] = neighbor
                    result = self.getPathHelper(neighbor, nodeB, visited)
                    if result != None:
                        return result

                    #If we get nowhere, backtrack
                    visited.pop(nodeA)
            return None


'''
FROM GRAPH TO MAZE
'''
class Maze(Graph):
    def __init__(self, app):
        super().__init__()
        self.app = app
    #Checks if the move is legal or not
    def isLegalMove(self, row, col, visited):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            if (row, col) not in visited:
                return True
        return False


    #Idea for Maze Generation from https://en.wikipedia.org/wiki/Maze_generation_algorithm
    #Makes a dfs Maze
    def dfsMaze(self, rows, cols):
        self.rows = rows
        self.cols = cols
        return self.dfsMazeHelper(0, 0, visited=set())

    def dfsMazeHelper(self, row, col, visited):
        if len(visited) == self.rows*self.cols:
            return self
        else:
            #Randomized moves
            visited.add((row, col))
            moves = [(0,1), (0,-1), (1, 0), (-1, 0)]
            random.shuffle(moves)
            for move in moves:
                drow, dcol = move
                #Inherent backtracking because doesn't change row or col
                newRow = row + drow
                newCol = col + dcol
                if self.isLegalMove(newRow, newCol, visited):
                    #Makes a path between the two
                    self.addEdge((row, col), (newRow, newCol))
                    result = self.dfsMazeHelper(newRow, newCol, visited)
                    if result != None:
                        return result
            return None

    #Drawing
    def getCellBounds(self, row, col):
        #Taken from 112 Notes/Lecture (also what do we do about the app.table)
        gridWidth  = self.app.width - 2*self.app.margin
        gridHeight = self.app.height - 2*self.app.margin
        cellWidth = gridWidth / self.app.maze.cols
        cellHeight = gridHeight / self.app.maze.rows
        x0 = self.app.margin + col * cellWidth + self.app.cellMargin
        x1 = self.app.margin + (col+1) * cellWidth - self.app.cellMargin
        y0 = self.app.margin + row * cellHeight + self.app.cellMargin
        y1 = self.app.margin + (row+1) * cellHeight - self.app.cellMargin
        return x0, x1, y0, y1
                
    def drawCell(self, canvas, row, col, color = 'white'):
        x0, x1, y0, y1 = self.getCellBounds(row, col)
        canvas.create_rectangle(x0, y0, x1, y1, fill = color, outline = '')
    
    def drawEdges(self,canvas):
        for row, col in self.table:
            for neighborRow, neighborCol in self.getNeighbors((row, col)):
                #Gets the edges of both cell and neighbor and make a rectangle to fill in
                _, x1, _, y1 = self.getCellBounds(row, col)
                nx0, _, ny0, _ = self.getCellBounds(neighborRow, neighborCol)
                canvas.create_rectangle(nx0, ny0, x1, y1, fill = 'white', outline = '')

    def drawMaze(self, canvas):
        for row, col in self.table:
            self.drawCell(canvas, row, col)
    
    def render(self, canvas):
        self.drawMaze(canvas)
        self.drawEdges(canvas)











    def convertTo2DList(self):
        maze = [[None]*self.cols for _ in range(self.rows)]
        for row, col in self.table:
            maze[row][col] = 1
        for cell in self.table:
            row, col = cell
            neighbors = self.getNeighbors(cell)
            for neighbor in neighbors:
                nrow, ncol = neighbor
                xrow = (nrow + row)/2
                xcol = (ncol + col)/2    
        print2dList(maze)

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





