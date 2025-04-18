from pygame.math import Vector2
from spring import distance_constraint
import math 
from settings import *

class Ball():
    def __init__(self, position):
        self.position = Vector2(position)
        self.velocity = Vector2(0, 0)
        self.colour=(255,0,0)


class SoftBodyObj():
    def __init__(self, name, vertices):
        self.name = name
        self.vertices = vertices
        


def create_formations():
    create_square( start_pos=Vector2(100, 100), size=30)
    create_triangle(start_pos=Vector2(300, 300), size=30)
    #create_square( start_pos=Vector2(500, 500), size=30)



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
    
    objects.append(SoftBodyObj("square", square))

    #check how many balls already exist in the engine

    
    #apply constraints
    rest_length = size  
    d = distance_constraint(balls[ball_count],balls[ball_count + 1], rest_length)
    constraints.append(d)
    d = distance_constraint(balls[ball_count + 1],balls[ball_count + 2], rest_length)
    constraints.append(d)
    d = distance_constraint(balls[ball_count + 2],balls[ball_count + 3], rest_length)
    constraints.append(d)
    d = distance_constraint(balls[ball_count + 3],balls[ball_count], rest_length)
    constraints.append(d)
    d = distance_constraint(balls[ball_count],balls[ball_count + 2], rest_length)
    constraints.append(d)
    d = distance_constraint(balls[ball_count + 1],balls[ball_count + 3], rest_length)
    constraints.append(d)



def create_triangle(start_pos = Vector2(100, 100), size = 30):
    triangle = []

    #create balls in a triangle formation
    balls.append(Ball(position=start_pos))
    balls.append(Ball(position=start_pos + Vector2(-size, -size))) 
    balls.append(Ball(position=start_pos + Vector2(size, -size)))
    
    ball_count = len(balls) - 3
    
    for i in range(3):
        triangle.append(balls[i + ball_count])
    
    objects.append(SoftBodyObj("triangle", triangle))


    #apply constraints
    rest_length = size
    d = distance_constraint(balls[ball_count],balls[ball_count + 1], rest_length)
    constraints.append(d)
    d = distance_constraint(balls[ball_count + 1],balls[ball_count + 2], rest_length)
    constraints.append(d)
    d = distance_constraint(balls[ball_count + 2],balls[ball_count], rest_length)
    constraints.append(d)

