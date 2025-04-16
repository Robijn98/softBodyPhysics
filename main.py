import pygame
from pygame.math import Vector2
import math
import random
import sys

pygame.init()

# set up main variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
fps = 0
frame = pygame.time.Clock()

# set up the screen
pygame.display.set_caption("2D soft body simulation")
pygame.mouse.set_visible(True)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

pygame.display.update()


class ball():
    def __init__(self, position):
        self.position = Vector2(position)
        self.velocity = Vector2(0, 0)
        self.colour=(255,0,0)
        


class distance_constraint():
    def __init__(self, p1, p2, distance):
        self.p1 = p1
        self.p2 = p2
        self.rest_length = 100
        self.spring_damping = 200
        self.spring_force = 5000

    def constrain(self, dt, gravity):
        
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


    
class Engine():
    def __init__(self, gravity, radius=5):
        self.radius = radius
        self.balls = []
        self.constraints = []
        self.objects = []
        self.gravity = Vector2(gravity)
        self.selected = None
        self.mouse_pos = Vector2(0, 0)
        self.prev_mouse_pos = Vector2(0, 0)

    def update(self, dt):
        for p in self.balls:
            p.force = Vector2(0, 0)

        for c in self.constraints:
            c.constrain(dt, self.gravity)

        for p in self.balls:
            p.position += p.velocity * dt


        self.resolve_collision()

    def resolve_collision(self):
        radius = 5
        for i, ball1 in enumerate(self.balls):
            for j, ball2 in enumerate(self.balls[i+1:], i+1):
                delta = ball2.position - ball1.position
                distance = delta.length()
                min_distance = radius * 2
               
                if distance < min_distance:

                    normal = delta.normalize()
                    overlap = (min_distance - distance) * 0.5

                    ball1.position -= normal * overlap
                    ball2.position += normal * overlap

                    relative_velocity = ball2.velocity - ball1.velocity
                    normal_velocity = relative_velocity.dot(normal)
                    tangent_velocity = relative_velocity - normal * normal_velocity

                    resitution = 0.5
                    ball1.velocity += normal * normal_velocity * resitution
                    ball2.velocity -= normal * normal_velocity * resitution

                    friction_coefficient = 0.8
                    ball1.velocity += tangent_velocity * friction_coefficient * 0.5
                    ball2.velocity -= tangent_velocity * friction_coefficient * 0.5

            #collision with environemnt
            for obj in self.objects:
                if ball1 not in obj:
                    if point_in_object(ball1.position, obj):
                        #move the ball outside the object
                        #find the side of the object that is closest to the ball
                        closest_side = []
                        for point in obj:
                            vector = ball1.position - point.position
                            distance = vector.length()
                            #find the two closest points
                            if len(closest_side) < 2:
                                closest_side.append(point)
                            else:
                                if distance < (ball1.position - closest_side[0].position).length():
                                    closest_side[0] = point
                                elif distance < (ball1.position - closest_side[1].position).length():
                                    closest_side[1] = point
                        
                        
                            



                        



            # Floor
            if ball1.position.y > SCREEN_HEIGHT - self.radius:
                ball1.position.y = SCREEN_HEIGHT - self.radius

                if ball1.velocity.y > 0:
                    ball1.velocity.y *= -0.5 

                if abs(ball1.velocity.y) < 1:
                    ball1.velocity.y = 0

                ball1.velocity.x *= 0.9
                if abs(ball1.velocity.x) < 0.5:
                    ball1.velocity.x = 0
           
            # Ceiling
            if ball1.position.y < self.radius:
                ball1.position.y = self.radius
                ball1.velocity.y *= -0.8

            # Right wall
            if ball1.position.x > SCREEN_WIDTH - self.radius:
                ball1.position.x = SCREEN_WIDTH - self.radius
                ball1.velocity.x *= -0.8
                if abs(ball1.velocity.x) < 2:
                    ball1.velocity.x = 0

            # Left wall
            if ball1.position.x < self.radius:
                ball1.position.x = self.radius
                ball1.velocity.x *= -0.8
                if abs(ball1.velocity.x) < 2:
                    ball1.velocity.x = 0
            

def point_in_object(point, object):
    inside = False
    x, y = point

    for i in range(len(object)):
        j = (i + 1) % len(object)
        xi, yi = object[i].position
        xj, yj = object[j].position

        intersect = ((yi > y) != (yj > y)) and \
                    (x < (xj - xi) * (y - yi) / (yj - yi + 1e-6) + xi)
        if intersect:
            inside = not inside

    return inside



def create_formations():
    #\square formation
    square = []
    start_pos = Vector2(300, 300)
    engine.balls.append(ball(position=start_pos))
    engine.balls.append(ball(position=start_pos + Vector2(30, 0))) 
    engine.balls.append(ball(position=start_pos + Vector2(30, 30)))
    engine.balls.append(ball(position=start_pos + Vector2(0, 30)))
    for i in range(4):
        square.append(engine.balls[i])
    engine.objects.append(square)
    print(engine.balls[0])
    
    #apply constraints
    rest_length = 30  
    d = distance_constraint(engine.balls[0], engine.balls[1], rest_length)
    engine.constraints.append(d)
    d = distance_constraint(engine.balls[1], engine.balls[2], rest_length)
    engine.constraints.append(d)
    d = distance_constraint(engine.balls[2], engine.balls[3], rest_length)
    engine.constraints.append(d)
    d = distance_constraint(engine.balls[3], engine.balls[0], rest_length)
    engine.constraints.append(d)
    d = distance_constraint(engine.balls[0], engine.balls[2], rest_length)
    engine.constraints.append(d)
    d = distance_constraint(engine.balls[1], engine.balls[3], rest_length)
    engine.constraints.append(d)

    #create balls in a triangle formation
    triangle = []
    start_pos = Vector2(600, 600)
    engine.balls.append(ball(position=start_pos))
    engine.balls.append(ball(position=start_pos + Vector2(-50, -100))) 
    engine.balls.append(ball(position=start_pos + Vector2(50, -100)))

    for i in range(4, 7):
        triangle.append(engine.balls[i])
    engine.objects.append(triangle)

    #triangle formation
    #apply constraints
    rest_length = 30  
    d = distance_constraint(engine.balls[4], engine.balls[5], rest_length)
    engine.constraints.append(d)
    d = distance_constraint(engine.balls[5], engine.balls[6], rest_length)
    engine.constraints.append(d)
    d = distance_constraint(engine.balls[6], engine.balls[4], rest_length)
    engine.constraints.append(d)


#creating engine and ball
engine = Engine(gravity=(0, 500))
create_formations()

run = True

while run:
    dt = clock.tick(fps) / 1000 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = Vector2(pygame.mouse.get_pos())
            for b in engine.balls:
                if(b.position - mouse_pos).length() < 50:
                    engine.selected = b
                    engine.prev_mouse_pos = mouse_pos
                    b.velocity = Vector2(0, 0)
                    b.colour = (0, 255, 0)
                    break
        elif event.type == pygame.MOUSEBUTTONUP:
            if engine.selected:
                current_mouse_pos = Vector2(pygame.mouse.get_pos())
                velocity = (current_mouse_pos - engine.prev_mouse_pos) * 2
                engine.selected.velocity = velocity
                engine.selected = None
                engine.prev_mouse_pos = Vector2(0, 0)
                for b in engine.objects[0]:
                    b.colour = (255, 0, 0)
                for b in engine.objects[1]:
                    b.colour = (0, 0, 255)



    if engine.selected:
        mouse_pos = Vector2(pygame.mouse.get_pos())
        engine.selected.position = mouse_pos

    engine.update(dt)
    screen.fill((0, 0, 0))

    for b in engine.balls:
        pygame.draw.circle(screen,b.colour, b.position, 5)
        pygame.draw.circle(screen, b.colour, b.position, 5, 1)
    
    for constraint in engine.constraints:
        pygame.draw.line(screen, (255, 255, 255), constraint.p1.position, constraint.p2.position, 1)
    
    pygame.display.update()



pygame.quit()
sys.exit()