import pygame
from pygame.locals import *


class ControlScheme:
    def __init__(self):
        self.left = K_LEFT
        self.right = K_RIGHT


class Bat:

    def __init__(self, start_pos, control_scheme):
        self.control_scheme = control_scheme
        self.move_left = False
        self.move_right = False
        self.move_speed = 350.0

        self.length = 10.0
        self.width = 100.0

        self.bounce_factor = 1.1

        self.position = [float(start_pos[0]), float(start_pos[1])]
        
        self.rect = pygame.Rect((start_pos[0], start_pos[1]), (self.width, self.length))
        self.bat_colour = pygame.Color(255, 255, 255, 255)

    def process_event(self, event):
        if event.type == KEYDOWN:
            if event.key == self.control_scheme.left:
                self.move_left = True
            if event.key == self.control_scheme.right:
                self.move_right = True

        if event.type == KEYUP:
            if event.key == self.control_scheme.left:
                self.move_left = False
            if event.key == self.control_scheme.right:
                self.move_right = False

    def update(self, dt):
        if self.move_left:
            self.position[0] -= dt * self.move_speed

            if self.position[0] < 20.0:
                self.position[0] = 20.0

            self.rect.x = self.position[0]
                
        if self.move_right:
            self.position[0] += dt * self.move_speed

            if self.position[0] > 680.0:
                self.position[0] = 680.0

            self.rect.x = self.position[0]

    def render(self, screen):
        pygame.draw.rect(screen, self.bat_colour, self.rect)
