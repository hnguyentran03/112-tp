

class Player():
    def __init__(self, app):
        #This seems weird
        x0, x1, y0, y1 = app.maze.getCellBounds(app, 0, 0)
        cx, cy = (x1 + x0) / 2, (y1 + y0) / 2
        self.location = (cx, cy)

    def checkLocation(self, app):
        cx, cy = self.location
        gridWidth  = app.width - 2*app.margin
        gridHeight = app.height - 2*app.margin
        cellWidth = gridWidth / app.maze.cols
        cellHeight = gridHeight / app.maze.rows
        col = (cx - app.margin - app.cellMargin)/(cellWidth)
        row = (cy - app.margin - app.cellMargin)/(cellHeight)
        return int(row), int(col)
    
    #Moving the player
    def moveWithKeys(self, app, event):
        if event.key == 'Up':
            self.movePlayer(app, 0, -5)
        elif event.key == 'Down':
            self.movePlayer(app, 0, 5)
        elif event.key == 'Left':
            self.movePlayer(app, -5, 0)
        elif event.key == 'Right':
            self.movePlayer(app, 5, 0)
    
    def movePlayer(self, app, dx, dy):
        cx, cy = self.location
        cx += dx
        cy += dy
        self.location = (cx, cy)

    #Drawing the player
    def drawPlayer(self, app, canvas):
        cx, cy = self.location
        x0, x1 = cx - 5, cx + 5
        y0, y1 = cy - 5, cy + 5
        canvas.create_oval(x0, y0, x1, y1, fill = 'red', outline = 'red')
    
    def render(self, app, canvas):
        self.drawPlayer(app, canvas)

