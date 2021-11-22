import math

class Player():
    def __init__(self, app):
        #This seems weird
        self.app = app
        x0, x1, y0, y1 = app.mazeGen.getCellBounds2(0, 0)
        cx, cy = (x1 + x0) / 2, (y1 + y0) / 2
        self.location = (cx, cy)
        self.angle = math.pi/2
        self.step = (app.cellHeight/5)
        if self.step > 0:
            self.turn = int(self.step)-1
        else:
            self.turn = int(self.step)
        self.move = (self.step * math.cos(self.angle), self.step * math.sin(self.angle))


    #Gets the current cell the player is in
    def checkLocation(self):
        cx, cy = self.location
        gridWidth  = self.app.width - 2*self.app.margin
        gridHeight = self.app.height - 2*self.app.margin
        cellWidth = gridWidth / self.app.mazeGen.cols
        cellHeight = gridHeight / self.app.mazeGen.rows
        col = (cx - self.app.margin - self.app.cellMargin)/(cellWidth)
        row = (cy - self.app.margin - self.app.cellMargin)/(cellHeight)
        return int(row), int(col)
    
    def isLegalPosition(self, cx, cy):
        # row, col = self.checkLocation()
        # #Cell legality check
        # x0, x1, y0, y1 = self.app.maze.getCellBounds(row, col)
        # outOfCellBounds = cx < x0 or cx > x1 or cx < y0 or cx > y1
        
        # if not outOfCellBounds:
        #     return True
        
        # for neighborRow, neighborCol in self.app.maze.getNeighbors((row, col)):
        #         nx0, _, ny0, _ = self.app.maze.getCellBounds(neighborRow, neighborCol)
                
        #         outOfEdgeBounds = cx < x1 or cx > nx0 or cy < y1 or cy > ny0
        #         if not outOfEdgeBounds:
        #             return True
        
        # return False
        return True


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
            self.angle -= math.pi/(3*(2**4))
            
            #Accounts for overangling
            if self.angle < 0:
                self.angle += 2*math.pi
            
            #Calculations from angle to movement
            dx, dy = self.move
            dx = math.cos(self.angle)
            dy = math.sin(self.angle)
            self.move = (self.step*dx, self.step*dy)
    
        elif event.key == 'Right':
            self.angle += math.pi/ (3*(2**4))
            
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
            cx += dx * direction * math.cos(math.pi/2)
            cy += dx * direction * math.sin(math.pi/2)
        
        self.location = (cx, cy)

    #Drawing the player
    def drawPlayer(self, canvas):
        cx, cy = self.location
        r = self.app.cellHeight/10
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill = 'red', outline = 'red')
    
    def render(self, canvas):
        self.drawPlayer(canvas)

