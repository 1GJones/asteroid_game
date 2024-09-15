
import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from asteroid import CircleShape, Asteroid, AsteroidField
import random
import math
import sys

PLAYER_SPIN_SPEED = 300
PLAYER_SPEED = 200
SHOT_RADIUS = 5
PLAYER_SHOOT_COOLDOWN = 0.3
class Player(pygame.sprite.Sprite):  # Inherit from pygame.sprite.Sprite
   
    def __init__(self, x, y, radius):
        super().__init__()  # Call the parent class (Sprite) constructor
        self.x = x
        self.y = y
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.radius = radius
        self.color = (255, 255, 255)  # white
        self.rotation = 0  # Initialize rotation in degrees
        self.position = pygame.Vector2(x, y)  # Initialize the player's position
        self.shoot_timer = 0  # Initialize the shoot cooldown timer

        
    def to_circle(self):
        # Pass x and y components separately along with the radius
        return CircleShape(self.position.x, self.position.y, self.radius)

    def move(self, dt):  # Move the player forward
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def move_backwards(self, dt):  # Move player backwards based on rotation
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        self.position -= forward * PLAYER_SPEED * dt  # Subtract to move backwards

    def rotate(self, dt):
        # Rotate Player based on spin
        self.rotation += PLAYER_SPIN_SPEED * dt

    def update(self, dt):
        # Handle player input and update the player rotation
        keys = pygame.key.get_pressed()
        
        if self.shoot_timer > 0:
            self.shoot_timer -= dt

        if keys[pygame.K_a]:  # Rotate left
            self.rotate(-dt)  # Negative rotation for left

        if keys[pygame.K_d]:  # Rotate right (clockwise)
            self.rotate(dt)  # Positive rotation for right

        if keys[pygame.K_w]:  # Move forward
            self.move(dt)

        if keys[pygame.K_s]:  # Move backward
            self.move_backwards(dt)
            
            
    def can_shoot(self):
        # The player can shoot if the shoot_timer has reached 0
        return self.shoot_timer <= 0

    def shoot(self):
        # Reset the shoot timer when firing a shot
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN


    def draw(self, screen):
        # Draw the player as a triangle
        pygame.draw.polygon(screen, self.color, self.triangle(), 2)

    def triangle(self):
        # This method returns the points of the triangle for drawing
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        right = pygame.Vector2(1, 0).rotate(self.rotation) * (self.radius / 1.5)

        a = self.position + forward * self.radius  # Tip of the triangle
        b = self.position - forward * self.radius - right  # Base point 1
        c = self.position - forward * self.radius + right  # Base point 2
        return [a, b, c]

# Shot Class

class Shot(CircleShape):
    def __init__(self, x, y, rotation):
        super().__init__(x, y, SHOT_RADIUS,)
        self.velocity = pygame.Vector2(0, -1).rotate(rotation) * 500
        self.color = (255, 255, 0)

    def update(self, dt):
        self.position += self.velocity * dt

        if self.position.x < 0 or self.position.x > SCREEN_WIDTH or self.position.y < 0 or self.position.y > SCREEN_HEIGHT:
            self.kill()  # Remove shot if it goes off screen

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)


def main():
    pygame.init()
    clock = pygame.time.Clock()  # Initialize the clock
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids Game")

    # Group for shots (bullets)
    shots = pygame.sprite.Group()

    # Player and groups
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 50)
    updatable = pygame.sprite.Group()  # All objects needed to update
    drawable = pygame.sprite.Group()  # All objects needed to draw
    asteroids = pygame.sprite.Group()

    # Set static containers for the Asteroid class
    Asteroid.containers = (asteroids, updatable, drawable)

    updatable.add(player)
    drawable.add(player)

    num_asteroids = 15
    
    asteroid_field = AsteroidField(num_asteroids, updatable, drawable)

    # Game Loop
    running = True
    while running:
        screen.fill((0, 0, 0))  # Fill the screen with black

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle player shots
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and player.can_shoot():  # Fire a shot when spacebar is pressed
            shot = Shot(player.position.x, player.position.y, player.rotation)
            shots.add(shot)
            updatable.add(shot)
            drawable.add(shot)
            player.shoot()  # Reset the player's shoot timer


        # Update all sprites
        updatable.update(dt)

        # Check for player-asteroid collisions
        if asteroid_field.check_collision(player.to_circle()):
            print("Game over!")
            pygame.quit()
            sys.exit()  # Exit the game

        # Check for shot-asteroid collisions
        for shot in shots:
            for asteroid in asteroids:
                if shot.check_collision_with_circle(asteroid):
                    print("Asteroid hit!")
                    shot.kill()  # Remove the shot
                    asteroid.split() # Optionally, remove the asteroid

        # Draw all sprites in the drawable group
        for sprite in drawable:
            sprite.draw(screen)

        pygame.display.flip()

        # Cap the frame rate and calculate delta time
        dt = clock.tick(60) / 1000  # Ensures the game loop runs at 60 FPS

    pygame.quit()


if __name__ == "__main__":
    main()
