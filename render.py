import pygame
import pygame_gui

from Fizikia import*
from classes import*

"""Initialize Pygame"""
pygame.init()

# --- Setup ---
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle Setup")
clock = pygame.time.Clock()
FPS = 120
dt = 0
font = pygame.font.SysFont(None, 24)

# UI Manager
manager = pygame_gui.UIManager((WIDTH, HEIGHT))



# --- Menu Widgets ---
particle_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((250, 100), (300, 40)), start_value=10, value_range=(1, 100), manager=manager
    )
label_particle_slider = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(560, 100, 200, 40), text=f"Number of particle: {particle_slider.get_current_value():.0f}", manager=manager
    )

radius_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((250, 160), (300, 40)), start_value=10, value_range=(1, 50), manager=manager, click_increment=0.001
    )
label_radius_slider = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(560, 160, 200, 40), text=f"Radius of particles: {radius_slider.get_current_value():.0f}", manager=manager
    )

mass_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((250, 220), (300, 40)), start_value=5, value_range=(1, 50), manager=manager
    )
label_mass_slider = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(560, 220, 200, 40), text=f"Particle Mass: {mass_slider.get_current_value():.0f}", manager=manager
    )

equal_checkbox = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((250, 280), (300, 40)), text=f"Mode", manager=manager
    )

start_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((250, 340), (300, 40)), text="Start Simulation", manager=manager
    )

# --- Game State ---
STATE = "menu"
equal_mode = True
a = particle(20, [(500), 100.0],[20.0, 0.0], 'green')
b = particle(25, [(600), 90.0], [-20.0, 0.0], 'red')
c = particle(30, [(700), 80.0], [-20.0, 0.0], 'blue')
d = particle(35, [(800), 70.0], [-20.0, 0.0], 'white')
e = particle(40, [(900), 60.0], [-20.0, 0.0], 'purple')
particles=[a, b, c, d, e] # will hold simulation particles


# --- Main Loop ---
running = True
while running:

    dt = clock.tick(FPS) * 60 / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if STATE == "menu":
            manager.process_events(event)
            # record slider input
            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == particle_slider:
                    new_value = particle_slider.get_current_value()
                    label_particle_slider.set_text(f"Number of particle: {new_value:.0f}")

                if event.ui_element == radius_slider:
                    new_value = radius_slider.get_current_value()
                    label_radius_slider.set_text(f"Radius of particles: {new_value:.0f}")

                if event.ui_element == mass_slider:
                    new_value = mass_slider.get_current_value()
                    label_mass_slider.set_text(f"Particle Mass: {new_value:.0f}")

            # record button input
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == equal_checkbox:
                    equal_mode = not equal_mode
                    equal_checkbox.set_text(f"Mode: Equal mass {equal_mode}")
                if event.ui_element == start_button:
                    # collect user settings
                    num = int(particle_slider.get_current_value())
                    radius = int(radius_slider.get_current_value())
                    mass = int(mass_slider.get_current_value())
                    
                    STATE = "simulation"

    # --- Drawing ---    

    if STATE == "menu":
        screen.fill((20, 20, 20))
        manager.update(dt)
        manager.draw_ui(screen)

    elif STATE == "simulation":
        pygame.display.set_caption("Physics Visualization")

        for particleA in particles:
            for particleB in particles:
                if not particleA == particleB:
                    if collision(particleA, particleB):
                        momentum_after_collision(particleA, particleB)

        # resolve collisions with the wall
        for particle in particles:
            particle.wall_collision([WIDTH/2, HEIGHT/2])

        # update particle positions
        for particle in particles:
            particle.update_position(WIDTH, HEIGHT, dt)

        # -- Rendering --
        screen.fill("black")  # clear screen with black
        img = font.render(f'hello', True, 'red')
        screen.blit(img, (20, 20))

        for p in particles:
            pygame.draw.circle(screen, p.color, tuple(p.position), p.radius)
        
    pygame.display.flip()

pygame.quit()