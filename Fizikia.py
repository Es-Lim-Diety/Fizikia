# import macros
import math
from collections import deque
import numpy as np
from classes import *
import matplotlib.cm as cm

""" Screen dimensions """
WIDTH, HEIGHT = 1280, 720

def  collision(particleA, particleB):
       separation = np.linalg.norm(particleA.position - particleB.position)
       LowerBound = particleA.radius + particleB.radius    
       return abs(separation) <= LowerBound

def momentum_after_collision(particleA, particleB): # vector decompostition method
     # set up basis vectors
     separation = particleA.position - particleB.position    

     norm = np.linalg.norm(separation)
     #avoid nan errors and division by zero!!
     if  norm != 0 and  not np.isnan(norm):
          norm_axis = separation / norm
     else:
          norm_axis = separation
     
     # transform velocities in the new orthonormal system
     v_an = np.dot(particleA.velocity, norm_axis)* norm_axis
     v_at = particleA.velocity - v_an

     v_bn = np.dot(particleB.velocity, norm_axis)* norm_axis
     v_bt = particleB.velocity - v_bn

    # compute final velocities
     v_an2 = ((particleA.mass - particleB.mass)*v_an + 2 * particleB.mass * v_bn)/ (particleA.mass + particleB.mass)
     v_bn2 = ((particleB.mass - particleA.mass)*v_bn + 2 * particleA.mass * v_an)/ (particleA.mass + particleB.mass)

    # updating final velocities into the particle attributes
     particleA.velocity = v_an2 + v_at
     particleB.velocity = v_bn2 + v_bt

# create data structure for the grid
def init_grid(WIDTH, HEIGHT, side_length):
    grid_width = math.ceil(WIDTH / side_length)
    grid_height = math.ceil(HEIGHT / side_length)
    num_grids = grid_width * grid_height
    gridlist = []
    for i in range(num_grids):
          row = i // grid_width
          col = i % grid_width
          # only include grids fully inside the screen
          if col * side_length < WIDTH and row * side_length < HEIGHT:
               gridlist.append(Node(i))   

    return gridlist, grid_width

# converts grid indices to coordinates of the top-left corner
def rev_hash_grid (grid_indices, grid_width, sidelength):
    y=(grid_indices // grid_width)*sidelength
    x=(grid_indices % grid_width)*sidelength

    positions = np.column_stack((x, y))
    return positions.astype(float)

# initialise particle velocities
def init_velocity(center, positions, speeds):
    distance_vectors = np.array(center) - positions

    magnitudes = np.linalg.norm(distance_vectors, axis=1, keepdims=True)
    direction_vectors = np.divide(distance_vectors, magnitudes, out=np.zeros_like(distance_vectors), where=magnitudes !=0)
    
    if speeds.ndim == 1:
        speeds = speeds.reshape(-1, 1)
    init_velocities = speeds * direction_vectors
    return init_velocities

# converts particle positions into grid indices
def hash_grid(positions, side_length, grid_width):
    coords = np.array(positions) // side_length
    x = coords[:, 0]
    y = coords[:, 1]
    hashes = (y * grid_width) + x

    return hashes.astype(int)

# ensures particles dont get stuck to the walls
def wall_sep(positions, radii, width, height):
    min_x = radii
    max_x = width - radii

    min_y = radii
    max_y = height - radii

    np.clip(positions[:, 0], min_x, max_x, out=positions[:, 0])
    np.clip(positions[:, 1], min_y, max_y, out=positions[:, 1])

# pretty self explanatory innit
def wall_collision(positions, velocities, radii, width, height,flag):
    if flag==False:
        return
    # x axis collision
    middle_x = width / 2
    allowed_distance_x = middle_x - radii
    
    distance_x = np.abs(positions[:, 0] - middle_x)
    collisions_x = distance_x >= allowed_distance_x

    velocities[collisions_x, 0] *= -1

    # y axis collision
    middle_y = height / 2
    allowed_distance_y = middle_y - radii

    distance_y = np.abs(positions[:, 1] - middle_y)
    collisions_y = distance_y >= allowed_distance_y

    velocities[collisions_y, 1] *= -1

# perform integration to find displacements
def update_positions(positions, velocities, dt=0.1):
    positions += (velocities * dt) 

# generalized use case
def collision_search(gridlist, rownum, particle_to_index_map, collisionQueue):
    gridset = set()
    collision_pairs = []
    
    while collisionQueue:
        node, i = collisionQueue.popleft()
        gridset.add(node)
            
        # internal_collisions
        particle_in_cell = list(node.container)
        for p1 in range(len(particle_in_cell)):
            for p2 in range(p1 + 1, len(particle_in_cell)):
                if collision(particle_in_cell[p1], particle_in_cell[p2]):
                    idx1 = particle_to_index_map[id(particle_in_cell[p1])]
                    idx2 = particle_to_index_map[id(particle_in_cell[p2])]
                    collision_pairs.append([idx1, idx2])
                    

        # collisions with neighbors
        for i_offset in [-1, 0, 1]:
            for j_offset in [-1, 0, 1]:
                # skip the center cell
                if i_offset == 0 and j_offset == 0:
                    continue
                # calculate neighbour offset index in 1D
                neighbor = i + (i_offset*rownum) + j_offset
                # boundary checks
                if not (0 <= neighbor < len(gridlist)):# check if neighbour is in the grid bounds
                    continue

                if (i % rownum == 0) and (j_offset == -1):# check for wrap-around on left edge
                    continue

                if ((i+1) % rownum == 0) and j_offset == 1: # check for wrap-around on the right edge
                    continue

                # if all checks pass, check for collisions with neighbouring cell
                neighbor_node = gridlist[neighbor]
                if neighbor_node.container and neighbor_node not in gridset:
                    for p1 in node.container:
                        for p2 in neighbor_node.container:
                            if collision(p1, p2):
                                idx1 = particle_to_index_map[id(p1)]
                                idx2 = particle_to_index_map[id(p2)]
                                collision_pairs.append([idx1, idx2])
    return np.array(collision_pairs)

# use conservation of momentum to calculate final particle velocities             
def resolve_collisions_numpy(matrix, positions, velocities, masses, radii,flag,dt,meanvelocity):
    if flag==True:
        # Get particle properties using indexing
        indices_A = matrix[:, 0]
        indices_B = matrix[:, 1]
        
        pos_A = positions[indices_A]
        pos_B = positions[indices_B]
        
        vel_A = velocities[indices_A]
        vel_B = velocities[indices_B]
        
        mass_A = masses[indices_A]
        mass_B = masses[indices_B]

        rad_A = radii[indices_A].reshape(-1, 1)
        rad_B = radii[indices_B].reshape(-1, 1)

        # --- Vectorize the physics calculations ---   
        # -- Fix overlaps -- 
        # Calculate separation vectors and distances (norms)
        separation_vecs = pos_A - pos_B
        norms = np.linalg.norm(separation_vecs, axis=1, keepdims=True)

        # Avoid division by zero for overlapping particles
        norms[norms == 0] = 1e-6    
        
        # Calculate normalized collision axes (unit vectors)
        norm_axes = separation_vecs / norms

        #calculate overlap
        radii_sum = rad_A + rad_B
        overlap = radii_sum - norms

        # only correct if overlap is positive
        overlap_mask = (overlap > 0)

        # calculate the correction
        correction_vecs = norm_axes * (overlap * 0.5) * overlap_mask

        # apply the correction
        np.add.at(positions, indices_A, correction_vecs)
        np.add.at(positions, indices_B, -correction_vecs)

        # -- Velocity resolution --
        
        # Project initial velocities onto the collision axes
        # This is the component of velocity along the line of collision    
        separation_vecs = pos_A - pos_B
        norms = np.linalg.norm(separation_vecs, axis=1, keepdims=True)
        norms[norms == 0] = 1e-6    
        norm_axes = separation_vecs / norms

        v_an_scalar = np.sum(vel_A * norm_axes, axis=1, keepdims=True)
        v_bn_scalar = np.sum(vel_B * norm_axes, axis=1, keepdims=True)
            
        # Apply the 1D elastic collision formula to the normal components
        m_sum = mass_A + mass_B
        new_v_an_scalar = ((mass_A - mass_B) * v_an_scalar + 2 * mass_B * v_bn_scalar) / m_sum
        new_v_bn_scalar = ((mass_B - mass_A) * v_bn_scalar + 2 * mass_A * v_an_scalar) / m_sum

        # calculate the change in velocity
        d_v_an_scalar = new_v_an_scalar - v_an_scalar
        d_v_bn_scalar = new_v_bn_scalar - v_bn_scalar

        # convert the scalar change to a vector in 2D
        d_v_A = d_v_an_scalar * norm_axes
        d_v_B = d_v_bn_scalar * norm_axes
        
        # Update the original arrays with the new velocities
        np.add.at(velocities, indices_A, d_v_A)
        np.add.at(velocities, indices_B, d_v_B)

        vel_A = velocities[indices_A]
        vel_B = velocities[indices_B]
        # adjust velocities to maintain mean velocity
        rms_current = np.sqrt(np.mean(np.sum(velocities**2, axis=1)))

        scaling_factor = meanvelocity / (rms_current + 1e-6)
        velocities *= scaling_factor
        
    #update positions after resolving collisions or if no collisions    
    positions += (velocities * dt)     

      
"""uniform radius version optimization"""
def collisonSearch_uniformradius(gridlist, gridwidth,particles,collisionQueue):
    """
    Collision Search with Domain-Specific Optimizations

    Assumptions:
    ------------
    1. Single-Particle Grid Occupancy
       - Each grid cell is approximately one particle diameter wide.
       - Statistically, at most one particle occupies a given grid at any frame.
       - Reduces neighbor collision checks while maintaining accuracy.

    2. Neighbor Collisions via Representative Particle
       - Only the first (representative) particle in each neighboring cell is checked.
       - Given typical velocities and small dt, particles are almost always
         captured in adjacent grids before skipping multiple grids.
       - Empirical testing shows very few missed collisions under expected conditions.

    3. Internal Grid Collisions
       - For grids with multiple particles, the first particle is used as reference.
       - Other particles cannot bypass the first without entering a neighbor grid first.
       - Captures most meaningful collisions with minimal pairwise checks.

    4. Limitations / Edge Cases
       - Assumptions are valid for expected simulation parameters (particle spacing, velocities, dt).
       - High initial velocities or unusually dense grids could violate assumptions.
       - A general-purpose collision method exists for handling such edge cases.

    Summary:
    --------
    These design choices are performance-oriented, domain-specific optimizations.
    They balance computational efficiency and collision accuracy for typical simulation conditions.
    Empirical validation supports them as safe and effective for high-performance CPU simulations.
    """
    rownum=gridwidth
    gridset=set()
    collision_pairs = []
    while collisionQueue:
        # pop the first grid in the queue and its position in list
        grid,i = collisionQueue.popleft()
        # add the grid to the set of visited grids
        gridset.add(grid)

        if grid.container:
            # check for collisions with neighboring grids
            # only run check if the grid is not empty
            idx=particles[id(next(iter(grid.container)))]
            #check internal collisions first
            if len(grid.container)>1:
                particlea=next(iter(grid.container))
                for particle in grid.container:
                    if particlea!=particle:
                        idx2=particles[id(particle)]
                        collision_pairs.append([idx, idx2])
        
            if i + 1 < len(gridlist) and (i + 1) % rownum != 0 and gridlist[i + 1].container:
                if gridlist[i + 1] not in gridset:
                    if collision(next(iter(gridlist[i + 1].container)), next(iter(grid.container))):
                        idx2=particles[id(next(iter(gridlist[i + 1].container)))]
                        collision_pairs.append([idx, idx2])

            if i - 1 >= 0 and i % rownum != 0 and gridlist[i - 1].container:
                if gridlist[i - 1] not in gridset:
                    if collision(next(iter(gridlist[i - 1].container)), next(iter(grid.container))):
                        idx2=particles[id(next(iter(gridlist[i - 1].container)))]
                        collision_pairs.append([idx, idx2])

            if i + rownum < len(gridlist) and gridlist[i+ rownum].container:#up
                if gridlist[i + rownum] not in gridset:
                    if collision(next(iter(gridlist[i + rownum].container)), next(iter(grid.container))):
                        idx2=particles[id(next(iter(gridlist[i + rownum].container)))]
                        collision_pairs.append([idx, idx2])

            if i + rownum - 1< len(gridlist) and i  % rownum != 0 and gridlist[i + rownum - 1].container:#NW
                if gridlist[i + rownum - 1] not in gridset:
                    if collision(next(iter(gridlist[i+ rownum - 1].container)), next(iter(grid.container))):
                        idx2=particles[id(next(iter(gridlist[i + rownum - 1].container)))]
                        collision_pairs.append([idx, idx2])

            if i + rownum + 1< len(gridlist) and (i + 1) % rownum != 0 and gridlist[i + rownum + 1].container:#NE
                if gridlist[i + rownum+1] not in gridset:
                    if collision(next(iter(gridlist[i+ rownum + 1].container)), next(iter(grid.container))):
                        idx2=particles[id(next(iter(gridlist[i + rownum + 1].container)))]
                        collision_pairs.append([idx, idx2])

            if i - rownum >= 0 and gridlist[i - rownum].container:#down
                if gridlist[i - rownum] not in gridset:
                    if collision(next(iter(gridlist[i - rownum].container)), next(iter(grid.container))):
                        idx2=particles[id(next(iter(gridlist[i - rownum].container)))]
                        collision_pairs.append([idx, idx2])

            if i - rownum + 1 >= 0 and i  % rownum != 0 and gridlist[i - rownum + 1 ].container:#SW
                if gridlist[i - rownum + 1] not in gridset:
                    if collision(next(iter(gridlist[i - rownum + 1].container)), next(iter(grid.container))):
                        idx2=particles[id(next(iter(gridlist[i - rownum + 1].container)))]
                        collision_pairs.append([idx, idx2])

            if i - rownum - 1 >= 0 and (i + 1) % rownum != 0 and gridlist[i - rownum - 1].container:#SE
                if gridlist[i - rownum - 1] not in gridset:
                    if collision(next(iter(gridlist[i - rownum - 1].container)), next(iter(grid.container))):
                        idx2=particles[id(next(iter(gridlist[i - rownum - 1].container)))]
                        collision_pairs.append([idx, idx2])
    return np.array(collision_pairs)                    

def update_particle_colors_by_speed(velocities, max_speed=20.0):
    # 1. Calculate speeds (vectorized)
    # equivalent to: sqrt(vx^2 + vy^2)
    speeds = np.linalg.norm(velocities, axis=1)

    # 2. Normalize speeds to 0.0 - 1.0 range
    # Any speed >= max_speed will be 1.0 (brightest color)
    normalized_speeds = np.clip(speeds / max_speed, 0.0, 1.0)

    # 3. Apply a colormap (e.g., 'inferno', 'plasma', 'viridis')
    # cm.inferno gives RGBA floats (0.0-1.0)
    rgba_colors = cm.inferno(normalized_speeds)

    # 4. Convert to RGB integers (0-255) for Pygame
    # Drop the Alpha channel ([:, :3]) and multiply by 255
    rgb_colors = (rgba_colors[:, :3] * 255).astype(int)

    return rgb_colors
