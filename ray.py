#Initialization of rays taken from  https://www.youtube.com/watch?v=gYRrGTC7GtA
#Calculations and inspiration for rays taken from https://permadi.com/1996/05/ray-casting-tutorial-7/
#raycasting test

from cmu_112_graphics import *
from graph import *
import math

#HELPER
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
    
    #Checks for every single horizontal barrier in rows
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
        
        #Calculates where the rays intersect with the first row it hits
        firstIntersectionX = cx + abs((cy - firstIntersectionY)) / math.tan(self.angle) * yOffset
        
        dx = self.app.cellHeight / math.tan(self.angle) * yOffset
        dy = self.app.cellHeight * yOffset
        rayX = firstIntersectionX
        rayY = firstIntersectionY

        #Extends ray until a wall
        while not(self.hitWall(rayX, rayY, direction)):
            rayX += dx
            rayY += dy
        
        return rayX, rayY

    #Checks for every single horizontal barrier in cols
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

        #Calculates where the rays intersect with the first col it hits
        firstIntersectionY = cy + abs(cx-firstIntersectionX) * math.tan(self.angle) * xOffset
        dx = self.app.cellWidth * xOffset
        dy = self.app.cellWidth * math.tan(self.angle) * xOffset

        rayX = firstIntersectionX
        rayY = firstIntersectionY
        
        #Extends ray until a wall
        while not(self.hitWall(rayX, rayY, direction)):
            rayX += dx
            rayY += dy
        
        return rayX, rayY

    #Calculates the shortest between the horizontal intersections and the vertical ones
    def castRay(self):
        cx, cy = self.app.player.location
        horizontalRayX, horizontalRayY = self.checkHorizontalLines()
        verticalRayX, verticalRayY = self.checkVerticalLines()
        
        #Sets the rays to be from the player
        horizontalRayX, horizontalRayY = horizontalRayX-cx, horizontalRayY-cy
        verticalRayX, verticalRayY = verticalRayX-cx, verticalRayY-cy

        #Calculates the distance of the ray
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
        
        #Calculates the row and col (because of precision errors)
        if almostEqual(row, math.ceil(row)): row = math.ceil(row)
        else: row = math.floor(row)

        col = rayX/self.app.cellWidth
        if almostEqual(col, math.ceil(col)): col = math.ceil(col)
        else: col = math.floor(col)
        
        #Recalculates the row and col based on which direction
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
        if  outOfBounds or self.app.maze[row][col] == 1: return True
        else: return False
    
    def render(self, canvas):
        cx, cy = self.app.player.location
        canvas.create_line(cx, cy, cx+self.rayX, cy+self.rayY, fill = 'purple')