import pygame
from Fizikia import*
from classes import*

   

"""Initialize Pygame"""
pygame.init()

""" Screen dimensions """
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics Visualization")

"""Clock for controlling FPS"""
clock = pygame.time.Clock()
FPS = 60

a = particle(30, [300.0, 100.0],[5.0, 0.0], [0.0,2],(0, 255, 0))
b = particle(40, [500.0, 80.0], [-5.0, 0.0], [0.0, 3], (255, 0, 0))
particles=[a, b]

  

running = True
while running:

    if collision(a, b):
        momentum_after_collision(a, b)
        print('collided')

    for particle in particles:
        particle.wall_collision([WIDTH/2, HEIGHT/2])

    for particle in particles:
        particle.update_position(WIDTH, HEIGHT)

    # -- Rendering --
    screen.fill((0, 0, 0))  # clear screen with black

    for p in particles:
        pygame.draw.circle(screen, p.color, tuple(p.position), p.radius)

    pygame.display.flip()  # update the screen

    clock.tick(FPS)  # limit FPS

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
