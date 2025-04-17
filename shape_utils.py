from engine import Engine
from pygame.math import Vector2
from spring import distance_constraint
import math 


class ball():
    def __init__(self, position):
        self.position = Vector2(position)
        self.velocity = Vector2(0, 0)
        self.colour=(255,0,0)


def create_formations(engine):

    create_triangle(engine, start_pos=Vector2(300, 300), size=30)
    create_square(engine, start_pos=Vector2(100, 100), size=30)
    create_square(engine, start_pos=Vector2(200, 200), size=30)
    #create_triangle(engine, start_pos=Vector2(400, 400), size=30)
    #create_circle(engine, start_pos=Vector2(500, 500), size=30, vertices=6)



def create_square(engine, start_pos = Vector2(100, 100), size = 30):
    square = []

    #create balls in a square formation
    engine.balls.append(ball(position=start_pos))
    engine.balls.append(ball(position=start_pos + Vector2(size, 0))) 
    engine.balls.append(ball(position=start_pos + Vector2(size, size)))
    engine.balls.append(ball(position=start_pos + Vector2(0, size)))
    for i in range(3):
        square.append(engine.balls[i])
    engine.objects.append(square)

    #check how many balls already exist in the engine
    ball_count = len(engine.balls) - 4

    
    #apply constraints
    rest_length = size  
    d = distance_constraint(engine.balls[ball_count], engine.balls[ball_count + 1], rest_length)
    engine.constraints.append(d)
    d = distance_constraint(engine.balls[ball_count + 1], engine.balls[ball_count + 2], rest_length)
    engine.constraints.append(d)
    d = distance_constraint(engine.balls[ball_count + 2], engine.balls[ball_count + 3], rest_length)
    engine.constraints.append(d)
    d = distance_constraint(engine.balls[ball_count + 3], engine.balls[ball_count], rest_length)
    engine.constraints.append(d)
    d = distance_constraint(engine.balls[ball_count], engine.balls[ball_count + 2], rest_length)
    engine.constraints.append(d)
    d = distance_constraint(engine.balls[ball_count + 1], engine.balls[ball_count + 3], rest_length)
    engine.constraints.append(d)

def create_triangle(engine, start_pos = Vector2(100, 100), size = 30):
    triangle = []

    #create balls in a triangle formation
    engine.balls.append(ball(position=start_pos))
    engine.balls.append(ball(position=start_pos + Vector2(-size, -size))) 
    engine.balls.append(ball(position=start_pos + Vector2(size, -size)))
    
    for i in range(3):
        triangle.append(engine.balls[i])
    
    engine.objects.append(triangle)

    ball_count = len(engine.balls) - 3

    #apply constraints
    rest_length = size
    d = distance_constraint(engine.balls[ball_count], engine.balls[ball_count + 1], rest_length)
    engine.constraints.append(d)
    d = distance_constraint(engine.balls[ball_count + 1], engine.balls[ball_count + 2], rest_length)
    engine.constraints.append(d)
    d = distance_constraint(engine.balls[ball_count + 2], engine.balls[ball_count], rest_length)
    engine.constraints.append(d)

def create_circle(engine, start_pos = Vector2(100, 100), size = 30, vertices = 10):
    circle = []

    #create balls in a circle formation
    for i in range(vertices):
        angle = i * (360 / vertices)
        x = start_pos.x + size * math.cos(math.radians(angle))
        y = start_pos.y + size * math.sin(math.radians(angle))
        engine.balls.append(ball(position=Vector2(x, y)))
        circle.append(engine.balls[i])
    

    #create one ball in the center of the circle
    engine.balls.append(ball(position=start_pos))
    
    circle.append(engine.balls[vertices])

    engine.objects.append(circle)

    ball_count = len(engine.balls) - (vertices + 1)

    #apply constraints
    rest_length = size
    for i in range(vertices):
        d = distance_constraint(engine.balls[ball_count + i], engine.balls[ball_count + (i + 1) % vertices], rest_length)
        engine.constraints.append(d)
        d = distance_constraint(engine.balls[ball_count + i], engine.balls[ball_count + vertices], rest_length)
        engine.constraints.append(d)


