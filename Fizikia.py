import math
from collections import deque
from classes import *

# import macros
""" Screen dimensions """
WIDTH, HEIGHT = 800, 600

def  collision(particleA, particleB):
       separation_vector = particleA.position - particleB.position
       separation = np.linalg.norm(separation_vector)
       LowerBound = particleA.radius + particleB.radius
       

       return  abs(separation) <= LowerBound

def momentum_after_collision(particleA, particleB):
     # vector decompostition method

     # set up basis vectors
     separation = particleA.position - particleB.position

    # separate the particles
     particleA.position += separation/2
     particleB.position -= separation/2

     norm = np.linalg.norm(separation)
     if not norm == 0:
          norm_axis = separation / norm
     else:
          norm_axis = separation
     tan_axis = np.array([-norm_axis[1], norm_axis[0]])
     
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

     gridlist = []
     for i in range(num_grids):
          row = i // grid_width
          col = i % grid_width
          # only include grids fully inside the screen
          if col * side_length < WIDTH and row * side_length < HEIGHT:
               gridlist.append(Node(i))

     return gridlist, grid_width, grid_height

def hash_grid (particle, side_length, grid_height):
     # x coordinate on grid
     x = particle.position[0] // side_length
     
     # y coordinates on grid
     y = particle.position[1] // side_length
     
     return (y*grid_height + x)

#helper function for collision search
def collisions(gridA,gridB):
    for g in gridA:# loop through all particles in the grid
        for j in gridB:# loop through all particles in the neighboring grid
            if collision(j,g):
                momentum_after_collision(j,g)# resolve collision

# generalized use case
def collision_search(gridlist, gridwidth):

    queue = deque([(node, i) for i, node in enumerate(gridlist) if len(node.container)])

    rownum=gridwidth
    gridset=set()

    while queue:

        grid,i = queue.popleft()
        gridset.add(grid)
        # check for collisions with neighboring grids
        # only run check if the grid is not empty
        if len(grid.container):

            # solve collisions within grid
            for i in range(len(grid.container)):
                for j in range(i,len(grid.container)):
                    if not grid.container[i] == grid.container[j]:
                        if collision(grid.container[i], grid.container[j]):
                            momentum_after_collision(grid.container[i], grid.container[j])

            if i + 1 < len(gridlist) and (i + 1) % rownum != 0 and len(gridlist[i + 1].container):#check the grid to the east
                if gridlist[i + 1] not in gridset:# to avoid double collision resolution
                    collisions(grid.conainer, gridlist[i + 1].container)
                                

            if i - 1 >= 0 and i  % rownum != 0 and len(gridlist[i - 1].container):#check the grid to the west
                if gridlist[i - 1] not in gridset:# to avoid double collision resolution
                    collisions(grid.container, gridlist[i - 1].container)
                                    

            if i + rownum < len(gridlist) and len(gridlist[i+ rownum].container):#check the grid to the south
                if gridlist[i + rownum] not in gridset:# to avoid double collision resolution
                    collisions(grid.container, gridlist[i + rownum].container)


            if i + rownum - 1< len(gridlist) and i  % rownum != 0 and len(gridlist[i + rownum - 1].container):#check the grid to the SW
                if gridlist[i + rownum - 1] not in gridset:# to avoid double collision resolution
                    collisions(grid.container, gridlist[i + rownum - 1].container)
                                

            if i + rownum + 1< len(gridlist) and (i + 1) % rownum != 0 and len(gridlist[i + rownum + 1].container):#check the grid to the SE
                if gridlist[i + rownum+1] not in gridset:# to avoid double collision resolution
                    collisions(grid.container, gridlist[i + rownum + 1].container)

            if i - rownum >= 0 and len(gridlist[i - rownum].container):#check the grid to the north
                if gridlist[i - rownum] not in gridset:# to avoid double collision resolution
                    collisions(grid.container, gridlist[i - rownum].container)

            if i - rownum + 1 >= 0 and i  % rownum != 0 and len(gridlist[i - rownum + 1].container):#check the grid to the NE
                if gridlist[i - rownum + 1] not in gridset:# to avoid double collision resolution
                    collisions(grid.container, gridlist[i - rownum + 1].container)

            if i - rownum - 1 >= 0 and (i + 1) % rownum != 0 and len(gridlist[i - rownum - 1].container):#check the grid to the SW
                if gridlist[i - rownum - 1] not in gridset:# to avoid double collision resolution
                    collisions(grid.container, gridlist[i - rownum - 1].container)



"""uniform radius version optimization"""
def gridbfs_uniformradius(gridlist, gridwidth):
    queue = deque([(node, i) for i, node in enumerate(gridlist) if node.container])

    rownum=gridwidth
    gridset=set()

    while queue:

        grid,i = queue.popleft()
        gridset.add(grid)

        if grid.container:
            if i + 1 < len(gridlist) and (i + 1) % rownum != 0 and gridlist[i + 1].container:
                if gridlist[i + 1] not in gridset:
                    if collision(gridlist[i + 1].container, grid.container):
                        momentum_after_collision(gridlist[i + 1].container, grid.container)

            if i - 1 >= 0 and i % rownum != 0 and gridlist[i - 1].container:
                if gridlist[i - 1] not in gridset:
                    if collision(gridlist[i - 1].container, grid.container):
                        momentum_after_collision(grid.container, gridlist[i - 1].container)

            if i + rownum < len(gridlist) and gridlist[i+ rownum].container:#up
                if gridlist[i + rownum] not in gridset:
                    if collision(gridlist[i + rownum].container, grid.container):
                       momentum_after_collision(grid.container,gridlist[i + rownum].container)

            if i + rownum - 1< len(gridlist) and i  % rownum != 0 and gridlist[i + rownum - 1].container:#NW
                if gridlist[i + rownum - 1] not in gridset:
                    if collision(gridlist[i+ rownum - 1].container, grid.container):
                        momentum_after_collision(grid.container, gridlist[i + rownum - 1].container)

            if i + rownum + 1< len(gridlist) and (i + 1) % rownum != 0 and gridlist[i + rownum + 1].container:#NE
                if gridlist[i + rownum+1] not in gridset:
                    if collision(gridlist[i+ rownum + 1].container, grid.container):
                        momentum_after_collision(grid.container, gridlist[i + rownum + 1].container)

            if i - rownum >= 0 and gridlist[i - rownum].container:#down
                if gridlist[i - rownum] not in gridset:
                    if collision(gridlist[i - rownum].container, grid.container):
                        momentum_after_collision(grid.container, gridlist[i - rownum].container)

            if i - rownum + 1 >= 0 and i  % rownum != 0 and gridlist[i - rownum + 1 ].container:#SW
                if gridlist[i - rownum + 1] not in gridset:
                    if collision(gridlist[i - rownum + 1].container, grid.container):
                        momentum_after_collision(grid.container, gridlist[i - rownum + 1].container)

            if i - rownum - 1 >= 0 and (i + 1) % rownum != 0 and gridlist[i - rownum - 1].container:#SE
                if gridlist[i - rownum - 1] not in gridset:
                    if collision(gridlist[i - rownum - 1].container, grid.container):
                        momentum_after_collision(grid.container, gridlist[i - rownum - 1].container)




#def hash_color(highest_mass, particles):
