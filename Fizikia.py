from classes import *

# import macros
""" Screen dimensions """
WIDTH, HEIGHT = 800, 600

def  collision(particleA, particleB):
       separation_vector = particleA.position - particleB.position
       separation = np.linalg.norm(separation_vector)
       LowerBound = particleA.radius + particleB.radius

       return  separation <= LowerBound

def momentum_after_collision(particleA, particleB):
     # vector decompostition method
     # change cordiate system so that x is the axis perpendicular to the 
     # collision and y is the axis tangent to the collision

     # set up basis vectors
     separation = particleA.position - particleB.position
     norm = np.linalg.norm(separation)
     if not norm == 0:
          norm_axis = separation / norm
     else:
          norm_axis = separation
     tan_axis = np.array([-norm_axis[1], norm_axis[0]])
     
     # resolve velocities in the basis vectors
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
def grid(WIDTH, HEIGHT, side_length):
     return [WIDTH/side_length][HEIGHT/side_length]

def hash (particle, side_length, grid_rows):
     # x coordinate on grid
     x = particle.position[0] // side_length
     
     # y coordinates on grid
     y = particle.position[1] // side_length
     
     return (x*grid_rows + y)

