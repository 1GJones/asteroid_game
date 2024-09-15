import pygame


# Base class for the games objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will use this later
        if hasattr(self, "containers"):
           super().__init__(self.containers)
        else:
            super().__init__()
            
            self.position = pygame.Vector2(x, y)
            self.velocity = pygame.Vector2(0, 0)
            self.radius = radius
            
    def draw(screen):
        white = (255, 255, 255)
 
      # sub-classes must override
        pygame.draw.polygon(screen, white,) 
            
    def update(self, dt):
       # sub-classes must override
         pass
                
