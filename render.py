import pygame
from Fizikia import*

"""Initialize Pygame"""
pygame.init()

""" Screen dimensions """
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics Visualization")

"""Clock for controlling FPS"""
clock = pygame.time.Clock()
FPS = 60

a=particle(69,vector(100,100),vector(1,0),vector(0,0),(0, 255, 0))
b=particle(420,vector(500,100),vector(-1,0),vector(0,0),(255, 0, 0))
particles=[a,b]
running = True
while running:

    if collision(a, b):
        momentum_after_collision(a, b)
        print('collided')

    a.update_position()
    b.update_position()

    # -- Rendering --
    screen.fill((0, 0, 0))  # clear screen with black

    for p in particles:
        pygame.draw.circle(screen, p.color, (p.position.x, p.position.y), p.radius)

    pygame.display.flip()  # update the screen

    clock.tick(FPS)  # limit FPS
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
