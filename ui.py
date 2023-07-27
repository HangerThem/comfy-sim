import pygame
import sys
import random

pygame.init()

# Set up some window constants
WIDTH, HEIGHT = 640, 480
WHITE = (255, 255, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ComfySim")

default_cursor = pygame.image.load('assets/hand.png')
default_cursor = pygame.transform.scale(default_cursor, (256, 256))
cursor_size = default_cursor.get_size()

click_cursor = pygame.image.load('assets/click.png')
click_cursor = pygame.transform.scale(click_cursor, (256, 256))

bg_img = pygame.image.load('assets/peepo2.png')
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

bg_mask = pygame.mask.from_surface(bg_img)  # create a mask from the background image

pygame.mouse.set_visible(False)

current_cursor = default_cursor

OBJECT_CLICKED = pygame.USEREVENT + 1

class Particle:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.alpha = 255

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.alpha -= 5  # fade out a bit each frame

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 105, 180, self.alpha), (int(self.x), int(self.y)), 3)

# List of all particles
particles = []

# Run until the user asks to quit
running = True
while running:
    # Fill the background with white
    screen.fill(WHITE)

    screen.blit(bg_img, (0, 0))

    for particle in particles:
        particle.update()
        particle.draw(screen)

    x, y = pygame.mouse.get_pos()
    screen.blit(current_cursor, (x - cursor_size[0], y))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            current_cursor = click_cursor
            # Check if the click was within the background image
            try:
                if bg_mask.get_at((event.pos[0], event.pos[1])):
                    pygame.event.post(pygame.event.Event(OBJECT_CLICKED))
                    for _ in range(25):
                        particles.append(Particle(event.pos[0], event.pos[1], random.uniform(-3, 3), random.uniform(-3, 3)))
            except IndexError:
                pass
        elif event.type == pygame.MOUSEBUTTONUP:
            current_cursor = default_cursor
        elif event.type == OBJECT_CLICKED:
            print("Background image was clicked!")

    # Remove particles that have faded out
    particles = [particle for particle in particles if particle.alpha > 0]

# Done! Time to quit.
pygame.quit()
sys.exit()
