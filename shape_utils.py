from pygame.math import Vector2
from spring import Spring
import math 
from settings import *
from connections import create_joint

class Ball():
    def __init__(self, position, static=False):
        self.position = Vector2(position)
        self.velocity = Vector2(0, 0)
        self.colour=(255,0,0)
        self.rest_position = None
        self.static = static


class SoftBodyObj():
    def __init__(self, name, vertices, static=False):
        self.name = name
        self.vertices = vertices
        self.static = static
        
    def initialize_softBody(self):
        center = Vector2(0, 0)
        for vertex in self.vertices:
            center += vertex.position
        center /= len(self.vertices)
        for vertex in self.vertices:
            vertex.rest_position = vertex.position - center


def create_formations():
    create_square( start_pos=Vector2(100, 100), size=30)
    create_triangle(start_pos=Vector2(200, 200), size=60)
    create_square(start_pos=Vector2(300, 300), size=50)
    #create_wheel(start_pos=Vector2(300, 300), size=30, num_balls=10)
    #create_wheel(start_pos=Vector2(300, 300), size=60, num_balls=10)
    # create_wheel(start_pos=Vector2(300, 300), size=50, num_balls=10)
    # create_joint(objects[0].vertices[10], objects[1].vertices[10])
    create_platform(start_pos=Vector2(400, 400), size=50)
    create_platform(start_pos=Vector2(500, 500), size=50)
    
    
    # #create small squares
    # x, y = 10, 10
    # size = 20
    # spacing = 40  # distance between squares
    # squares_per_row = SCREEN_WIDTH // spacing

    # for i in range(20):
    #     if y > SCREEN_HEIGHT - size:
    #         break

    #     create_square(start_pos=Vector2(x, y), size=size)

    #     x += spacing
    #     if x > SCREEN_WIDTH - size:
    #         x = 30
    #         y += spacing



def create_square(start_pos = Vector2(100, 100), size = 30):
    square = []

    #create balls in a square formation
    balls.append(Ball(position=start_pos))
    balls.append(Ball(position=start_pos + Vector2(size, 0))) 
    balls.append(Ball(position=start_pos + Vector2(size, size)))
    balls.append(Ball(position=start_pos + Vector2(0, size)))

    ball_count = len(balls) - 4

    
    for i in range(4):
        square.append(balls[i + ball_count])
    
    softbody = SoftBodyObj("square", square)
    softbody.initialize_softBody()
    objects.append(softbody)

    #check how many balls already exist in the engine

    
    #apply spring_points
    rest_length = size  
    d = Spring(balls[ball_count],balls[ball_count + 1], rest_length)
    spring_points.append(d)
    d = Spring(balls[ball_count + 1],balls[ball_count + 2], rest_length)
    spring_points.append(d)
    d = Spring(balls[ball_count + 2],balls[ball_count + 3], rest_length)
    spring_points.append(d)
    d = Spring(balls[ball_count + 3],balls[ball_count], rest_length)
    spring_points.append(d)
    d = Spring(balls[ball_count],balls[ball_count + 2], rest_length)
    spring_points.append(d)
    d = Spring(balls[ball_count + 1],balls[ball_count + 3], rest_length)
    spring_points.append(d)

def create_triangle(start_pos = Vector2(100, 100), size = 30):
    triangle = []

    #create balls in a triangle formation
    balls.append(Ball(position=start_pos))
    balls.append(Ball(position=start_pos + Vector2(-size, -size))) 
    balls.append(Ball(position=start_pos + Vector2(size, -size)))
    
    ball_count = len(balls) - 3
    
    for i in range(3):
        triangle.append(balls[i + ball_count])
    
    softbody = SoftBodyObj("triangle", triangle)
    softbody.initialize_softBody()
    objects.append(softbody)


    #apply spring_points
    rest_length = size
    d = Spring(balls[ball_count],balls[ball_count + 1], rest_length)
    spring_points.append(d)
    d = Spring(balls[ball_count + 1],balls[ball_count + 2], rest_length)
    spring_points.append(d)
    d = Spring(balls[ball_count + 2],balls[ball_count], rest_length)
    spring_points.append(d)

def create_wheel(start_pos = Vector2(100, 100), size = 30, num_balls = 10):
    wheel = []

    #create balls in a circle formation
    for i in range(num_balls):
        angle = (2 * math.pi / num_balls) * i
        x = start_pos.x + size * math.cos(angle)
        y = start_pos.y + size * math.sin(angle)
        balls.append(Ball(position=Vector2(x, y)))

    balls.append(Ball(position=start_pos)) # add center ball

    ball_count = len(balls) - num_balls - 1 
    
    for i in range(num_balls):
        wheel.append(balls[i + ball_count])
    wheel.append(balls[ball_count + num_balls]) # add center ball to wheel
    
    softbody = SoftBodyObj("wheel", wheel)
    softbody.initialize_softBody()
    objects.append(softbody)

    #apply spring_points
    rest_length = size / num_balls
    for i in range(num_balls):
        d = Spring(balls[ball_count + i], balls[ball_count + (i + 1) % num_balls], rest_length)
        spring_points.append(d)
       #constraint to center ball
        d = Spring(balls[ball_count + i], balls[ball_count + num_balls], rest_length)
        spring_points.append(d)

def create_circle(start_pos = Vector2(100, 100), size = 30, num_balls = 10):
    circle = []

    #create balls in a circle formation
    for i in range(num_balls):
        angle = (2 * math.pi / num_balls) * i
        x = start_pos.x + size * math.cos(angle)
        y = start_pos.y + size * math.sin(angle)
        balls.append(Ball(position=Vector2(x, y)))


    ball_count = len(balls) - num_balls 
    
    for i in range(num_balls):
        circle.append(balls[i + ball_count])
    
    softbody = SoftBodyObj("circle", circle)
    softbody.initialize_softBody()
    objects.append(softbody)

    #apply spring_points
    rest_length = size / num_balls
    for i in range(num_balls):
        d = Spring(balls[ball_count + i], balls[ball_count + (i + 1) % num_balls], rest_length)
        spring_points.append(d)

def create_platform(start_pos = Vector2(100, 100), size = 30):
    platform = []

    #create balls in a square formation
    balls.append(Ball(position=start_pos, static=True))
    balls.append(Ball(position=start_pos + Vector2(size*3, 0), static=True)) 
    balls.append(Ball(position=start_pos + Vector2(size*3, size), static=True))
    balls.append(Ball(position=start_pos + Vector2(0, size), static=True))

    ball_count = len(balls) - 4

    
    for i in range(4):
        platform.append(balls[i + ball_count])
    
    softbody = SoftBodyObj("platform", platform, static=True)
    softbody.initialize_softBody()
    objects.append(softbody)

    #check how many balls already exist in the engine

    
    #apply spring_points
    rest_length = size  
    d = Spring(balls[ball_count],balls[ball_count + 1], rest_length, spring_gravity=False)
    spring_points.append(d)
    d = Spring(balls[ball_count + 1],balls[ball_count + 2], rest_length, spring_gravity=False)
    spring_points.append(d)
    d = Spring(balls[ball_count + 2],balls[ball_count + 3], rest_length, spring_gravity=False)
    spring_points.append(d)
    d = Spring(balls[ball_count + 3],balls[ball_count], rest_length, spring_gravity=False)
    spring_points.append(d)
    d = Spring(balls[ball_count],balls[ball_count + 2], rest_length, spring_gravity=False)
    spring_points.append(d)
    d = Spring(balls[ball_count + 1],balls[ball_count + 3], rest_length, spring_gravity=False)
    spring_points.append(d)
