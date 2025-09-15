class vector:
    """ class for vector variables"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

class particle:
    """class for objects in simulation"""
    def __init__(self, mass,position, velocity,acceleration):
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
