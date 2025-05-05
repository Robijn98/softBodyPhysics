from settings import *
import math
from pygame.math import Vector2

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
    
def collision_with_static(balls, objects):
    radius = 5
    restitution = 0.5
    friction = 0.8

    for ball in balls:
        if ball.static:
            continue
        for obj in objects:
            if not obj.static:
                continue

            closest_dist = 1000
            closest_edge = None
            closest_t = 0

            for i in range(len(obj.vertices)):
                A = obj.vertices[i]
                B = obj.vertices[(i + 1) % len(obj.vertices)]

                AB = B.position - A.position
                AE = ball.position - A.position
                BE = ball.position - B.position

                AB_BE = AB.dot(BE)
                AB_AE = AB.dot(AE)

                if AB_BE > 0:
                    t = (ball.position - B.position).length()
                elif AB_AE < 0:
                    t = (ball.position - A.position).length()
                else:
                    x1, y1 = AB.x, AB.y
                    x2, y2 = AE.x, AE.y
                    mod = math.sqrt(x1**2 + y1**2)
                    t = abs(x1 * y2 - x2 * y1) / mod

                if t < closest_dist:
                    closest_dist = t
                    closest_edge = (A, B)

            if closest_dist < radius:
                # We have a collision

                A, B = closest_edge
                AB = B.position - A.position
                AE = ball.position - A.position

                ab_len2 = AB.length_squared()
                t = AE.dot(AB) / (ab_len2 + 1e-6)
                t = max(0.0, min(1.0, t))

                closest_point = A.position + AB * t
                diff = ball.position - closest_point

                if diff.length_squared() == 0:
                    n = AB.normalize().rotate(90) 
                else:
                    n = diff.normalize()

                # push ball out
                penetration = radius - closest_dist
                ball.position += n * penetration

                # bounce
                vn = ball.velocity.dot(n)
                if vn < 0:
                    ball.velocity -= (1 + restitution) * vn * n

                # Friction
                vt = ball.velocity - ball.velocity.dot(n) * n
                ball.velocity -= vt * (1 - friction)

                # Small velocity kill
                if abs(ball.velocity.x) < 0.5:
                    ball.velocity.x = 0
                if abs(ball.velocity.y) < 0.5:
                    ball.velocity.y = 0


            # Check for collision with each vertex
            for vertex in obj.vertices:
                diff = ball.position - vertex.position
                dist = diff.length()

                if dist < radius:
                    #collision detected 
                    penetration = radius - dist
                    if dist == 0:
                        n = Vector2(0, -1) 
                    else:
                        n = diff.normalize()

                    # Push ball
                    ball.position += n * penetration

                    #velocity
                    vn = ball.velocity.dot(n)
                    if vn < 0:
                        ball.velocity -= (1 + restitution) * vn * n

                    # Friction
                    vt = ball.velocity - ball.velocity.dot(n) * n
                    ball.velocity -= vt * (1 - friction)

                    if abs(ball.velocity.x) < 0.5:
                        ball.velocity.x = 0
                    if abs(ball.velocity.y) < 0.5:
                        ball.velocity.y = 0





def resolve_collision(balls, objects):
    
    radius = 5
    dt = 1 / 60
    restitution = 0.5
    friction = 0.8

    mass_ball = 1.0
    mass_edge = 2.0

    for ball in balls:
        
        collision_with_environment(ball)
        
        #prevent self collision
        for obj in objects:

            if ball in obj.vertices or obj.static:
                continue
                
            # loop every edge 
            dist = 1000
            closest_edge = (0, 0)
            for i in range(len(obj.vertices)):
                
                #if any point of the object is inside the ball, ignore collision
                A = obj.vertices[i]
                B = obj.vertices[(i+1) % len(obj.vertices)]
                
                AB = B.position - A.position
                BE = ball.position - B.position
                AE = ball.position - A.position
                AB_BE = AB.dot(BE)
                AB_AE = AB.dot(AE)
                
                if AB_BE > 0:
                    y = ball.position.y - B.position.y
                    x = ball.position.x - B.position.x
                    t = math.sqrt(x**2 + y**2)
                
                elif AB_AE < 0:
                    y = ball.position.y - A.position.y
                    x = ball.position.x - A.position.x
                    t = math.sqrt(x**2 + y**2)
                else:
                    x1 = AB.x
                    y1 = AB.y
                    x2 = AE.x
                    y2 = AE.y

                    mod = math.sqrt(x1**2 + y1**2)
                    t = abs(x1 * y2 - x2 * y1) / mod

                if t < dist and dist != 0:
                    dist = t
                    closest_edge = (A, B)

                if dist < radius:
                    # collision detected
                    
                    # project center onto AB:
                    t = (ball.position - A.position).dot(AB)
                    denom = AB.length_squared() + 1e-6 
                    t /= denom
                    t = max(0.0, min(1.0, t))

                    closest = A.position + AB * t
                    diff    = ball.position - closest
                    penetration = radius - dist

                    if penetration <= 0:
                        continue 

                    # collision normal
                    if dist == 0:
                        n = AB.normalize().rotate(90)
                    else:
                        n = diff.normalize()

                    # relative velocity at ] contact point
                    v_edge  = A.velocity * (1-t) + B.velocity * t
                    rel_vel = ball.velocity - v_edge
                    vn = rel_vel.dot(n)

                    if vn < 0:
                        inv_m_edge = ((1-t)**2 + t**2) / mass_edge
                        inv_m = mass_ball + inv_m_edge

                        # normal impulse magnitude
                        numerator = -(1 + restitution) * vn
                        denominator = (1/ 2) + (i + t) ** 2 * (1/6)
                        j_mag = numerator / denominator
                        
                        j = n * j_mag

                        # apply to ball and edge endpoints
                        ball.velocity += j / mass_ball * friction
                        A.velocity    -= j * (1-t)  /mass_edge * friction
                        B.velocity    -= j *    t  /mass_edge 

            # Check for collision with each vertex
            for vertex in obj.vertices:
                diff = ball.position - vertex.position
                dist = diff.length()

                if dist < radius:
                    # Collision 
                    penetration = radius - dist
                    if dist == 0:
                        n = Vector2(0, -1)  
                    else:
                        n = diff.normalize()

                    # Push ball 
                    ball.position += n * penetration

                    #  velocity
                    vn = ball.velocity.dot(n)
                    if vn < 0:
                        ball.velocity -= (1 + restitution) * vn * n

                    # Friction
                    vt = ball.velocity - ball.velocity.dot(n) * n
                    ball.velocity -= vt * (1 - friction)


                    if abs(ball.velocity.x) < 0.5:
                        ball.velocity.x = 0
                    if abs(ball.velocity.y) < 0.5:
                        ball.velocity.y = 0


