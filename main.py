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
pygame.display.set_caption("Physics Simulation")
pygame.mouse.set_visible(True)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

screen.fill((0, 0, 0))

pygame.display.update()


class ball():
    def __init__(self, position):
        self.position = Vector2(position)
        self.velocity = Vector2(0, 0)
        self.colour=(255,0,0)


class Engine():
    def __init__(self, gravity):
        self.balls = []
        self.gravity = Vector2(gravity)

    def update(self, dt):
        for p in self.balls:
            p.velocity += self.gravity * dt
        for p in self.balls:
            p.position += p.velocity * dt


engine = Engine(gravity=(0, 500))

for i in range(0, 5):
    x = random.randint(200, 400)
    y = random.randint(200, 500)
    position = Vector2(x, y)
    engine.balls.append(ball(position=position))
    

run = True

while run:
    dt = clock.tick(fps) / 1000 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    engine.update(dt)
    screen.fill((0, 0, 0))

    for b in engine.balls:
        pygame.draw.circle(screen,(255,255,255), b.position, 5)
    pygame.display.update()

pygame.quit()
sys.exit()