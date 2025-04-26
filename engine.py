import pygame
from pygame.math import Vector2
from collisions import resolve_collision, collision_with_static
from settings import *
from shape_matching import shape_matching, pressure_force

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
            if p.static == False:
                p.position += p.velocity * dt
            

        for i in objects:
            shape_matching(i, dt, 500)
         
        #constraints
        
        for joint in joints:
            joint.connect()


        resolve_collision(balls=balls, objects=objects)
        collision_with_static(balls=balls, objects=objects)


