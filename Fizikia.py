import math
from collections import deque
import numpy as np
from classes import *

# import macros
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

"""support functions for rendering"""
# create data structure for the grid
def grid(WIDTH, HEIGHT, side_length):
    grid_width = math.ceil(WIDTH / side_length)
    grid_height = math.ceil(HEIGHT / side_length)
    num_grids = grid_width * grid_height
    wallgrids=set()
    gridlist = []
    for i in range(num_grids):
          row = i // grid_width
          col = i % grid_width
          # only include grids fully inside the screen
          if col * side_length < WIDTH and row * side_length < HEIGHT:
               gridlist.append(Node(i))
          if col==0 or col==grid_width-1 or row==0 or row==grid_height-1:
               wallgrids.add(gridlist[i])     

    return wallgrids,gridlist, grid_width, grid_height



def revhash_grid (grid_position, grid_width,sidelength):
    y=(grid_position // grid_width)*sidelength
    x=(grid_position % grid_width)*sidelength
    return (float(x),float(y))


# initialise particle velocities
def velocity(center, p, speed=5):#
    distance_vector = np.array(center) - np.array(p)
    magnitude = np.linalg.norm(distance_vector)
    if magnitude == 0:
        return np.array([0, 0])
    direction = distance_vector / magnitude
    init_velocity = speed * direction
    return init_velocity



# generalized use case
def collision_search(gridlist, rownum, particle_to_index_map):
    queue = deque([(node, i) for i, node in enumerate(gridlist) if len(node.container)])
    gridset = set()
    collision_pairs = []
    
    while queue:
        node, i = queue.popleft()
        gridset.add(node)        
        if not node.container:
            continue
            
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

                # if all checks pass, perform collision logic
                neighbor_node = gridlist[neighbor]
                if neighbor_node.container and neighbor_node not in gridset:
                    for p1 in node.container:
                        for p2 in neighbor_node.container:
                            if collision(p1, p2):
                                idx1 = particle_to_index_map[id(p1)]
                                idx2 = particle_to_index_map[id(p2)]
                                collision_pairs.append([idx1, idx2])
    return np.array(collision_pairs)

                
def resolve_collisions_numpy(matrix, positions, velocities, masses):
    # 1. Get particle properties using fancy indexing
    indices_A = matrix[:, 0]
    indices_B = matrix[:, 1]
    
    pos_A = positions[indices_A]
    pos_B = positions[indices_B]
    
    vel_A = velocities[indices_A]
    vel_B = velocities[indices_B]
    
    mass_A = masses[indices_A]
    mass_B = masses[indices_B]

    # --- 2. Vectorize the physics calculations ---
    seperation_array = np.zeros_like(positions)  # same shape as positions
    
    # Calculate separation vectors and distances (norms)
    separation_vecs = pos_A - pos_B
    norms = np.linalg.norm(separation_vecs, axis=1, keepdims=True)
    # Update separation arrays to resolve sticky collisions
    np.add.at(seperation_array, indices_A, separation_vecs / 2)
    np.add.at(seperation_array, indices_B, -separation_vecs / 2)

    
    
    # Avoid division by zero for overlapping particles
    norms[norms == 0] = 1e-6 
    
    # Calculate normalized collision axes (unit vectors)
    norm_axes = separation_vecs / norms
    
    # Project initial velocities onto the collision axes
    # This is the component of velocity along the line of collision
    v_an_scalar = np.sum(vel_A * norm_axes, axis=1, keepdims=True)
    v_bn_scalar = np.sum(vel_B * norm_axes, axis=1, keepdims=True)
    
    # Calculate the tangential velocities (perpendicular to the collision)
    v_at = vel_A - v_an_scalar * norm_axes
    v_bt = vel_B - v_bn_scalar * norm_axes
    
    # Apply the 1D elastic collision formula to the normal components
    m_sum = mass_A + mass_B
    new_v_an_scalar = ((mass_A - mass_B) * v_an_scalar + 2 * mass_B * v_bn_scalar) / m_sum
    new_v_bn_scalar = ((mass_B - mass_A) * v_bn_scalar + 2 * mass_A * v_an_scalar) / m_sum
    
    # Reconstruct the final velocity vectors
    new_vel_A = new_v_an_scalar * norm_axes + v_at
    new_vel_B = new_v_bn_scalar * norm_axes + v_bt
    
    # --- 3. Update the original arrays with the new velocities ---
    velocities[indices_A] = new_vel_A
    velocities[indices_B] = new_vel_B
    
    #uncomment to use separation in position update function
    #return seperation_array    
    



"""uniform radius version optimization"""
def gridbfs_uniformradius(gridlist, gridwidth,particles):
    #finds grids with particles and adds them to the queue
    queue = deque([(node, i) for i, node in enumerate(gridlist) if node.container])

    rownum=gridwidth
    gridset=set()
    collision_pairs = []
    while queue:
        # pop the first grid in the queue and its position in list
        grid,i = queue.popleft()
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