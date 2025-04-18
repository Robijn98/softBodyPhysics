import pygame
from pygame.math import Vector2
import math
import random
import sys
from collisions import resolve_collision
from settings import balls, constraints, objects

class Engine():
    def __init__(self, gravity, radius=5):
        self.radius = radius
        # self.balls = []
        # self.constraints = []
        # self.objects = []
        self.gravity = Vector2(gravity)
        self.selected = None
        self.mouse_pos = Vector2(0, 0)
        self.prev_mouse_pos = Vector2(0, 0)



    def update(self, dt):

        for p in balls:
            p.force = Vector2(0, 0)


        for c in constraints:
            c.constrain(dt, self.gravity)

        for p in balls:
            p.position += p.velocity * dt


        resolve_collision(balls=balls, objects=objects)




