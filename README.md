Fizikia
Fizikia is a Python-based 2D particle simulation and visualization tool built with Pygame and pygame_gui. It allows users to configure, simulate, and visualize the motion and collisions of particles in a customizable environment.

Features
Interactive GUI: Easily set the number, and mass of particles using sliders and buttons.
Real-Time Simulation: Particles move and interact according to simple physics rules, including elastic collisions and wall bounces.
Collision Handling: Particle-particle and particle-wall collisions are detected and resolved with momentum conservation.
Customizable Parameters: Users can toggle between equal or varied particle properties.
Visualization: Particles are rendered in real time, with color coding for easy distinction.
Requirements
Python 3.8+
Pygame
pygame_gui
Install dependencies with:
pip install pygame pygame_gui

Usage
Run the Simulation:
python render.py

Configure Particles:
Use the sliders to set the number, and mass of particles.
Toggle the "Mode" button to switch between equal and varied particle properties.
Click "Start Simulation" to begin.

Simulation:

Watch particles move, collide, and bounce within the window.
The simulation updates in real time, showing the effects of your chosen parameters.
File Structure
render.py – Main application script with GUI and simulation loop.
Fizikia.py – Physics and collision logic for particles and grids.
classes.py – Definitions for the particle class and other supporting classes.

How It Works
Initialization: The GUI is set up with sliders and buttons for user input.
Menu State: Users configure particle properties.
Simulation State: Particles are created and simulated based on user settings. The simulation loop handles movement, collision detection, and rendering.
Physics: Collisions are resolved using momentum conservation, and particles bounce off the window boundaries.
Customization
You can extend or modify the simulation by editing Fizikia.py and classes.py to add new physics behaviors, visualization features, or user controls.

License
This project is open source and available under the MIT License.

Acknowledgments
Pygame
pygame_gui
