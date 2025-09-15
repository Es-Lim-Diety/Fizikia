def  collision(particleA, particleB):
        return particleA.position == particleB.position

def momentum_after_collision(particleA, particleB):
    # define masses
    m1 = particleA.mass
    m2 = particleB.mass
    # define initial velocities
    u1 = particleA.velocity.x
    u2 = particleB.velocity.x

    # update velocities of the particles
    particleA.velocity = ((m1 - m2)*u1 + 2*m2*u2)/ (m1 + m2)
    particleB.velocity = ((m2 - m1)*u2 + 2*m1*u1)/ (m1 + m2)

# this is the instance method
def update_position(self, velocity, dt):
    self.position += velocity * dt

