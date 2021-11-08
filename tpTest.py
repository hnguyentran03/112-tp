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
    
    def getPath(self, nodeA, nodeB):
        return self.getPathHelper(nodeA, nodeB, dict())

    #dfs search
    def getPathHelper(self, nodeA, nodeB, visited):
        if nodeA == nodeB:
            return visited
        else:
            visited[nodeA] = None
            for neighbor in self.getNeighbors(nodeA):
                if neighbor not in visited:
                    visited[nodeA] = neighbor
                    result = self.getPathHelper(nodeA, nodeB)
                    if result != None:
                        return result
            return None