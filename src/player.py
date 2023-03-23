import math

class Player:
    def __init__(self, startX, startY, controls, step=5, angle=0, width=0, size=5, color='red'):
        self.cx = startX
        self.cy = startY
        self.angle = angle
        self.step = step
        self.dx, self.dy = (self.step * math.cos(self.angle), self.step*math.sin(self.angle))
        self.mousePos = width/2
        self.controls = controls
        self.size = size
        self.color = color
    
    def getRow(self, maze):
        return math.floor(self.cy / maze.getCellHeight())
    
    def getCol(self, maze):
        return math.floor(self.cx / maze.getCellWidth())

    def isIllegalPosition(self, maze):
        row, col = self.getRow(maze), self.getCol(maze)
        return maze.checkPos(row, col)
    
    def keyPressed(self, event, maze):
        # Movement
        if event.key in self.controls['Up']:
            self.movePlayer(1, 'Up', maze)
        elif event.key in self.controls['Down']:
            self.movePlayer(-1, 'Down', maze)
        elif event.key in self.controls['Left']:
            self.movePlayer(-1, 'Left', maze)
        elif event.key in self.controls['Right']:
            self.movePlayer(1, 'Right', maze)

        # Turning
        if event.key in self.controls['Turn Left']:
            self.angle -= math.pi/self.controls['Turn Speed']
            
            # Accounts for overangling
            if self.angle < 0: self.angle += 2*math.pi
            
            # Calculations from angle to movement
            self.dx = self.step * math.cos(self.angle)
            self.dy = self.step * math.sin(self.angle)
        
        elif event.key in self.controls['Turn Right']:
            self.angle += math.pi/self.controls['Turn Speed']
            
            # Accounts for overangling
            if self.angle > 2*math.pi:
                self.angle -= 2*math.pi
            
            # Calculations from angle to movement
            self.dx = self.step * math.cos(self.angle)
            self.dy = self.step * math.sin(self.angle)

    def mouseMoved(self , event):
        #TODO put in controls
        difference = event.x - self.mousePos
        self.angle += math.pi*difference/self.controls['Sensitivity']
    
    def movePlayer(self, direction, directionName, maze):
        cx, cy = self.cx, self.cy
        if directionName == 'Up' or directionName == 'Down':
            self.cx += self.dx * direction
            self.cy += self.dy * direction
        
        # TODO FIX
        elif directionName == 'Left' or directionName == 'Right':
            self.cx += (self.dy * direction * -1)/2
            self.cy += (self.dx * direction)/2
        
        if not self.isIllegalPosition(maze):
            self.cx = cx
            self.cy = cy
    
    def render(self, canvas):
        r = self.size
        canvas.create_oval(self.cx-r, self.cy-r, self.cx+r, self.cy+r, fill = self.color)



    



        