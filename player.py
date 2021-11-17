import math

class Player():
    def __init__(self, app):
        #This seems weird
        self.app = app
        x0, x1, y0, y1 = app.maze.getCellBounds(0, 0)
        cx, cy = (x1 + x0) / 2, (y1 + y0) / 2
        self.location = (cx, cy)
        self.angle = 0
        self.distance = 5
        self.dangle = 0.2
        self.dx = self.distance * math.cos(self.angle)
        self.dy = self.distance * math.sin(self.angle)

    def checkLocation(self):
        cx, cy = self.location
        gridWidth  = self.app.width - 2*self.app.margin
        gridHeight = self.app.height - 2*self.app.margin
        cellWidth = gridWidth / self.app.maze.cols
        cellHeight = gridHeight / self.app.maze.rows
        col = (cx - self.app.margin - self.app.cellMargin)/(cellWidth)
        row = (cy - self.app.margin - self.app.cellMargin)/(cellHeight)
        return int(row), int(col)
    
    #Moving the player
    def moveWithKeys(self, event):
        #Moving
        if event.key == 'Up':
            self.movePlayer(1)
        elif event.key == 'Down':
            self.movePlayer(-1)
        
        #Turning
        elif event.key == 'Left':
            self.angle -= self.dangle
            if self.angle < 0:
                self.angle += 2 * math.pi
            self.dx = self.distance * math.cos(self.angle)
            self.dy = self.distance * math.sin(self.angle)
        
        elif event.key == 'Right':
            self.angle += self.dangle
            if self.angle < 0:
                self.angle += 2 * math.pi
            self.dx = self.distance * math.cos(self.angle)
            self.dy = self.distance * math.sin(self.angle)
    
    def movePlayer(self, direction):
        cx, cy = self.location
        cx += self.dx * direction
        cy += self.dy * direction
        self.location = (cx, cy)

    #Drawing the player
    def drawPlayer(self, canvas):
        cx, cy = self.location
        r = 5
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill = 'red', outline = 'red')
        canvas.create_line(cx, cy, cx+self.dx, cy + self.dy, fill = 'red', width = 3)
    
    def render(self, canvas):
        self.drawPlayer(canvas)

