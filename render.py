import pygame
from Fizikia import*
from classes import*

   

"""Initialize Pygame"""
pygame.init()

""" Screen dimensions """
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics Visualization")

"""Clock for controlling FPS"""
clock = pygame.time.Clock()
FPS = 120

a = particle(30, [(500), 100.0],[10.0, 0.0], 'green')
b = particle(40, [(640), 100.0], [-10.0, 0.0], 'red')
particles=[a, b]
radius=10#to be changed by user with pygame framework

gridlist,gridwidth,gridheight=grid(WIDTH, HEIGHT, radius * 2)

dt = 0 
font = pygame.font.SysFont(None, 24)




running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    
    
    
    """collided=gridbfs(gridlist,gridwidth)
        for collisions in collided:
                momentum_after_collision(collisions[0],collisions[1])"""
    
    # resolve collisions with the wall
    if collision(a, b):
        momentum_after_collision(a, b)
        print('collided')

    # resolve collisions between particles
    for particle in particles:
        particle.wall_collision([WIDTH/2, HEIGHT/2])

    # update particle positions
    for particle in particles:
        particle.update_position(WIDTH, HEIGHT, dt)

    # -- Rendering --
    screen.fill("black")  # clear screen with black
    img = font.render(f'', True, 'red')
    screen.blit(img, (20, 20))

    for p in particles:
        pygame.draw.circle(screen, p.color, tuple(p.position), p.radius)

    pygame.display.flip()  # update the screen

    dt = clock.tick(FPS) * FPS/10000  # limit FPS
    print(dt)
    

    
    