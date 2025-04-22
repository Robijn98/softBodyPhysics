from settings import *

class Joint:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def connect(self):
        # Connect the two points
        middle = (self.p2.position + self.p1.position) / 2
        self.p1.position = middle  
        self.p2.position = middle

        average_velocity = (self.p1.velocity + self.p2.velocity) / 2    
        self.p1.velocity = average_velocity
        self.p2.velocity = average_velocity



def create_joint(p1, p2):
    joint = Joint(p1, p2)
    joints.append(joint)

