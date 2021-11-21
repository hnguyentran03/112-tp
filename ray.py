#FROM https://www.youtube.com/watch?v=gYRrGTC7GtA
#https://permadi.com/1996/05/ray-casting-tutorial-7/
#raycasting test
from cmu_112_graphics import *
from graph import *
import math

def almostEqual(d1, d2):
    epsilon = 10**-10
    return (abs(d2 - d1) < epsilon)

class Ray():
    def __init__(self, app, angle):
        self.app = app
        self.angle = angle
        self.castRay()
    
    def getDistance(self):
        distance = (self.rayX**2 + self.rayY**2)**(1/2)
        return distance
    
    def checkHorizontalLines(self):
        cx, cy = self.app.player.location
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
        print('intersect', firstIntersectionX, firstIntersectionY)
        rayX = firstIntersectionX
        rayY = firstIntersectionY

        while not(self.hitWall(rayX, rayY, direction)):
            rayX += dx
            rayY += dy
        
        return rayX, rayY

    def checkVerticalLines(self):
        cx, cy = self.app.player.location
        if 3/2*math.pi < self.angle <= 2*math.pi or 0 <= self.angle < 1/2*math.pi:
            direction = 'Right'
            xOffset = 1
            firstIntersectionX = (cx // self.app.cellWidth + 1) * self.app.cellWidth
        elif 1/2*math.pi < self.angle <= math.pi or math.pi <= self.angle < 3/2*math.pi:
            direction = 'Left'
            xOffset = -1
            firstIntersectionX = (cx // self.app.cellWidth) * self.app.cellWidth
        else:
            direction = ''
            xOffset = 1
            firstIntersectionX = 0

        firstIntersectionY = cy + abs(cx-firstIntersectionX) * math.tan(self.angle) * xOffset
        dx = self.app.cellWidth * xOffset
        dy = self.app.cellWidth * math.tan(self.angle) * xOffset

        rayX = firstIntersectionX
        rayY = firstIntersectionY
        
        while not(self.hitWall(rayX, rayY, direction)):
            rayX += dx
            rayY += dy
        
        return rayX, rayY

    def castRay(self):
        cx, cy = self.app.player.location
        horizontalRayX, horizontalRayY = self.checkHorizontalLines()
        verticalRayX, verticalRayY = self.checkVerticalLines()
        horizontalRayX, horizontalRayY = horizontalRayX-cx, horizontalRayY-cy
        verticalRayX, verticalRayY = verticalRayX-cx, verticalRayY-cy

        horizontalRay = ((horizontalRayX)**2 + (horizontalRayY)**2)**(1/2)
        verticalRay = ((verticalRayX)**2 + (verticalRayY)**2)**(1/2)

        if horizontalRay > verticalRay:
            self.rayX = verticalRayX
            self.rayY = verticalRayY
        else:
            self.rayX = horizontalRayX
            self.rayY = horizontalRayY
    
    def hitWall(self, rayX, rayY, direction):
        row = rayY/self.app.cellHeight
        if almostEqual(row, math.ceil(row)):
            row = math.ceil(row)
        else:
            row = math.floor(row)

        col = rayX/self.app.cellWidth
        if almostEqual(col, math.ceil(col)):
            col = math.ceil(col)
        else:
            col = math.floor(col)

        if direction == 'Up':
            row, col = row-1, col
        elif direction == 'Down':
            row, col = row, col
        elif direction == 'Left':
            row, col = row, col-1
        elif direction == 'Right':
            row, col = row, col
        else: return True
        
        outOfBounds = not(0 <= row < len(self.app.maze)) or not(0 <= col < len(self.app.maze))
        if  outOfBounds or self.app.maze[row][col] == 1:
            return True
        else:
            return False
    
    def render(self, canvas):
        cx, cy = self.app.player.location
        canvas.create_line(cx, cy, cx+self.rayX, cy+self.rayY, fill = 'red')






# #TESTING
# def cellDimension(app):
#     gridWidth  = 500
#     gridHeight = 500
#     app.cellWidth = gridWidth / len(app.maze[0])
#     app.cellHeight = gridHeight / len(app.maze)

# def appStarted(app):
#     app.margin = 0
#     app.player = (150, 150)
#     app.playerAngle = 1/2*math.pi
#     app.mazeGen = Maze(app)
#     app.mazeGen.dfsMaze(5,5)
#     # app.maze =[[1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
#     #            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#     #            [1, 0, 1, 0, 1, 1, 1, 1, 0, 0],
#     #            [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
#     #            [1, 0, 1, 1, 0, 1, 0, 1, 1, 1],
#     #            [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
#     #            [0, 0, 0, 0, 1, 0, 0, 0, 1, 1],
#     #            [1, 0, 1, 0, 1, 1, 0, 0, 0, 0],
#     #            [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
#     #            [1, 0, 1, 1, 0, 1, 0, 1, 1, 1]]

#     app.maze = app.mazeGen.convertTo2DList()

#     cellDimension(app)
#     app.numRays = int(len(app.maze)*10)
#     createRays(app)
#     app.state = False
#     app.step = len(app.maze)/2
#     if app.step > 0:
#         app.turn = int(app.step)-1
#     else:
#         app.turn = int(app.step)
#     app.playerMove = (app.step*math.cos(app.playerAngle), app.step*math.sin(app.playerAngle))

# def createRays(app):
#     app.rays = []
#     for difference in range(app.numRays):
#         angleDifference = math.pi/(2**9)*difference
        
#         leftAngle = app.playerAngle-angleDifference
#         rightAngle = app.playerAngle+angleDifference
#         if leftAngle < 0: leftAngle += 2*math.pi
#         elif leftAngle > 2*math.pi: leftAngle -= 2*math.pi
#         if rightAngle < 0: rightAngle += 2*math.pi
#         elif rightAngle > 2*math.pi: rightAngle -= 2*math.pi

#         leftRay = Ray(app, leftAngle)
#         rightRay = Ray(app, rightAngle)
#         app.rays.insert(0, leftRay)
#         app.rays.append(rightRay)

# def drawMaze(app, canvas):
#     for row in range(len(app.maze)):
#         for col in range(len(app.maze[0])):
#             color = 'white'
#             if app.maze[row][col] == 1:
#                 color = 'black'
#             drawCell(app, canvas, row, col, color)


# def drawCell(app, canvas, row, col, color = 'white'):
#     x0, x1, y0, y1 = getCellBounds(app, row, col)
#     canvas.create_rectangle(x0, y0, x1, y1, fill = color, outline = 'grey', width = 3)

# def getCellBounds(app, row, col):
#     #Taken from 112 Notes/Lecture (also what do we do about the app.table)
#     x0 = app.margin + col * app.cellWidth
#     x1 = app.margin + (col+1) * app.cellWidth
#     y0 = app.margin + row * app.cellHeight
#     y1 = app.margin + (row+1) * app.cellHeight
#     return x0, x1, y0, y1

# def drawPlayer(app, canvas):
#     cx, cy = app.player
#     dx, dy = app.playerMove
#     r = 5
#     canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill = 'yellow')
#     canvas.create_line(cx, cy, cx+2*dx, cy+2*dy, fill = 'yellow', width = 3)

# def redrawAll(app, canvas):
#     if app.state:
#         draw3D(app, canvas)
#     else:
#         drawMaze(app, canvas)
#         drawPlayer(app, canvas)
#         for ray in app.rays:
#             ray.render(canvas)

# def movePlayer(app, direction, directionName):
#     cx, cy = app.player
#     dx, dy = app.playerMove
#     if directionName == 'Up' or directionName == 'Down':
#         cx += dx * direction
#         cy += dy * direction
#     elif directionName == 'Left' or directionName == 'Right':
#         cx += dy * direction
#         cy += dx * direction
    
#     app.player = (cx, cy)

# def keyPressed(app, event):
#     if event.key == 'w':
#         movePlayer(app, 1, 'Up')
#     elif event.key == 's':
#         movePlayer(app, -1, 'Down')
#     elif event.key == 'a':
#         movePlayer(app, -1, 'Left')
#     elif event.key == 'd':
#         movePlayer(app, 1, 'Right')
#     if event.key == 'Left':
#         app.playerAngle -= math.pi/(3*(2**app.turn))
#         if app.playerAngle < 0:
#             app.playerAngle += 2*math.pi
#         dx, dy = app.playerMove
#         dx = math.cos(app.playerAngle)
#         dy = math.sin(app.playerAngle)
#         app.playerMove = (app.step*dx, app.step*dy)
   
#     elif event.key == 'Right':
#         app.playerAngle += math.pi/ (3*(2**app.turn))
#         if app.playerAngle > 2*math.pi:
#             app.playerAngle -= 2*math.pi
#         dx, dy = app.playerMove
#         dx = math.cos(app.playerAngle)
#         dy = math.sin(app.playerAngle)
#         app.playerMove = (app.step*dx, app.step*dy)
    
#     createRays(app)

#     if event.key == 'p':
#         app.state = not app.state

# #USEFUL
# def draw3D(app, canvas):
#     wallHeight = 200
#     constant = 255
#     midpoint = app.height/2
#     dx = app.width / app.numRays
#     for i, ray in enumerate(app.rays):
#         distanceToWall = ray.getDistance()
#         try:
#             color = f'#00{hex(int(255*(app.cellHeight/distanceToWall)))[-2:]}00'
#             height = wallHeight/(distanceToWall)*constant
#         except ZeroDivisionError:
#             color = f'#00{hex(int(255*(app.cellHeight/(distanceToWall+1))))[-2:]}00'
#             height = wallHeight/(distanceToWall+1)*constant
#         y0 = midpoint - height/2
#         y1 = midpoint + height/2
#         x0 = dx * i
#         x1 = dx * (i + 1)
#         canvas.create_rectangle(x0, y0, x1, y1, fill = color, outline = '')

# runApp(width=500,height=500)