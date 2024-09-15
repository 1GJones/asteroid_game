
import pygame
import math

from circleshape import CircleShape # Assuming CircleShape is in shapes.py


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y)
        
        self.position = pygame.Vector2(x, y)
        self.rotation = 0 
        print(type(CircleShape))
        
    def triangle(self):
        # Example triangle centered around (self.x, self.y)
        angle = math.radians(0)
        offset_angle = 120  # Degrees between each point

        points = []
        for i in range(3):  # Triangle has 3 points
            x = self.x + self.radius * math.cos(angle)
            y = self.y + self.radius * math.sin(angle)
            points.append((x, y))
            angle += math.radians(offset_angle)
            return points
    
