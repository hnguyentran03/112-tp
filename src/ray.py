import math

class Ray:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
    
    def getDistance(self):
        return math.sqrt(self.x**2 + self.y**2)