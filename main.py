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
        dt = 1 / 60
        restitution = 0.5
        friction = 0.8

        # only loop each unordered pair once
    # ----- ball–environment collisions (edge‑based) -----
        mass_ball = 1.0
        mass_edge = 2.0
        for ball in self.balls:
            
            collision_with_environment(ball)
            
            #prevent self collision
            for obj in self.objects:
                if ball in obj:
                    continue  

                # loop every edge 
                for i in range(len(obj)):
                    A = obj[i]
                    B = obj[(i+1) % len(obj)]
                    AB = B.position - A.position

                    # project center onto AB:
                    t = (ball.position - A.position).dot(AB)
                    denom = AB.length_squared() + 1e-6
                    t /= denom
                    t = max(0.0, min(1.0, t))

                    closest = A.position + AB * t
                    diff    = ball.position - closest
                    dist    = diff.length()
                    penetration = radius - dist

                    if penetration <= 0:
                        continue  # no overlap with this edge

                    # collision normal
                    if dist == 0:
                        # fallback: take a perp to AB
                        n = AB.normalize().rotate(90)
                    else:
                        n = diff.normalize()

                    # relative velocity at the contact point
                    v_edge  = A.velocity * (1-t) + B.velocity * t
                    rel_vel = ball.velocity - v_edge
                    vn = rel_vel.dot(n)

                    print(f"vn: {vn}, penetration: {penetration}, t: {t}, A: {A.position}, B: {B.position}")
                    # only apply impulse if closing
                    if vn < 0:
                        inv_m_edge = ((1-t)**2 + t**2) / mass_edge
                        inv_m = mass_ball + inv_m_edge

                        # normal impulse magnitude
                        numerator = -(1 + restitution) * vn
                        denominator = (1/ 2) + (i + t) ** 2 * (1/6)
                        j_mag = numerator / denominator
                        
                        j = n * j_mag

                        # apply to ball and edge endpoints
                        ball.velocity += j / mass_ball
                        A.velocity    -= j * (1-t)  /mass_edge
                        B.velocity    -= j *    t  /mass_edge

                    if penetration > 0.01:
                        # apply penetration correction
                        n = n.rotate(90)
                        correction = n * (penetration / inv_m)
                        ball.position += correction / mass_ball
                        A.position    -= correction * (1-t) / mass_edge
                        B.position    -= correction *    t  / mass_edge



def collision_with_environment(ball):
    radius = 5
    # Floor
    if ball.position.y > SCREEN_HEIGHT - radius:
        ball.position.y = SCREEN_HEIGHT - radius

        if ball.velocity.y > 0:
            ball.velocity.y *= -0.5 

        if abs(ball.velocity.y) < 1:
            ball.velocity.y = 0

        ball.velocity.x *= 0.9
        if abs(ball.velocity.x) < 0.5:
            ball.velocity.x = 0

    # Ceiling
    if ball.position.y < radius:
        ball.position.y = radius
        ball.velocity.y *= -0.8

    # Right wall
    if ball.position.x > SCREEN_WIDTH - radius:
        ball.position.x = SCREEN_WIDTH - radius
        ball.velocity.x *= -0.8
        if abs(ball.velocity.x) < 2:
            ball.velocity.x = 0

    # Left wall
    if ball.position.x < radius:
        ball.position.x = radius
        ball.velocity.x *= -0.8
        if abs(ball.velocity.x) < 2:
            ball.velocity.x = 0
            

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

def ball_on_ball_collision(ball1, edge=[]):
    radius = 5
    print(f"ball1: {ball1.position}, edge: {[b.position for b in edge]}")
    # Check which ball from edge is closest to ball1
    ball2 = edge[0]
    closest_distance = (ball1.position - ball2.position).length()
    for ball in edge:
        distance = (ball1.position - ball.position).length()
        if distance < closest_distance:
            closest_distance = distance
            ball2 = ball

    delta = ball2.position - ball1.position
    distance = delta.length()
    min_distance = radius * 2
    if distance == 0:
        return


    if distance < min_distance:
        # Collision resolution
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


    print("balls collided succesfully")


def create_formations():
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