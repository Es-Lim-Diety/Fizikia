import math
from collections import deque
import numpy as np
from classes import *

# import macros
""" Screen dimensions """
WIDTH, HEIGHT = 1280, 720

def  collision(particleA, particleB):
       separation_vector = particleA.position - particleB.position
       separation = np.linalg.norm(separation_vector)
       LowerBound = particleA.radius + particleB.radius
       

       return  abs(separation) <= LowerBound

def momentum_after_collision(particleA, particleB):
     # vector decompostition method

     # set up basis vectors
     separation = particleA.position - particleB.position

    # assign separation vectors to particles for position update math
     particleA.seperation = separation/2
     particleB.seperation = -(separation/2)

    
     norm = np.linalg.norm(separation)
     #avoid nan errors and division by zero!!
     if  norm != 0 and  not np.isnan(norm):
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
    return(float(x),float(y))


def velocity(centerx,centery,px,py):
    dx=centerx-px
    dy=centery-py
    magnitude=np.sqrt((dx*dx)+(dy*dy))
    speed=5
    vx=(dx/magnitude)*speed
    vy=(dy/magnitude)*speed
    return (vx,vy)

#helper function for collision search
def collisions(gridA,gridB):
    if len(gridA)>1 and len(gridB)>1:
        for g in gridA:# loop through all particles in the grid
            for j in gridB:# loop through all particles in the neighboring grid
                if collision(j,g):
                    momentum_after_collision(j,g)# resolve collision
    elif len(gridA)==1 and len(gridB)>1:
        particleA=next(iter(gridA))
        for j in gridB:
            if collision(j,particleA):
                momentum_after_collision(j,particleA)
    elif len(gridB)==1 and len(gridA)>1:
        particleB=next(iter(gridB))
        for i in gridA:
            if collision(i,particleB):
                momentum_after_collision(i,particleB)
    else:# both grids have only one particle
        particleA=next(iter(gridA))
        particleB=next(iter(gridB))
        if collision(particleA,particleB):
            momentum_after_collision(particleA,particleB)                                        

def internal_collisions(grid):
    for i in grid:
        for j in grid:
            if not i == j:
                if collision(i,j):
                    momentum_after_collision(i, j)
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
            if len(grid.container)>1:
                internal_collisions(grid.container)

            if i + 1 < len(gridlist) and (i + 1) % rownum != 0 and len(gridlist[i + 1].container):#check the grid to the east
                if gridlist[i + 1] not in gridset:# to avoid double collision resolution
                    collisions(grid.container, gridlist[i + 1].container)
                                

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
    #finds grids with particles and adds them to the queue
    queue = deque([(node, i) for i, node in enumerate(gridlist) if node.container])

    rownum=gridwidth
    gridset=set()

    while queue:
        # pop the first grid in the queue and its position in list
        grid,i = queue.popleft()
        # add the grid to the set of visited grids
        gridset.add(grid)

        if grid.container:
            # check for collisions with neighboring grids
            # only run check if the grid is not empty
            
            #check internal collisions first
            if len(grid.container)>1:
                particlea=next(iter(grid.container))
                for particle in grid.container:
                    if particlea!=particle:
                        momentum_after_collision(particlea,particle)
        
            if i + 1 < len(gridlist) and (i + 1) % rownum != 0 and gridlist[i + 1].container:
                if gridlist[i + 1] not in gridset:
                    if collision(next(iter(gridlist[i + 1].container)), next(iter(grid.container))):
                        momentum_after_collision(next(iter(gridlist[i + 1].container)), next(iter(grid.container)))

            if i - 1 >= 0 and i % rownum != 0 and gridlist[i - 1].container:
                if gridlist[i - 1] not in gridset:
                    if collision(next(iter(gridlist[i - 1].container)), next(iter(grid.container))):
                        momentum_after_collision(next(iter(grid.container)), next(iter(gridlist[i - 1].container)))

            if i + rownum < len(gridlist) and gridlist[i+ rownum].container:#up
                if gridlist[i + rownum] not in gridset:
                    if collision(next(iter(gridlist[i + rownum].container)), next(iter(grid.container))):
                       momentum_after_collision(next(iter(grid.container)), next(iter(gridlist[i + rownum].container)))

            if i + rownum - 1< len(gridlist) and i  % rownum != 0 and gridlist[i + rownum - 1].container:#NW
                if gridlist[i + rownum - 1] not in gridset:
                    if collision(next(iter(gridlist[i+ rownum - 1].container)), next(iter(grid.container))):
                        momentum_after_collision(next(iter(grid.container)), next(iter(gridlist[i + rownum - 1].container)))

            if i + rownum + 1< len(gridlist) and (i + 1) % rownum != 0 and gridlist[i + rownum + 1].container:#NE
                if gridlist[i + rownum+1] not in gridset:
                    if collision(next(iter(gridlist[i+ rownum + 1].container)), next(iter(grid.container))):
                        momentum_after_collision(next(iter(grid.container)), next(iter(gridlist[i + rownum + 1].container)))

            if i - rownum >= 0 and gridlist[i - rownum].container:#down
                if gridlist[i - rownum] not in gridset:
                    if collision(next(iter(gridlist[i - rownum].container)), next(iter(grid.container))):
                        momentum_after_collision(next(iter(grid.container)), next(iter(gridlist[i - rownum].container)))

            if i - rownum + 1 >= 0 and i  % rownum != 0 and gridlist[i - rownum + 1 ].container:#SW
                if gridlist[i - rownum + 1] not in gridset:
                    if collision(next(iter(gridlist[i - rownum + 1].container)), next(iter(grid.container))):
                        momentum_after_collision(next(iter(grid.container)), next(iter(gridlist[i - rownum + 1].container)))

            if i - rownum - 1 >= 0 and (i + 1) % rownum != 0 and gridlist[i - rownum - 1].container:#SE
                if gridlist[i - rownum - 1] not in gridset:
                    if collision(next(iter(gridlist[i - rownum - 1].container)), next(iter(grid.container))):
                        momentum_after_collision(next(iter(grid.container)), next(iter(gridlist[i - rownum - 1].container)))