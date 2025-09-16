import csv

from classes import *

def  collision(particleA, particleB):
       separation=particleA.position.x-particleB.position.x
       LowerBound=particleA.radius+particleB.radius

       return separation <= LowerBound

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

fps=60

numberOfLoops=(60*fps) #decide later

a=particle(69,vector(0,0),vector(1,0),vector(0,0))
print(a.velocity.x)

b=particle(420,vector(5,0),vector(-1,0),vector(0,0))

for i in range(numberOfLoops):
    if collision(a,b):
        momentum_after_collision(a,b)
        print('collided')

    a.update_position(fps)
    b.update_position(fps)

    with open("particleCollider.csv","a") as f:
        writer = csv.writer(f)
        writer.writerow([a.position.x,b.position.x])





