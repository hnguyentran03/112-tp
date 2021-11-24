import math

#HELPER
def almostEqual(d1, d2):
    epsilon = 10**-10
    return (abs(d2 - d1) < epsilon)

class Player():
    def __init__(self, app):
        #This seems weird
        self.app = app
        x0, x1, y0, y1 = app.mazeGen.getCellBounds2(0, 0)
        cx, cy = (x1 + x0) / 2, (y1 + y0) / 2
        self.location = (cx, cy)
        self.angle = math.pi/2
        self.step = (app.cellHeight/5)
        self.move = (self.step * math.cos(self.angle), self.step * math.sin(self.angle))


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
    
    def isIllegalPosition(self, cx, cy):
        row, col = self.checkLocation(cx, cy)

        outOfBounds = not(0 <= row < len(self.app.maze)) or not(0 <= col < len(self.app.maze))
        if  outOfBounds or self.app.maze[row][col] == 1: return True
        else: return False



    #Angle to turn taken from https://www.youtube.com/watch?v=gYRrGTC7GtA
    #Moving the player
    def moveWithKeys(self, event):
        #Moving
        if event.key == 'w':
            self.movePlayer(1, 'Up')
        elif event.key == 's':
            self.movePlayer(-1, 'Down')
        elif event.key == 'a':
            self.movePlayer(-1, 'Left')
        elif event.key == 'd':
            self.movePlayer(1, 'Right')
        
        #Turning
        if event.key == 'Left':
            self.angle -= math.pi/(3*(2**3))
            
            #Accounts for overangling
            if self.angle < 0: self.angle += 2*math.pi
            
            #Calculations from angle to movement
            dx, dy = self.move
            dx = math.cos(self.angle)
            dy = math.sin(self.angle)
            self.move = (self.step*dx, self.step*dy)
    
        elif event.key == 'Right':
            self.angle += math.pi/ (3*(2**3))
            
            #Accounts for overangling
            if self.angle > 2*math.pi:
                self.angle -= 2*math.pi
            
            #Calculations from angle to movement
            dx, dy = self.move
            dx = math.cos(self.angle)
            dy = math.sin(self.angle)
            self.move = (self.step*dx, self.step*dy)

    def movePlayer(self, direction, directionName):
        cx, cy = self.location
        dx, dy = self.move
        
        if directionName == 'Up' or directionName == 'Down':
            cx += dx * direction
            cy += dy * direction
        
        #FIX
        elif directionName == 'Left' or directionName == 'Right':
            cx += (dy * direction * -1)/2
            cy += (dx * direction)/2
        
        if not self.isIllegalPosition(cx, cy):
            self.location = (cx, cy)

    #Drawing the player
    def drawPlayer(self, canvas):
        cx, cy = self.location
        r = self.app.cellHeight/5
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill = 'red', outline = 'red')
    
    def render(self, canvas):
        self.drawPlayer(canvas)