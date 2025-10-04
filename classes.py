import numpy as np

from Fizikia import*


class Node:
    def __init__(self,position):
        self.position = position
        self.container=set()


class particle:
    """class for objects in simulation"""
    def __init__(self, mass, position, velocity, color,radius):
        self.mass = mass
        self.position = np.array(position)
        self.velocity = np.array(velocity)        
        self.radius = radius if radius is not None else mass
        self.color = color
    
    """integrate velocity to calculate position"""
    def update_position(self,width,height,sidelength,gridheight,gridlist,dt=0.1):
        # remove particle from its inital grid container
        i = self.hash_grid(sidelength, gridheight)
        if self in gridlist[i].container:        
            gridlist[i].container.remove(self)       

        # simple Euler integration
        self.position += self.velocity * dt

        # keep the particle inside the screen
        self.wall_sep(width,height)

        # hash program into the correct grid
        i = self.hash_grid( sidelength, gridheight)
        gridlist[i].container.add(self)

    # hashing particles into grid nodes by position
    def hash_grid(self, side_length, grid_width):
        coords = self.position // side_length
        return (int(coords[1] * grid_width + coords[0]))

    # separate the particle from the wall
    def wall_sep(self, width, height):
        flag=False
        if self.position[0] > width:
            flag=True
            self.position[0] = width - self.radius
        if self.position[1] > height:
            flag=True
            self.position[1] = height - self.radius
        if self.position[0] < 0:
            flag=True
            self.position[0] = 0 + self.radius
        if self.position[1] < 0:
            flag=True
            self.position[1] = 0 + self.radius
        return flag

    def wall_collision(self,width,height):
        # compute box center
        middle=[width/2, height/2]

        # check and resolve collision with vertical wall
        distance_from_middle_x = abs(self.position[0] - middle[0])
        allowed_distance_from_middle_x = middle[0] - self.radius
        if distance_from_middle_x >= allowed_distance_from_middle_x:
            self.wall_sep(width, height)
            norm_axis = np.array([1, 0])
            self.velocity -= 2* np.dot(self.velocity, norm_axis) * norm_axis
        
        # check and resolve collision with horizontal wall
        distance_from_middle_y = abs(self.position[1] - middle[1])
        allowed_distance_from_middle_y = middle[1] - self.radius
        if distance_from_middle_y >= allowed_distance_from_middle_y:
             self.wall_sep(width, height)
             norm_axis = np.array([0, 1])
             self.velocity -= 2* np.dot(self.velocity, norm_axis) * norm_axis       