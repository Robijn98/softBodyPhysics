import math

class Spring():
    def __init__(self, p1, p2, distance):
        self.p1 = p1
        self.p2 = p2
        self.rest_length = (p2.position - p1.position).length()
        self.spring_damping = 20
        self.spring_force = 500

    def create_spring(self, dt, gravity):
 
        p0 = self.p1.position
        p1 = self.p2.position
        v0 = self.p1.velocity
        v1 = self.p2.velocity

        delta = p1 - p0
        distance = delta.length()
        if distance == 0:
            return

        direction = delta / distance
        required_delta = direction * self.rest_length

        force = self.spring_force * (required_delta - delta)

        self.p1.velocity -= force * dt
        self.p2.velocity += force * dt

        #add gravity
        self.p1.velocity += gravity * dt

        # Damping
        vrel = (v1 - v0).dot(direction)
        damping_factor = math.exp(-self.spring_damping * dt)
        new_vrel = vrel * damping_factor
        vrel_delta = new_vrel - vrel

        damping_force = direction * (vrel_delta / 2.0)

        self.p1.velocity -= damping_force
        self.p2.velocity += damping_force


    