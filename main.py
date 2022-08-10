import pygame
import time
import math
import random

class Sphere():
    def __init__(self, x, y, xv, yv, mass, color, elasticity):
        self.x = x
        self.y = y
        self.xv = xv
        self.yv = yv
        self.mass = mass
        self.color = color
        self.elasticity = elasticity
        self.rad = math.sqrt(mass / 3.142)

    @property
    def momentum(self):
        return math.sqrt((self.xv) ** 2 + (self.yv) ** 2) * self.mass
    @property
    def resultant_vector(self):
        return math.sqrt((self.xv) ** 2 + (self.yv) ** 2)
    def update(self):
        self.x += self.xv
        if self.x + self.rad > Status.screen_size[0]:
            self.xv = -self.xv
            self.x = 2 * Status.screen_size[0] - self.x - 2 * self.rad
        elif self.x - self.rad < 0:
            self.xv = -self.xv
            self.x = -self.x + 2 * self.rad
        self.y += self.yv
        if self.y + self.rad > Status.screen_size[1]:
            self.yv = -self.yv
            self.y = 2 * Status.screen_size[1] - self.y - 2 * self.rad
        elif self.y - self.rad < 0:
            self.yv = -self.yv
            self.y = -self.y + 2 * self.rad

    def collide(self, other:object):
        y_dis = self.y - other.y
        x_dis = self.x - other.x
        dis = math.sqrt((x_dis) ** 2 + (y_dis) ** 2)
        if dis == 0:
            self.x -= 1
            self.y -= 1
            y_dis = self.y - other.y
            x_dis = self.x - other.x
            dis = math.sqrt((x_dis) ** 2 + (y_dis) ** 2)

        y_over_dis = y_dis / dis
        x_over_dis = x_dis / dis

        self_tan = (self.yv * -x_over_dis + self.xv * y_over_dis)
        self_norm = (self.yv * y_over_dis + self.xv * x_over_dis)

        other_tan = (other.yv * -x_over_dis + other.xv * y_over_dis)
        other_norm = (other.yv * y_over_dis + other.xv * x_over_dis)

        #formula src: https://www.vobarian.com/collisions/2dcollisions2.pdf
        self_final_norm = (self_norm * (self.mass - other.mass) + 2 * other.mass * other_norm)\
                       / (self.mass + other.mass)
        obj_final_norm = (other_norm * (other.mass - self.mass) + 2 * self.mass * self_norm)\
                      / (other.mass + self.mass)

        self.xv = self_tan * y_over_dis + self_final_norm * x_over_dis
        self.yv = self_tan * -x_over_dis + self_final_norm * y_over_dis

        other.xv = other_tan * y_over_dis + obj_final_norm * x_over_dis
        other.yv = other_tan * -x_over_dis + obj_final_norm * y_over_dis

    def collide1(self, other:object):
        temp_y = self.yv
        temp_x = self.xv
        self.xv = (other.xv * other.mass / self.mass + self.xv) / 2
        self.yv = (other.yv * other.mass / self.mass + self.yv) / 2
        other.xv = (temp_x * self.mass / other.mass + other.xv) / 2
        other.yv = (temp_y * self.mass / other.mass + other.yv) / 2

    def collide2(self, other:object):
        y_dis = self.y - other.y
        x_dis = self.x - other.x
        self_momen = self.momentum
        other_momen = other.momentum
        self_theta = math.degrees(1.5708 - math.atan(x_dis / y_dis) - math.atan2(self.yv, self.xv))
        other_theta = math.degrees(1.5708 - math.atan(-x_dis / -y_dis) - math.atan2(other.yv, other.xv))

        self.yv = other_momen / self.mass * math.sin(self_theta)
        self.xv = other_momen / self.mass * math.cos(self_theta)

        other.yv = self_momen / other.mass * math.sin(other_theta)
        other.xv = self_momen / other.mass * math.cos(other_theta)

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.rad)

def friction(self:Sphere, scale:float):
    scale %= 1
    self.xv *= (1 - scale)
    self.yv *= (1 - scale)

def earth(self:Sphere, scale):
    if self.y > Status.screen_size[1] - (self.rad + 5):
        friction(self, 0.05)
        return
    self.yv += scale
    friction(self, 0.01)

def blackhole(target, hole_x, hole_y, scale):
    x_dis = target.x - hole_x
    y_dis = target.y - hole_y
    dis = math.sqrt((x_dis) ** 2 + (y_dis) ** 2)
    if dis == 0:
        return
    scale = scale ** 2 / dis ** 2
    target.xv -= x_dis / dis * scale
    target.yv -= y_dis / dis * scale

def draw_arrow(window, color, p1, p2, width = 5, scale = 1, head = 5):
    v1 = [p2[0] - p1[0], p2[1] - p1[1]]
    hypo = math.sqrt(v1[0] ** 2 + v1[1] ** 2)
    if hypo == 0:
        return
    v2 = [v1[1], -v1[0]]
    uv2 = [v2[0] / hypo, v2[1] / hypo]
    uv1 = [v1[0] / hypo, v1[1] / hypo]
    body = hypo * scale - head
    if body < 0:
        return
    vertices = [
        (p1[0] + width * uv2[0], p1[1] + width * uv2[1]),
        (p1[0] + body * uv1[0] + width * uv2[0], p1[1] + body * uv1[1] + width * uv2[1]),
        (p1[0] + body * uv1[0] + 2 * width * uv2[0], p1[1] + body * uv1[1] + 2 * width * uv2[1]),
        (p1[0] + scale * v1[0], p1[1] + scale * v1[1]),
        (p1[0] + body * uv1[0] - 2 * width * uv2[0], p1[1] + body * uv1[1] - 2 * width * uv2[1]),
        (p1[0] + body * uv1[0] - width * uv2[0], p1[1] + body * uv1[1] - width * uv2[1]),
        (p1[0] - width * uv2[0], p1[1] - width * uv2[1]),
    ]
    pygame.draw.polygon(window, color, vertices)

def print_trail(target:Sphere):
    draw_arrow(Status.window,
               target.color,
               (target.x, target.y),
               (target.x + target.xv, target.y + target.yv),
               target.rad / 2,
               0,
               -7.3
    )

def print_vector(target:Sphere, width = 0.5, scale = 10, head = 5):
    draw_arrow(Status.window, Color.BLUE,
               (target.x, target.y),
               (target.x + target.xv, target.y),
               width, scale, head)
    draw_arrow(Status.window, Color.RED,
               (target.x, target.y),
               (target.x, target.y + target.yv),
               width, scale, head)
    draw_arrow(Status.window, Color.LIME,
               (target.x, target.y),
               (target.x + target.xv, target.y + target.yv),
               width, scale, head)

class Color:
    WHITE = (255, 255, 255)
    BLACK = (0,0,0)
    YELLOW = (255,255,0)
    RED = (255, 0, 0)
    CYAN = (0, 255, 255)
    LIME = (0, 255, 0)
    BLUE = (0, 0, 255)

class Status:
    screen_size = (1200, 700)
    window = pygame.display.set_mode(screen_size)
    mid = (screen_size[0] / 2, screen_size[1] / 2)
    run = True

def random_balls(count = 10):
    balls = []
    i = 0
    while (i < count):
        mass = random.randint(100, 500)

        balls.append(Sphere(
            random.randint(0, Status.screen_size[0]),
            random.randint(0, Status.screen_size[1]),
            random.randint(-1, 1),
            random.randint(-1, 1),
            mass,
            (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)),
            1#random.uniform(0.9, 1)
        ))
        i += 1
    return balls

def run():
    # up down left right
    pressed = []
    scale = 100
    directions = {82:(0, -scale),81:(0, scale),80:(-scale, 0),79:(scale, 0)}
    balls = []

    balls.append(Sphere(300, 300, 0, 0, 10000, Color.YELLOW, 1))
    # balls.append(Sphere(100, 300, 10, 0, 100, Color.RED, 1))
    #balls.append(object(500, 140, -10, 0, 100, Color.RED, 1))
    #balls.append(object(200, 100, 10, 0, 100, Color.RED, 1))
    #balls.append(object(600, 100, 10, 0, 100, Color.RED, 1))

    pygame.init()
    pygame.display.set_caption("the best game ever")
    clock = pygame.time.Clock()
    player1 = 0

    while Status.run:
        clock.tick(60)

        if balls.__len__() <= 1:
            time.sleep(1)
            #player1 = object(100, 140, 0, 0, 50000, Color.RED, 1)
            balls = random_balls(2)
            #balls.append(player1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Status.run = False
            elif event.type == pygame.KEYDOWN:
                pressed.append(event.scancode)
            elif event.type == pygame.KEYUP:
                pressed.remove(event.scancode)

        for key in pressed:
            if key in directions:
                #player1.yv += directions[key][1] / ball.mass
                #player1.xv += directions[key][0] / ball.mass
                for ball in balls:
                    ball.yv += directions[key][1] / ball.mass
                    ball.xv += directions[key][0] / ball.mass

        Status.window.fill(Color.WHITE)
        balls.sort(key=lambda x: x.x)
        for idx, ball in enumerate(balls):
            # if Status.mid[0] - 10 <= ball.x <= Status.mid[0] + 10:
            #     if math.sqrt((ball.x - Status.mid[0]) ** 2 + (ball.y - Status.mid[1]) ** 2) < ball.rad + 10:
            #         if ball is player1:
            #             print(f"you are number {balls.__len__()}")
            #             balls = [];
            #         else:
            #             balls.pop(idx)
            #             print(balls.__len__())
            #         continue
            for other in balls[idx + 1:]:
                rad = ball.rad + other.rad
                if other.x - ball.x < rad:
                    if math.sqrt((ball.x - other.x) ** 2 + (ball.y - other.y) ** 2) < rad:
                        ball.collide(other)
                else:
                    break
            ball.update()
            earth(ball, 0.981)
            #blackhole(ball, Status.mid[0], Status.mid[1], 100)
            ball.draw(Status.window)
            print_vector(ball, scale=ball.mass / 100)
        # pygame.draw.circle(Status.window, (255, 255, 255), Status.mid, 10)
        pygame.display.update()
    pygame.quit()

if __name__ == '__main__':
    run()