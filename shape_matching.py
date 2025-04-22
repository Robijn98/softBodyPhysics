from settings import *
import math
from pygame.math import Vector2


def shape_matching(obj, dt, springforce):
    #find center of object
    center = Vector2(0, 0)
    for v in obj.vertices:
        center += v.position
    center /= len(obj.vertices)

    #find rotation angle
    A = 0
    B = 0
    for v in obj.vertices:
        r = v.position - center  
        q = v.rest_position     
        A += r.dot(q)
        B += r.cross(q)

    angle = -math.atan2(B, A)  
    for v in obj.vertices:
        v.rest_position.rotate_ip(angle)
    # match the shape to the rest position
    for v in obj.vertices:
        q_rotated = v.rest_position.rotate(angle)
        target = center + q_rotated
        delta = target - v.position
        v.velocity += delta * springforce * dt


def pressure_force(obj, dt, pressureforce):
    # find center of object
    center = Vector2(0, 0)
    for v in obj.vertices:
        center += v.position
    center /= len(obj.vertices)

    # find pressure force
    for v in obj.vertices:
        r = v.position - center  
        q = v.rest_position     
        target = center + q
        delta = target - v.position
        v.velocity += delta * pressureforce * dt
    
