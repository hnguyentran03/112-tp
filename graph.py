import random
from cmu_112_graphics import *

#Idea for graph class (and some funcitons) from Graph Algorithm Mini-Lecture
class Graph():
    def __init__(self):
        self.table = {}
    
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
    def getCellBounds(self, app, row, col):
        #Taken from 112 Notes/Lecture (also what do we do about the app.table)
        gridWidth  = app.width - 2*app.margin
        gridHeight = app.height - 2*app.margin
        cellWidth = gridWidth / app.maze.cols
        cellHeight = gridHeight / app.maze.rows
        x0 = app.margin + col * cellWidth + app.cellMargin
        x1 = app.margin + (col+1) * cellWidth - app.cellMargin
        y0 = app.margin + row * cellHeight + app.cellMargin
        y1 = app.margin + (row+1) * cellHeight - app.cellMargin
        return x0, x1, y0, y1
                
    def drawCell(self, app, canvas, row, col, color = 'white'):
        x0, x1, y0, y1 = self.getCellBounds(app, row, col)
        canvas.create_rectangle(x0, y0, x1, y1, fill = color, outline = '')
    
    def drawEdges(self, app, canvas):
        for row, col in self.table:
            for neighborRow, neighborCol in self.table[(row, col)]:
                pathRow = (row + neighborRow) / 2
                pathCol = (col + neighborCol) / 2
                self.drawCell(app, canvas, pathRow, pathCol)

    def drawMaze(self, app, canvas):
        for row, col in self.table:
            self.drawCell(app, canvas, row, col)
    
    def render(self, app, canvas):
        self.drawMaze(app, canvas)
        self.drawEdges(app, canvas)






#TEST CODE
def main():
    rows = cols = 10
    maze = Maze()
    maze.dfsMaze(rows, cols)
    print(maze.table)
    print()
    print(maze.getPath((0,0),(9,9)))

# main()






