import math

class Player:
    def __init__(self, startX, startY, step=5, angle=0):
        self.cx = startX
        self.cy = startY
        self.angle = angle
        self.step = step
        self.dx, self.dy = (self.step * math.cos(self.angle), self.step*math.sin(self.angle))
    
    def getRow(self, cellHeight):
        return math.floor(self.cy / cellHeight)
    
    def getCol(self, cellWidth):
        return math.floor(self.cx / cellWidth)
    
    
        