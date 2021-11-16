class Player():
    def __init__(self, app):
        #This seems weird
        self.app = app
        x0, x1, y0, y1 = app.maze.getCellBounds(0, 0)
        cx, cy = (x1 + x0) / 2, (y1 + y0) / 2
        self.location = (cx, cy)

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
        if event.key == 'Up':
            self.movePlayer(self.app, 0, -5)
        elif event.key == 'Down':
            self.movePlayer(self.app, 0, 5)
        elif event.key == 'Left':
            self.movePlayer(self.app, -5, 0)
        elif event.key == 'Right':
            self.movePlayer(self.app, 5, 0)
    
    def movePlayer(self, dx, dy):
        cx, cy = self.location
        cx += dx
        cy += dy
        self.location = (cx, cy)

    #Drawing the player
    def drawPlayer(self, canvas):
        cx, cy = self.location
        x0, x1 = cx - 5, cx + 5
        y0, y1 = cy - 5, cy + 5
        canvas.create_oval(x0, y0, x1, y1, fill = 'red', outline = 'red')
    
    def render(self, canvas):
        self.drawPlayer(canvas)

