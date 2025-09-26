import numpy as np

class Node:
    def __init__(self,position):
        self.position = position
        self.width=100
        self.height=100
        self.container=[]


class particle:
    """class for objects in simulation"""
    def __init__(self, mass, position, velocity, acceleration, color):
        self.mass = mass
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.acceleration = np.array(acceleration)
        self.radius = mass
        self.color = color
    
    """integrate acceleration to calculate velocity"""
    def update_velocity(self):
        self.velocity += self.acceleration * dt

    """integrate velocity to calculate position"""
    def update_position(self,width,height):
        self.update_velocity()
        self.position += self.velocity
        if self.position[0] > width:
            self.position[0] = width - self.radius
        if self.position[1] > height:
            self.position[1] = height - self.radius
        if self.position[0] <0:
            self.position[0] = 0 + self.radius
        if self.position[1] < 0:
            self.position[1] = 0 + self.radius

    def wall_collision(self, middle):
        # check collision with vertical wall
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