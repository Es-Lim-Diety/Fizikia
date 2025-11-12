import numpy as np
from Fizikia import*

class Node:
    def __init__(self,position):
        self.position = position
        self.container = set()

class particle:
    """class for objects in simulation"""
    def __init__(self, mass, position, velocity, color,radius,grid=None):
        self.mass = mass
        self.position = np.array(position)
        self.velocity = np.array(velocity)        
        self.radius = radius
        self.color = color
        

    
        

        