import pygame
import pygame_gui
import time

from Fizikia import*
from classes import*

"""Initialize Pygame"""
pygame.init()

# --- setup ---
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle Setup")
clock = pygame.time.Clock()
FPS = 60
# UI Manager
manager = pygame_gui.UIManager((WIDTH, HEIGHT))
current_selected_color = (255, 0, 0)
STATE = "menu"


# -- menu widgets --
#sliders with their labels
velocity_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((490, 100), (300, 40)), start_value=5, value_range=(0, 20), manager=manager, click_increment=1, 
)
label_velocity_slider = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((800, 100), (200, 40)), text=f"Particle Velocity: {velocity_slider.get_current_value():.0f}", manager=manager, 
)

particle_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((490, 160), (300, 40)), start_value=10, value_range=(1, 20000), manager=manager, click_increment=1, 
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
    relative_rect=pygame.Rect((490, 280), (300, 40)), start_value=5, value_range=(1, 50), manager=manager, click_increment=1, 
    )
label_mass_slider = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((800, 280), (200, 40)), text=f"Particle Mass: {mass_slider.get_current_value():.0f}", manager=manager, 
    )

color_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((490, 220), (300, 40)), start_value=0, value_range=(0, 360), manager=manager, click_increment=1
)
label_color_slider = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((800, 220), (200, 40)), text=f"Particle color: {color_slider.get_current_value():.0f}", manager=manager, 
)
color_preview_box = pygame_gui.elements.UIPanel(relative_rect= pygame.Rect((1100, 220), (40, 40)), manager=manager)
color_preview_box.background_colour = pygame.Color(current_selected_color)
color_preview_box.rebuild()

# buttons
equal_checkbox = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((315, 340), (300, 40)), text="Equal Mass Setup", manager=manager, 
    )
custom_checkbox = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((665, 340), (300, 40)), text="Custom Setup", manager=manager,
)

add_particle_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((490, 340,), (300, 40)), text="Add particle", manager=manager, 
)

start_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((490, 460), (300, 40)), text="Start Simulation", manager=manager, 
    )


# function to set visibility of widgets
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

         color_slider.hide()
         label_color_slider.hide()
         color_preview_box.hide()


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
             color_slider.show()
             label_color_slider.show()
             color_preview_box.show()
         elif state == "custom_setup":
             mass_slider.show()
             label_mass_slider.show()
             radius_slider.show()
             label_radius_slider.show()
             velocity_slider.show()
             label_velocity_slider.show()
             color_slider.show()
             label_color_slider.show()
             add_particle_button.show()
             start_button.show()
             color_preview_box.show()

# function to initialise numpy arrays
def initialize_particles(init_grid_indices, color_list, gridlist):
    # initialise all particle object and simulation ready NumPy arrays from lists of particle data
    global particles, positions, velocities, masses, radii, particles_to_index_map, STATE, collisionQueue
      # create particle objects from the data lists
    for i in range(positions.shape[0]):
        p = particle(
            radius = radii[i],
            position=positions[i],
            velocity=velocities[i],
            color=color_list[i],
            mass=masses[i]
        )
        particles.append(p)
        particles_to_index_map[id(p)] = i
        # populate nodes with particle data
        gridlist[int(init_grid_indices[i])].container.add(p)
        # populate queue with active nodes
        collisionQueue.append((gridlist[int(init_grid_indices[i])], int(init_grid_indices[i])))

    # start the simulation
    STATE = "simulation"

# --- simulation ---

particles=[]
particles_to_index_map={}
#use deque to avoid recreating the queue in the search algos
collisionQueue=deque()
initial_masses = []
initial_radii = []
initial_colors = []
initial_speeds = []
positions=None
velocities=None
masses=None
radii=None
init_grid_indices=None
set_ui_visibility(STATE)
    # main loop
def main():
    global particles, initial_masses, initial_radii, initial_colors, initial_speeds, positions, velocities, masses, radii, WIDTH, HEIGHT, screen, clock, manager, current_selected_color, STATE, velocity_slider, label_velocity_slider, particle_slider, label_particle_slider, radius_slider, label_radius_slider, mass_slider, label_mass_slider, color_slider, label_color_slider, color_preview_box, equal_checkbox, custom_checkbox, add_particle_button, start_button 
    running = True
    heat = True
    while running:

        dt = clock.tick(FPS) / 1000.0
        # handle user input
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
                        colors = []
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

                    if event.ui_element == color_slider:
                        color_value = int(color_slider.get_current_value())
                        temp_color = pygame.Color(0)
                        temp_color.hsla = (color_value, 100, 50, 100)                    
                        current_selected_color = (temp_color.r, temp_color.g, temp_color.b)

                        label_color_slider.set_text(f"Particle Color: {color_value}")
                        color_preview_box.background_colour = pygame.Color(current_selected_color)
                        color_preview_box.rebuild()
        
                # record button input
                if event.type == pygame_gui.UI_BUTTON_PRESSED:                
                    if event.ui_element == start_button:
                        # collect user settings
                        num = int(particle_slider.get_current_value())
                        vel_magnitude = int(velocity_slider.get_current_value())              

                        # initialise grid for simulation
                        side_length = 10
                        gridlist, gridwidth = init_grid(WIDTH, HEIGHT, side_length)                    
                        #surf,rect = make_circle_surface(2, (0, 255, 0))

                        # populate NumPy arrays                    
                        init_grid_indices = np.linspace(0, len(gridlist) - 1, num=num)         
                        positions = rev_hash_grid(init_grid_indices, gridwidth, side_length)
                        masses = np.full(num, 1.0).reshape(-1, 1)
                        radii = np.full(num, 2.0)
                        speeds = np.full(num, vel_magnitude)
                        velocities = init_velocity([WIDTH/2, HEIGHT/2], positions, speeds) 
                        
                                               
                        colors = update_particle_colors_by_speed(velocities, max_speed=20.0)                    

                        # build particles and start simulation
                        if positions.size:
                            initialize_particles(
                                init_grid_indices,
                                colors, 
                                gridlist
                            )  
                                                    
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
                    
                    if event.ui_element == color_slider:
                        color_value = int(color_slider.get_current_value())
                        temp_color = pygame.Color(0)
                        temp_color.hsla = (color_value, 100, 50, 100)                   
                        current_selected_color = (temp_color.r, temp_color.g, temp_color.b)

                        label_color_slider.set_text(f"Particle Color: {color_value}")
                        color_preview_box.background_colour = pygame.Color(current_selected_color)
                        color_preview_box.rebuild()
                        
                if event.type == pygame_gui.UI_BUTTON_PRESSED:                
                    if event.ui_element == add_particle_button:
                        # collect user settings
                        vel_magnitude = int(velocity_slider.get_current_value())
                        rad = int(radius_slider.get_current_value())
                        mass = int(mass_slider.get_current_value())
                        color = current_selected_color

                        # append data to the lists
                        initial_masses.append(mass)
                        initial_radii.append(rad)
                        initial_colors.append(color)
                        initial_speeds.append(vel_magnitude)
                        

                    if event.ui_element == start_button:
                        # create a grid
                        side_length = 100
                        gridlist, gridwidth = init_grid(WIDTH, HEIGHT, side_length)                    
                        
                        # populate NumPy arrays
                        masses = np.array(initial_masses).reshape(-1, 1)
                        radii = np.array(initial_radii)
                        init_grid_indices = np.linspace(0, len(gridlist) - 1, num=len(initial_masses))                  
                        positions = rev_hash_grid(init_grid_indices, gridwidth, side_length)
                        speeds = np.array(initial_speeds)
                        velocities = init_velocity([WIDTH/2, HEIGHT/2], positions, speeds)
                        heat=False  
                        
                        # initialise particles and start simulation
                        if positions.size:
                            initialize_particles(
                                init_grid_indices,
                                initial_colors,
                                gridlist)

            manager.process_events(event)
        
        screen.fill((20, 20, 20))
        manager.update(dt/60)
        manager.draw_ui(screen)

        if STATE == "simulation":
            pygame.display.set_caption("Physics Visualization")
            # --- calculations ---        
            old_node_ids = hash_grid(positions, side_length, gridwidth)

            # handle collisions
            startsearch=time.time()
            collision_matrix = collision_search(gridlist, gridwidth, particles_to_index_map, collisionQueue)
            endsearch=time.time()
            #profiling prints
            print(f"Collision search time: {endsearch-startsearch:.4f} seconds")
            flag=False
            # determine time step based on max speed
            max_speed = np.mean(np.linalg.norm(velocities, axis=1))
            dt_calc = 1 / (1 + max_speed/2 )

            #profiling prints
            print(f"max speed: {max_speed:.4f}")
            print(f"dt for collision resolution: {dt_calc:.6f} seconds")

            if collision_matrix.size > 0:
                #skip collision math if no collisions detected and only update positions
                flag=True
            startcalc=time.time()    
            resolve_collisions_numpy(collision_matrix, positions, velocities, masses, radii,flag,dt_calc)                  
            wall_collision(positions, velocities, radii, WIDTH, HEIGHT,flag)
            endcalc=time.time()
            #profiling prints
            print(f"Collision resolution time: {endcalc-startcalc:.4f} seconds")              
                
                

            #update positions        
            
            wall_sep(positions, radii, WIDTH, HEIGHT)
            new_node_ids = hash_grid(positions, side_length, gridwidth)        

            # calculate new colors
            new_colors = update_particle_colors_by_speed(velocities, max_speed=50.0)


            # --- render ---
            screen.fill("black")
            # assign values to particles and draw them
            startren=time.time()
            for i, p in enumerate(particles):            
                p.color=new_colors[i]
                p.position=positions[i]    

                if old_node_ids[i] != new_node_ids[i]:
                    old_node = gridlist[old_node_ids[i]]
                    new_node = gridlist[new_node_ids[i]]

                    
                    old_node.container.remove(p)                
                    new_node.container.add(p)

                    collisionQueue.append((new_node, new_node_ids[i]))
                    
                pygame.draw.circle(screen, p.color, tuple(p.position), p.radius) 
            endren=time.time()
            print(f"Render time: {endren-startren:.4f} seconds")
        fps = clock.get_fps()
        print(f"Rendering at {fps:.0f}fps")
        pygame.display.flip()
    pygame.quit()

main()