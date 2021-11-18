#FROM https://www.youtube.com/watch?v=gYRrGTC7GtA
#https://permadi.com/1996/05/ray-casting-tutorial-7/
#raycasting test
from cmu_112_graphics import *
import math

class Ray():
    def __init__(self, app, angle):
        self.app = app
        self.angle = angle
        self.cx, self.cy = self.app.player
        self.castRay()
    
    def checkHorizontalLines(self):
        cx, cy = self.app.player
        if 0 < self.angle < math.pi:
            direction = 'Down'
            yOffset = 1
            firstIntersectionY = (cy // self.app.cellHeight + 1) * self.app.cellHeight
        elif math.pi < self.angle < 2*math.pi:
            direction = 'Up'
            yOffset = -1
            firstIntersectionY = (cy // self.app.cellHeight) * self.app.cellHeight
        else:
            direction = ''
            yOffset = 1
            firstIntersectionY = 0
        
        firstIntersectionX = cx + abs((cy - firstIntersectionY)) / math.tan(self.angle) * yOffset
        dx = self.app.cellHeight / math.tan(self.angle) * yOffset
        dy = self.app.cellHeight * yOffset
        
        rayX = firstIntersectionX
        rayY = firstIntersectionY

        while not(self.hitWall(rayX, rayY, direction)):
            rayX += dx
            rayY += dy
        
        return rayX, rayY

    def checkVerticalLines(self):
        cx, cy = self.app.player
        if 3/2*math.pi < self.angle <= 2*math.pi or 0 <= self.angle < 1/2*math.pi:
            direction = 'Right'
            xOffset = 1
            firstIntersectionX = (cx // self.app.cellWidth + 1) * self.app.cellWidth
        elif math.pi < self.angle < 2*math.pi:
            direction = 'Left'
            xOffset = -1
            firstIntersectionX = (cx // self.app.cellWidth) * self.app.cellWidth
        else:
            direction = ''
            xOffset = 1
            firstIntersectionX = 0

        firstIntersectionY = cy - abs(cx-firstIntersectionX) * math.tan(self.angle) * xOffset
        dx = self.app.cellWidth * xOffset
        dy = self.app.cellWidth * math.tan(self.angle) * xOffset

        rayX = firstIntersectionX
        rayY = firstIntersectionY
        
        while not(self.hitWall(rayX, rayY, direction)):
            rayX += dx
            rayY += dy
        
        return rayX, rayY

    def castRay(self):
        horizontalRayX, horizontalRayY = self.checkHorizontalLines()
        verticalRayX, verticalRayY = self.checkVerticalLines()

        print('h', horizontalRayX, horizontalRayY)
        print('v', verticalRayX, verticalRayY)

        horizontalRay = (horizontalRayX**2 + horizontalRayY**2)**(1/2)
        verticalRay = (verticalRayX**2 + verticalRayY**2)**(1/2)

        if horizontalRay > verticalRay:
            self.rayX = verticalRayX
            self.rayY = verticalRayY
        else:
            self.rayX = horizontalRayX
            self.rayY = horizontalRayY
            
        self.rayX = verticalRayX
        self.rayY = verticalRayY

    
    def hitWall(self, rayX, rayY, direction):
        if direction == 'Up':
            row, col = int(rayY//self.app.cellHeight-1), int(rayX//self.app.cellWidth)
        elif direction == 'Down':
            row, col = int(rayY//self.app.cellHeight), int(rayX//self.app.cellWidth)
        elif direction == 'Left':
            row, col = int(rayY//self.app.cellHeight), int(rayX//self.app.cellWidth-1)
        elif direction == 'Right':
            row, col = int(rayY//self.app.cellHeight), int(rayX//self.app.cellWidth)
        else: return True
        
        if not(0 < row < 5) or not(0 < col < 5) or self.app.maze[row][col] == 1:
            return True
        else:
            return False
        # return True
    
    def render(self, canvas):
        cx, cy = self.app.player
        canvas.create_line(cx, cy, self.rayX, self.rayY, fill = 'red')

def cellDimension(app):
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    app.cellWidth = gridWidth / len(app.maze[0])
    app.cellHeight = gridHeight / len(app.maze)

def appStarted(app):
    app.margin = 0
    app.player = (150, 150)
    app.playerAngle = 1/2*math.pi
    app.playerMove = (10*math.cos(app.playerAngle), 10*math.sin(app.playerAngle))
    app.maze =[[1, 1, 1, 1, 1],
               [1, 0, 0, 0, 1],
               [1, 0, 1, 0, 1],
               [1, 0, 0, 0, 1],
               [1, 1, 1, 1, 1]]
    cellDimension(app)
    app.ray = Ray(app, app.playerAngle)

def drawMaze(app, canvas):
    for row in range(len(app.maze)):
        for col in range(len(app.maze[0])):
            color = 'black'
            if app.maze[row][col] == 1:
                color = 'white'
            drawCell(app, canvas, row, col, color)


def drawCell(app, canvas, row, col, color = 'white'):
    x0, x1, y0, y1 = getCellBounds(app, row, col)
    canvas.create_rectangle(x0, y0, x1, y1, fill = color, outline = 'grey', width = 3)

def getCellBounds(app, row, col):
    #Taken from 112 Notes/Lecture (also what do we do about the app.table)
    x0 = app.margin + col * app.cellWidth
    x1 = app.margin + (col+1) * app.cellWidth
    y0 = app.margin + row * app.cellHeight
    y1 = app.margin + (row+1) * app.cellHeight
    return x0, x1, y0, y1

def drawPlayer(app, canvas):
    cx, cy = app.player
    dx, dy = app.playerMove
    r = 5
    canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill = 'yellow')
    canvas.create_line(cx, cy, cx+2*dx, cy+2*dy, fill = 'yellow', width = 3)

def redrawAll(app, canvas):
    drawMaze(app, canvas)
    drawPlayer(app, canvas)
    app.ray.render(canvas)

def movePlayer(app, direction):
    cx, cy = app.player
    dx, dy = app.playerMove
    cx += dx * direction
    cy += dy * direction
    app.player = (cx, cy)

def keyPressed(app, event):
    if event.key == 'Up':
        movePlayer(app, 1)
    elif event.key == 'Down':
        movePlayer(app, -1)
    
    if event.key == 'Left':
        app.playerAngle -= math.pi/24
        if app.playerAngle < 0:
            app.playerAngle += 2*math.pi
        dx, dy = app.playerMove
        dx = math.cos(app.playerAngle)
        dy = math.sin(app.playerAngle)
        app.playerMove = (10*dx, 10*dy)
   
    elif event.key == 'Right':
        app.playerAngle += math.pi/24
        if app.playerAngle > 2*math.pi:
            app.playerAngle -= 2*math.pi
        dx, dy = app.playerMove
        dx = math.cos(app.playerAngle)
        dy = math.sin(app.playerAngle)
        app.playerMove = (10*dx, 10*dy)
    
    app.ray = Ray(app, app.playerAngle)





runApp(width=500,height=500)