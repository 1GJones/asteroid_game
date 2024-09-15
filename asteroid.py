
import pygame
import math
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        super().__init__()
        self.position = pygame.Vector2(x, y)
        self.radius = radius
        self.color = (255, 255, 255)
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)
        
    def check_collision_with_circle(self, other_circle):
        # Calculate the distance between the centers of the two circles 
        dx = self.position.x - other_circle.position.x
        dy = self.position.y - other_circle.position.y
        distance = math.sqrt(dx * dx + dy * dy)
        
        # Check if the distance is less than the sum of the radii
        return distance < (self.radius + other_circle.radius)

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
       super().__init__(x, y, radius)
       self.velocity = pygame.Vector2(random.uniform(-100, 100), random.uniform(-100, 100))
       self.color = (255, 255, 255)
       if self.containers:
           self.add(self.containers)
           
    def split(self):
         # Kill this asteroid (destroy the current one)
        ASTEROID_MIN_RADIUS = 10
         
        if self.radius <= ASTEROID_MIN_RADIUS: 
           self.kill()
           return
            
            # Generate a random angle for splitting between 20 and 50 degrees
        random_angle = random.uniform(20, 50)
            
            # Create two new smaller asteroids with half the current radiu 
        new_radius = self.radius // 2
            
            # Create the first smaller asteroid, rotated by +random_angle
        asteroid_1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_1.velocity = self.velocity.rotate(random_angle)* 1.2 # Scale up the velocity by 1.2
            
            # Create the second smaller asteroid, rotated by -random_angle
        asteroid_2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_2.velocity = self.velocity.rotate(-random_angle)* 1.2 # Scale up the velocity by 1.2
        
        # Add the new asteroids to the containers (game's sprite groups)
        if self.containers:
            asteroid_1.add(self.containers)
            asteroid_2.add(self.containers)

        # Destroy the current large asteroid
        self.kill()      
            
    def draw(self, screen):
       pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)
          
           
    def update(self, dt):
        # Move the asteroid based on its velocity
        self.position += self.velocity * dt

        # Wrap around the screen edges
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = 0

        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0

       
class Shot(pygame.sprite.Sprite):
    def __init__(self, x, y, rotation):
        super().__init__()
        self.image = pygame.Surface((5,5))
        self.image.fill(255, 215, 0)
        self.rect = self.image.get_rect(center=(x, y))
        self.position = pygame.Vector2(x, y)
        self.rotation = rotation
        self.velocity = pygame.Vector2(0, -1).rotate(rotation) * 500
        
       
        
        
    def update(self, dt):
        self.position += self.velocity * dt

        # Keep asteroids within screen boundaries by wrapping around
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)

    
class AsteroidField:
    def __init__(self, num_asteroids, updatable_group, drawable_group, safe_zone_radius=200):
        self.asteroids = []

        for _ in range(num_asteroids):
            while True:
                # Randomly generate a position for the asteroid
                x = random.randint(0, SCREEN_WIDTH)
                y = random.randint(0, SCREEN_HEIGHT)

                # Calculate the distance from the player's starting position (center of the screen)
                distance_to_player = math.sqrt((x - SCREEN_WIDTH / 2) ** 2 + (y - SCREEN_HEIGHT / 2) ** 2)

                # Ensure the asteroid doesn't spawn too close to the player
                if distance_to_player > safe_zone_radius:
                    break  # Valid spawn position, break out of the loop

            # Create the asteroid and add it to the groups
            asteroid = Asteroid(x, y, random.randint(30, 50))  # Random radius for asteroids
            updatable_group.add(asteroid)
            drawable_group.add(asteroid)
            self.asteroids.append(asteroid)

    def check_collision(self, other_circle):
        for asteroid in self.asteroids:
            if asteroid.check_collision_with_circle(other_circle):
                return True
        return False
