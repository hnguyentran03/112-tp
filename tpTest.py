import random
from cmu_112_graphics import *

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
        return self.getPathHelper(nodeA, nodeB, dict())

    def getPathHelper(self, nodeA, nodeB, visited):
        if nodeA == nodeB:
            return visited
        else:
            visited[nodeA] = None
            for neighbor in self.getNeighbors(nodeA):
                if neighbor not in visited:
                    visited[nodeA] = neighbor
                    result = self.getPathHelper(neighbor, nodeB, visited)
                    if result != None:
                        return result
            if visited[nodeA] == None:
                visited.pop(nodeA)
            return None

class Maze(Graph):
    #Checks if the move is legal or not
    def isLegalMove(self, row, col, visited):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            if (row, col) not in visited:
                return True
        return False

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


#TEST CODE
def main():
    rows = cols = 10
    maze = Maze()
    maze.dfsMaze(rows, cols)
    print(maze.table)
    print()
    print(maze.getPath((0,0),(9,9)))

# main()






