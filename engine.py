import pygame
from pygame.math import Vector2
import math
import random
import sys
from settings import *
from collisions import  resolve_collision

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


        resolve_collision(balls=self.balls, objects=self.objects)




