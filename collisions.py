from settings import *
import math

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
    

def resolve_collision(balls, objects):
    
    radius = 5
    dt = 1 / 60
    restitution = 0.5
    friction = 0.8

    # only loop each unordered pair once
    mass_ball = 1.0
    mass_edge = 2.0


    for ball in balls:
        
        collision_with_environment(ball)
        
        #prevent self collision
        for obj in objects:
            
            if ball in obj:
                print(f"Skipping self collision for ball {ball} in object {obj}")
                continue

            # loop every edge 
            dist = 1000
            closest_edge = (0, 0)
            for i in range(len(obj)):
                # find the closest edge to the ball
                # keep checking distance is bigger than radius

                A = obj[i]
                B = obj[(i+1) % len(obj)]
                
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

                if t < dist:
                    dist = t
                    closest_edge = (A, B)

                if dist < 10:
                    # collision
                    print("Collision detected")
                    print(f"dist: {dist}, A: {A.position}, B: {B.position}")










                # Y = B.position.y - A.position.y
                # X = B.position.x - A.position.x
                # numerator = (Y * ball.position.x) - (X * ball.position.y) + (B.position.x * A.position.y) - (A.position.x * B.position.y)
                # numerator = abs(numerator)
                # denomenator = math.sqrt(((Y * Y) + (X * X)))
                # dist = numerator / denomenator
     
                # if dist < 10:
                #     # collision
                #     print("Collision detected")
                #     print(f"dist: {dist}, A: {A.position}, B: {B.position}")
                




                # A = obj[i]
                # # modulus to loop back to the first point
                # B = obj[(i+1) % len(obj)]
                # AB = B.position - A.position

                # # project center onto AB:
                # t = (ball.position - A.position).dot(AB)
                # denom = AB.length_squared() + 1e-6 
                # t /= denom
                # t = max(0.0, min(1.0, t))

                # closest = A.position + AB * t
                # diff    = ball.position - closest
                # dist    = diff.length()
                # penetration = radius - dist

                # if penetration <= 0:
                #     continue 

                # # collision normal
                # if dist == 0:
                #     n = AB.normalize().rotate(90)
                # else:
                #     n = diff.normalize()

                # # relative velocity at the contact point
                # v_edge  = A.velocity * (1-t) + B.velocity * t
                # rel_vel = ball.velocity - v_edge
                # vn = rel_vel.dot(n)

                # print(f"vn: {vn}, penetration: {penetration}, t: {t}, A: {A.position}, B: {B.position}")
                # if vn < 0:
                #     inv_m_edge = ((1-t)**2 + t**2) / mass_edge
                #     inv_m = mass_ball + inv_m_edge

                #     # normal impulse magnitude
                #     numerator = -(1 + restitution) * vn
                #     denominator = (1/ 2) + (i + t) ** 2 * (1/6)
                #     j_mag = numerator / denominator
                    
                #     j = n * j_mag

                #     # apply to ball and edge endpoints
                #     ball.velocity += j / mass_ball
                #     A.velocity    -= j * (1-t)  /mass_edge
                #     B.velocity    -= j *    t  /mass_edge

                # if penetration > 0.01:
                #     # apply penetration correction

                #     correction = n * (penetration) * (1 - restitution )

                #     ball.position += correction / mass_ball
                #     A.position    -= correction * (1-t) / mass_edge
                #     B.position    -= correction *    t  / mass_edge



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
