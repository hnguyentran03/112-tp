import math

#HELPERS
def almostEqual(d1, d2):
    epsilon = 10**-10
    return (abs(d2 - d1) < epsilon)

def normalize(row, col):
    if row % 2 == 1: row -= 1
    if col %2 == 1: col -= 1

    return row//2, col//2


class Sprite():
    def __init__(self, app, type, location):
        self.app = app
        self.type = type
        self.location = location
        # self.texture = texture
        # self.state = state

class Enemy():
    def __init__(self, app, location):
        self.app = app
        self.location = location
    
        #Gets the current cell the player is in
    def checkLocation(self, cx, cy):
        row = cy/self.app.cellHeight
        
        #Calculates the row and col (because of precision errors)
        if almostEqual(row, math.ceil(row)): row = math.ceil(row)
        else: row = math.floor(row)

        col = cx/self.app.cellWidth
        if almostEqual(col, math.ceil(col)): col = math.ceil(col)
        else: col = math.floor(col)

        return row, col
    
    def move(self):
        pass

    def getPath(self):
        px, py = self.app.player.location
        cx, cy = self.location

        prow, pcol = self.app.player.checkLocation(px, py)
        crow, ccol = self.checkLocation(cx, cy)

        prow, pcol = normalize(prow, pcol) 
        crow, ccol = normalize(crow, ccol)

        path = self.app.mazeGen.getPath((crow, ccol), (prow, pcol))
        print(path)

    def drawEnemy(self, canvas):
        cx, cy = self.location
        r = self.app.cellHeight/10
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill = 'purple', outline = 'purple')
    
    def render(self, canvas):
        self.drawEnemy(canvas)