#!/usr/bin/env python
import pygame
import math
from random import random
from pygame.math import Vector2

"""
A Physics toy based on this blog entitled 'Six useful snippets':
https://blog.bruce-hill.com/6-useful-snippets

Worth visiting the web page to see the author break down the six different algorithms (with interactive examples)
that go into making up this program. 

I've converted the final program over to pygame for you.
"""


def mix(a_val, b_val, amount):
    """
    Also known as 'lerp'. this simple bit of maths lets us blend smoothly between two different values.
    Useful when you want to blend between colours, positions or something else by some percentage amount.
    """
    return (1 - amount) * a_val + amount * b_val


def clamp(x, minimum, maximum):
    if x < minimum:
        return minimum
    if x > maximum:
        return maximum
    return x


def mix_vector2(a_vec, b_vec, amount):
    mix_x = mix(a_vec.x, b_vec.x, amount)
    mix_y = mix(a_vec.y, b_vec.y, amount)
    return Vector2(mix_x, mix_y)


def clamp_vector2(vector_to_clamp, min_vec, max_vec):
    clamped_x = clamp(vector_to_clamp.x, min_vec.x, max_vec.x)
    clamped_y = clamp(vector_to_clamp.y, min_vec.y, max_vec.y)
    return Vector2(clamped_x, clamped_y)


W, H = 500, 375
MIN_RADIUS, MAX_RADIUS = W / 40, W / 12
BUCKET_SIZE = 1.1 * MAX_RADIUS
STIFFNESS = 0.5
GRAVITY = Vector2(0, 2000)
GOLDEN_RATIO = (math.sqrt(5) - 1) / 2


def collisions_between(things):
    buckets = dict()
    maybe_collisions = set()
    for t in things:
        xmin = int((t.pos.x - t.radius) / BUCKET_SIZE)
        xmax = int((t.pos.x + t.radius) / BUCKET_SIZE)
        for x in range(xmin, xmax + 1):
            ymin = int((t.pos.y - t.radius) / BUCKET_SIZE)
            ymax = int((t.pos.y + t.radius) / BUCKET_SIZE)
            for y in range(ymin, ymax + 1):
                if (x, y) not in buckets:
                    buckets[(x, y)] = []
                else:
                    for other in buckets[(x, y)]:
                        maybe_collisions.add((other, t))
                buckets[(x, y)].append(t)

    return [(a, b) for (a, b) in maybe_collisions
            if a.pos.distance_to(b.pos) <= a.radius + b.radius]


class Ball:
    def __init__(self, position, radius, colour):
        self.pos = position
        self.prev_pos = position
        self.radius = radius
        self.mass = radius * radius
        self.color = colour

    def in_radius(self, point):
        if self.pos.distance_to(point) < self.radius:
            return True
        return False


pygame.init()

screen = pygame.display.set_mode((W, H))
background = pygame.Surface((W, H))
background.fill(pygame.Color("#FFFFFF"))

balls = []
for i in range(30):
    r = mix(MIN_RADIUS, MAX_RADIUS, random())
    pos = Vector2(mix(r, W - r, random()), mix(r, H - r, random()))
    color = pygame.Color("#000000")
    color.hsla = 360 * ((i * GOLDEN_RATIO) % 1), 50, 70, 100
    balls.append(Ball(pos, r, color))

dt, iterations = 1 / 60, 5

clock = pygame.time.Clock()
running = True
held_ball = None
while running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = Vector2(pygame.mouse.get_pos())
                for ball in balls:
                    if ball.in_radius(mouse_pos):
                        held_ball = ball

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                held_ball = None

    for ball in balls:
        # Verlet integration
        next_pos = (2 * ball.pos) - ball.prev_pos + (GRAVITY * (dt * dt))
        ball.prev_pos = ball.pos
        ball.pos = next_pos

    if held_ball is not None:
        held_ball.pos = Vector2(pygame.mouse.get_pos())

    # Solve constraints iteratively
    for _ in range(iterations):
        # Resolve overlaps:
        for (a, b) in collisions_between(balls):
            a2b = (b.pos - a.pos).normalize()
            distance = a.pos.distance_to(b.pos)
            overlap = (a.radius + b.radius) - distance
            a.pos = a.pos - a2b * (STIFFNESS * overlap * (b.mass / (a.mass + b.mass)))
            b.pos = b.pos + a2b * (STIFFNESS * overlap * (a.mass / (a.mass + b.mass)))

        # Stay on screen:
        for b in balls:
            clamped = clamp_vector2(b.pos, Vector2(b.radius, b.radius),
                                    Vector2(W - b.radius, H - b.radius))

            if clamped != b.pos:
                b.pos = mix_vector2(b.pos, clamped, STIFFNESS)
                # damping
                b.prev_pos = mix_vector2(b.prev_pos, b.pos, 0.001)

        # Draw:
        screen.blit(background, (0, 0))
        for ball in balls:
            pygame.draw.circle(screen, ball.color, (int(ball.pos.x), int(ball.pos.y)), int(ball.radius))

    pygame.display.flip()
