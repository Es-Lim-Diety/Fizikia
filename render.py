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

a=particle(5,vector(300,100),vector(5,0),vector(0,0),(0, 255, 0))
b=particle(40,vector(500,100),vector(-5,0),vector(0,0),(255, 0, 0))
particles=[a,b]

def wall_collision(particle, middle):
        distance_from_middle = abs(particle.position.x - middle)
        allowed_distance_from_middle = middle - particle.radius
        if distance_from_middle >= allowed_distance_from_middle:
            particle.velocity.x *= -1  

running = True
while running:

    if collision(a, b):
        momentum_after_collision(a, b)
        print('collided')

    
    for particle in particles:
         wall_collision(particle, WIDTH/2)


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
