from classes import *

def  collision(particleA, particleB):
       separation=(particleA.position.x-particleB.position.x)*-1
       LowerBound=particleA.radius+particleB.radius

       return  separation <= LowerBound

def momentum_after_collision(particleA, particleB):
    # define masses
    m1 = particleA.mass
    m2 = particleB.mass
    # define initial velocities
    u1 = particleA.velocity.x
    u2 = particleB.velocity.x

    # update velocities of the particles
    particleA.velocity.x = ((m1 - m2)*u1 + 2*m2*u2)/ (m1 + m2)
    particleB.velocity.x = ((m2 - m1)*u2 + 2*m1*u1)/ (m1 + m2)
