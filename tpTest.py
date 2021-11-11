import random
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
                    visited.add((newRow, newCol))
                    result = self.dfsMazeHelper(newRow, newCol, visited)
                    if result != None:
                        return result
            return None

'''
class Cell():
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __repr__(self):
        return f'Cell({self.row}, {self.col})'

#2DList
def makeBoard(rows, cols):
    board = [[None]*cols for _ in range(rows)]
    
    for row in range(rows):
        for col in range(cols):
            board[row][col] = Cell(row, col)
'''


# #Dictionary
# def generalMaze(rows, cols):
#     maze = Graph()
#     for row in range(rows):
#         for col in range(cols):
#             maze.table[(row, col)] = dict()
#     return maze

# def isLegalMove(maze, row, col, visited):
#     numRows = 10
#     numCols = 10
#     if 0 <= row < numRows and 0 <= col < numCols:
#         if (row, col) not in visited:
#             return True
#     return False

# def dfsMaze(rows, cols):
#     maze = generalMaze(rows, cols)
#     return dfsMazeHelper(maze, 0, 0, visited=set())

# def dfsMazeHelper(maze, row, col, visited):
#     if len(visited) == 10*10:
#         return maze
#     else:
#         moves = [(0,1), (0,-1), (1, 0), (-1, 0)]
#         random.shuffle(moves)
#         for move in moves:
#             drow, dcol = move
#             newRow = row + drow
#             newCol = col + dcol
#             if isLegalMove(maze, newRow, newCol, visited):
#                 maze.addEdge((row, col), (newRow, newCol))
#                 visited.add((newRow, newCol))
#                 result = dfsMazeHelper(maze, newRow, newCol, visited)
#                 if result != None:
#                     return result
#         return None

def main():
    rows = cols = 10
    maze = Maze()
    maze.dfsMaze(rows, cols)
    print(maze.table)
    print()
    print(maze.getPath((0,0),(9,9)))

main()

    

