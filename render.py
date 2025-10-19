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
# UI Manager
manager = pygame_gui.UIManager((WIDTH, HEIGHT))
# function to create circle surface to speed up rendering
def make_circle_surface(radius, color):
    surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(surf, color, (radius, radius), radius)
    return surf,surf.get_rect()

# menu widgets
#sliders with their labels
velocity_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((490, 100), (300, 40)), start_value=5, value_range=(0, 20), manager=manager, click_increment=1, 
)
label_velocity_slider = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((800, 100), (200, 40)), text=f"Particle Velocity: {velocity_slider.get_current_value():.0f}", manager=manager, 
)

particle_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((490, 160), (300, 40)), start_value=10, value_range=(1, 5000), manager=manager, click_increment=1, 
    )
label_particle_slider = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((800, 160), (200, 40)), text=f"Number of particle: {particle_slider.get_current_value():.0f}", manager=manager, 
    )

radius_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((490, 160), (300, 40)), start_value=10, value_range=(1, 50), manager=manager, click_increment=1, 
    )
label_radius_slider = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((800, 160), (200, 40)), text=f"Radius of particles: {radius_slider.get_current_value():.0f}", manager=manager, 
    )

mass_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((490, 220), (300, 40)), start_value=5, value_range=(1, 50), manager=manager, click_increment=1, 
    )
label_mass_slider = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((800, 220), (200, 40)), text=f"Particle Mass: {mass_slider.get_current_value():.0f}", manager=manager, 
    )



# buttons
equal_checkbox = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((315, 340), (300, 40)), text="Equal Mass Setup", manager=manager, 
    )
custom_checkbox = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((665, 340), (300, 40)), text="Custom Setup", manager=manager,
)

add_particle_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((490, 280,), (300, 40)), text="Add particle", manager=manager, 
)

start_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((490, 460), (300, 40)), text="Start Simulation", manager=manager, 
    )

# game state
STATE = "menu"
particles=[]

def set_ui_visibility(state):
         # Hide all UI elements first
         equal_checkbox.hide()
         custom_checkbox.hide()
        
         particle_slider.hide()
         label_particle_slider.hide()
        
         mass_slider.hide()
         label_mass_slider.hide()
        
         radius_slider.hide()
         label_radius_slider.hide()
        
         velocity_slider.hide()
         label_velocity_slider.hide()

         add_particle_button.hide()
         start_button.hide()

        # Show elements for the current State
         if state == "menu":
             equal_checkbox.show()
             custom_checkbox.show()  
         elif state == "equal_setup":
             particle_slider.show()
             label_particle_slider.show()
             velocity_slider.show()
             label_velocity_slider.show()
             start_button.show()
         elif state == "custom_setup":
             mass_slider.show()
             label_mass_slider.show()
             radius_slider.show()
             label_radius_slider.show()
             velocity_slider.show()
             label_velocity_slider.show()
             add_particle_button.show()
             start_button.show()



set_ui_visibility(STATE)
# main loop
running = True
while running:

    dt = clock.tick(FPS) * 60 / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if STATE == "menu":
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == equal_checkbox:
                    STATE= "equal_setup"                    
                    set_ui_visibility(STATE) 
                if event.ui_element == custom_checkbox:
                    STATE= "custom_setup"
                    set_ui_visibility(STATE)

        elif STATE == "equal_setup":
            # update slider data
            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == velocity_slider:
                    new_value = velocity_slider.get_current_value()
                    label_velocity_slider.set_text(f"Particle Velocity: {new_value:.0f}")

                if event.ui_element == particle_slider:
                    new_value = particle_slider.get_current_value()
                    label_particle_slider.set_text(f"Number of particle: {new_value:.0f}")
       
            # record button input
            if event.type == pygame_gui.UI_BUTTON_PRESSED:                
                if event.ui_element == start_button:
                    # collect user settings
                    num = int(particle_slider.get_current_value())
                    vel = int(velocity_slider.get_current_value())              

                    # initialise data for simulation
                    wallgrids, gridlist, gridwidth, gridheight = grid(WIDTH, HEIGHT, 10)
                    sidelength=10
                    incr=math.floor((len(gridlist) / num))
                    idx=0
                    collisionQueue=deque()
                    surf,rect = make_circle_surface(5, (0, 255, 0))
                    for i in range(num):
                        position = gridlist[idx].position
                        x, y = revhash_grid(position, gridwidth,10)
                        vx, vy = velocity([WIDTH/2, HEIGHT/2], [x, y])
                        particles += [particle(5, [x, y], [vx, vy], 'green', 5,gridlist[idx])]
                        gridlist[idx].container.add(particles[-1])
                        collisionQueue.append((gridlist[idx],position))  
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
        elif STATE == "custom_setup":
            # update slider data
            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == velocity_slider:
                    new_value = velocity_slider.get_current_value()
                    label_velocity_slider.set_text(f"Particle Velocity: {new_value:.0f}")

                if event.ui_element == radius_slider:
                    new_value = radius_slider.get_current_value()
                    label_radius_slider.set_text(f"Particle Radius: {new_value:.0f}")

                if event.ui_element == mass_slider:
                    new_value = mass_slider.get_current_value()
                    label_mass_slider.set_text(f"Particle Mass: {new_value:.0f}")

            if event.type == pygame_gui.UI_BUTTON_PRESSED:                
                if event.ui_element == add_particle_button:
                    # collect user settings
                    vel = int(velocity_slider.get_current_value())
                    rad = int(radius_slider.get_current_value())
                    mass = int(mass_slider.get_current_value())
                    
                    
                
        
                              
                

        manager.process_events(event)

    # drawing

    
    screen.fill((20, 20, 20))
    manager.update(dt/60)
    manager.draw_ui(screen)

    if STATE == "simulation":
        pygame.display.set_caption("Physics Visualization")
        # handle collisions between particles
        # find all the collision pairs
        collision_matrix = collisonSearch_uniformradius(gridlist, gridwidth, particles_to_index_map,collisionQueue)

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
                velocities[idx] = particles[idx].velocity  # Update velocities array if needed
            particles[idx].update_position(WIDTH, HEIGHT, sidelength, gridwidth, gridlist, dt)
            collisionQueue.append((particles[idx].grid,particles[idx].hash_grid(sidelength, gridwidth)))
            positions[idx] = particles[idx].position  # Update positions array if needed
            rect.center=(positions[idx][0], positions[idx][1])
            screen.blit(surf, rect)
            #pygame.draw.circle(screen, particles[idx].color, tuple(particles[idx].position), particles[idx].radius)            

        # rendering
         # clear screen with black

        
            
    fps = clock.get_fps()
    print(f"Rendering at {fps}fps, {dt}")
    pygame.display.flip()
pygame.quit()