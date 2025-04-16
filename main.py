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
        self.K = 100
        self.damping = 0.1

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

        spring_force = 100 
        force = spring_force * (required_delta - delta)

        self.p1.velocity -= force * dt
        self.p2.velocity += force * dt

        #add gravity
        self.p1.velocity += gravity * dt
        self.p2.velocity += gravity * dt

        # Damping
        vrel = (v1 - v0).dot(direction)
        spring_damping = 5 
        damping_factor = math.exp(-spring_damping * dt)
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
        self.gravity = Vector2(gravity)
        self.selected = None
        self.mouse_pos = Vector2(0, 0)
        self.prev_mouse_pos = Vector2(0, 0)

    def update(self, dt):
        for p in self.balls:
            p.force = Vector2(0, 0)
        #constraints

        for c in self.constraints:
            c.constrain(dt, self.gravity)

        for p in self.balls:
            p.position += p.velocity * dt

            #collisions
            # Floor
            if p.position.y > SCREEN_HEIGHT - self.radius:
                p.position.y = SCREEN_HEIGHT - self.radius

                if p.velocity.y > 0:
                    p.velocity.y *= -0.5 

                if abs(p.velocity.y) < 1:
                    p.velocity.y = 0

                p.velocity.x *= 0.9
                if abs(p.velocity.x) < 0.5:
                    p.velocity.x = 0
           
            # Ceiling
            if p.position.y < self.radius:
                p.position.y = self.radius
                p.velocity.y *= -0.8

            # Right wall
            if p.position.x > SCREEN_WIDTH - self.radius:
                p.position.x = SCREEN_WIDTH - self.radius
                p.velocity.x *= -0.8
                if abs(p.velocity.x) < 2:
                    p.velocity.x = 0

            # Left wall
            if p.position.x < self.radius:
                p.position.x = self.radius
                p.velocity.x *= -0.8
                if abs(p.velocity.x) < 2:
                    p.velocity.x = 0

        self.resolve_collision()

    def resolve_collision(self):
        radius = 5
        for i, ball1 in enumerate(self.balls):
            for j, ball2 in enumerate(self.balls[i+1:], i+1):
                delta = ball2.position - ball1.position
                distance = delta.length()
                min_distance = radius * 2
                if distance < min_distance:
                    overlap = (min_distance - distance) * 0.9
                    push = delta.normalize() * overlap
                    ball1.position -= push
                    ball2.position += push
            




#creating engine and ball
engine = Engine(gravity=(0, 500))

start_pos = Vector2(300, 300)
engine.balls.append(ball(position=start_pos))
engine.balls.append(ball(position=start_pos + Vector2(30, 0))) 

#apply constraints
# apply constraints
rest_length = 30  
for i in range(len(engine.balls)-1):
    d = distance_constraint(engine.balls[i], engine.balls[i+1], rest_length)
    engine.constraints.append(d)


run = True

while run:
    dt = clock.tick(fps) / 1000 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = Vector2(pygame.mouse.get_pos())
            for b in engine.balls:
                if(b.position - mouse_pos).length() < 10:
                    engine.selected = b
                    engine.prev_mouse_pos = mouse_pos
                    b.velocity = Vector2(0, 0)
                    break
        elif event.type == pygame.MOUSEBUTTONUP:
            if engine.selected:
                current_mouse_pos = Vector2(pygame.mouse.get_pos())
                velocity = (current_mouse_pos - engine.prev_mouse_pos) * 2
                engine.selected.velocity = velocity
                engine.selected = None
                engine.prev_mouse_pos = Vector2(0, 0)


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