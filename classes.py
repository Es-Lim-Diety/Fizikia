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
        i = self.hash_grid(sidelength, gridheight)
        if self in gridlist[i].container:        
            gridlist[i].container.remove(self)
        

        # simple Euler integration
        self.position += self.velocity * dt
        # keep the particle inside the screen
        self.wall_sep(width,height)
        i = self.hash_grid( sidelength, gridheight)
        gridlist[i].container.add(self)

    def hash_grid(self, side_length, grid_height):
        # x coordinate on grid
        x = self.position[0] // side_length

        # y coordinates on grid
        y = self.position[1] // side_length

        return (int(y * grid_height + x))

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

    def wall_collision(self,width,height,sidelength,gridheight,gridlist):
        # check collision with vertical wall
        middle=[width/2, height/2]
        distance_from_middle_x = abs(self.position[0] - middle[0])
        allowed_distance_from_middle_x = middle[0] - self.radius

        # resolve collision
        if distance_from_middle_x >= allowed_distance_from_middle_x:
            norm_axis = np.array([1,0])
            self.velocity -= 2* np.dot(self.velocity, norm_axis) * norm_axis
        
        # check collision with horizontal wall
        distance_from_middle_y = abs(self.position[1] - middle[1])
        allowed_distance_from_middle_y = middle[1] - self.radius
        # resolve collision
        if distance_from_middle_y >= allowed_distance_from_middle_y:
             norm_axis = np.array([0, 1])
             self.velocity -= 2* np.dot(self.velocity, norm_axis) * norm_axis
        i = self.hash_grid(sidelength, gridheight)
        if self in gridlist[i].container:
            gridlist[i].container.remove(self)
        if self.wall_sep(width,height):
            i = self.hash_grid(sidelength, gridheight)
        gridlist[i].container.add(self)
