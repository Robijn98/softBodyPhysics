import pygame
from pygame.math import Vector2
import math
import random
import sys
from collisions import resolve_collision
from settings import balls, spring_points, objects

class Engine():
    def __init__(self, gravity, radius=5):
        self.radius = radius
        self.gravity = Vector2(gravity)
        self.selected = None
        self.mouse_pos = Vector2(0, 0)
        self.prev_mouse_pos = Vector2(0, 0)

    def update(self, dt):

        for p in balls:
            p.force = Vector2(0, 0)

        for c in spring_points:
            c.create_spring(dt, self.gravity)

        for p in balls:
            p.position += p.velocity * dt

        
        resolve_collision(balls=balls, objects=objects)
