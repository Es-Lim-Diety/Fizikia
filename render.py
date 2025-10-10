import pygame
import pygame_gui

from Fizikia import*
from classes import*

"""Initialize Pygame"""
pygame.init()

# setup
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle Setup")
clock = pygame.time.Clock()
FPS = 60
dt = 0
# UI Manager
manager = pygame_gui.UIManager((WIDTH, HEIGHT))



# menu widgets
particle_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((250, 100), (300, 40)), start_value=10, value_range=(1, 5000), manager=manager
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

# game state
STATE = "menu"
equal_mode = True
particles=[]

# main loop
running = True
while running:

    dt = clock.tick(FPS) *60 / 1000.0
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

                    if equal_mode:
                        wallgrids, gridlist, gridwidth, gridheight = grid(WIDTH, HEIGHT, 10)
                        sidelength=10
                        incr=math.floor((len(gridlist) / num))
                        idx=0
                        for i in range(num):
                            position = gridlist[idx].position
                            x, y = revhash_grid(position, gridwidth,10)
                            vx, vy = velocity([WIDTH/2, HEIGHT/2], [x, y])
                            particles += [particle(5, [x, y], [vx, vy], 'green', 5)]
                            idx += incr
                        # create a dictionary to make it easy to identify particles
                        particles_to_index_map = {id(p): i for i, p in enumerate(particles)}
                        # fetch the positions, velocities and masses of every particle and store in a numpy array (will be useful for collision resolution)
                        position_data = [p.position for p in particles]
                        velocity_data = [p.velocity for p in particles]
                        mass_data = [p.mass for p in particles]
                        positions = np.array(position_data, dtype=float)
                        velocities = np.array(velocity_data, dtype=float)
                        # reshape to make sure its a column vector
                        masses = np.array(mass_data, dtype=float).reshape(-1, 1)
                    STATE = "simulation"

    # drawing

    if STATE == "menu":
        screen.fill((20, 20, 20))
        manager.update(dt)
        manager.draw_ui(screen)

    elif STATE == "simulation":
        pygame.display.set_caption("Physics Visualization")
        # handle collisions between particles
        # find all the collision pairs
        collision_matrix = gridbfs_uniformradius(gridlist, gridwidth, particles_to_index_map)

        # resolve collisions, but the output will be stored in the velocity array
        if collision_matrix.size > 0:
            resolve_collisions_numpy(collision_matrix, positions, velocities, masses)
        
        screen.fill("black")

        for idx in range(len(particles)):
            # Get the particle object from your master list
            particles[idx].velocity=velocities[idx]            
            # Get the new velocity from the updated NumPy array            
            # Assign the new velocity back to the object's attribute
            if particles[idx].grid in wallgrids:
                particles[idx].wall_collision(WIDTH, HEIGHT)
                #velocities[idx] = particles[idx].velocity  # Update velocities array if needed
            particles[idx].update_position(WIDTH, HEIGHT, sidelength, gridwidth, gridlist, dt)
            #positions[idx] = particles[idx].position  # Update positions array if needed
            pygame.draw.circle(screen, particles[idx].color, tuple(particles[idx].position), particles[idx].radius)            

        # rendering
         # clear screen with black

        
            
    fps = clock.get_fps()
    print(f"Rendering at {fps}fps")
    pygame.display.flip()
pygame.quit()