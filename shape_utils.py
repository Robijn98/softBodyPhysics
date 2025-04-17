from engine import Engine
from pygame.math import Vector2
from spring import distance_constraint
print("shape_utils.py was imported")



class ball():
    def __init__(self, position):
        self.position = Vector2(position)
        self.velocity = Vector2(0, 0)
        self.colour=(255,0,0)


def create_formations(engine):
    #square formation
    
    square = []
    start_pos = Vector2(300, 300)
    engine.balls.append(ball(position=start_pos))
    engine.balls.append(ball(position=start_pos + Vector2(30, 0))) 
    engine.balls.append(ball(position=start_pos + Vector2(30, 30)))
    #engine.balls.append(ball(position=start_pos + Vector2(0, 30)))
    for i in range(3):
        square.append(engine.balls[i])
    engine.objects.append(square)
    print(engine.balls[0])
    
    #apply constraints
    rest_length = 30  
    d = distance_constraint(engine.balls[0], engine.balls[1], rest_length)
    engine.constraints.append(d)
    d = distance_constraint(engine.balls[1], engine.balls[2], rest_length)
    engine.constraints.append(d)
    d = distance_constraint(engine.balls[0], engine.balls[2], rest_length)
    engine.constraints.append(d)
    # d = distance_constraint(engine.balls[3], engine.balls[0], rest_length)
    # engine.constraints.append(d)
    # d = distance_constraint(engine.balls[0], engine.balls[2], rest_length)
    # engine.constraints.append(d)
    # d = distance_constraint(engine.balls[1], engine.balls[3], rest_length)
    # engine.constraints.append(d)

    #create balls in a triangle formation
    triangle = []
    start_pos = Vector2(600, 600)
    engine.balls.append(ball(position=start_pos))
    engine.balls.append(ball(position=start_pos + Vector2(-50, -100))) 
    engine.balls.append(ball(position=start_pos + Vector2(50, -100)))
    

    for i in range(3, 5):
        triangle.append(engine.balls[i])
    engine.objects.append(triangle)

    #triangle formation
    #apply constraints
    rest_length = 30  
    d = distance_constraint(engine.balls[3], engine.balls[4], rest_length)
    engine.constraints.append(d)
    d = distance_constraint(engine.balls[4], engine.balls[5], rest_length)
    engine.constraints.append(d)
    d = distance_constraint(engine.balls[5], engine.balls[3], rest_length)
    engine.constraints.append(d)