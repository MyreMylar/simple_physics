import math
import pygame
from pygame.locals import *


class ControlScheme:
    def __init__(self):
        self.left = K_LEFT
        self.right = K_RIGHT
        self.up = K_UP
        self.down = K_DOWN


class Bat:

    def __init__(self, start_pos, control_scheme):
        self.control_scheme = control_scheme
        self.move_left = False
        self.move_right = False
        self.rotate_left = False
        self.rotate_right = False
        self.move_speed = 350.0

        self.height = 10.0
        self.width = 100.0

        self.rotation = 0.0

        self.bounce_factor = 1.1

        self.position = [float(start_pos[0]), float(start_pos[1])]

        self.verts = [[start_pos[0], start_pos[1]],
                      [start_pos[0] + self.width, start_pos[1]],
                      [start_pos[0] + self.width, start_pos[1] + self.height],
                      [start_pos[0], start_pos[1] + self.height]]

        self.edges = [[self.verts[0], self.verts[1]],
                      [self.verts[1], self.verts[2]],
                      [self.verts[2], self.verts[3]],
                      [self.verts[3], self.verts[0]]]
        
        self.rect = pygame.Rect((start_pos[0]-self.width/2, start_pos[1]), (self.width, self.height))
        self.rect.centerx = self.position[0]
        self.rect.centery = self.position[1]
        self.bat_colour = pygame.Color("#FFFFFF")

        self.color_key = (127, 33, 33)
        self.draw_surface = pygame.Surface((self.rect.width, self.rect.height))
        self.final_draw_surface = pygame.Surface((self.rect.width, self.rect.height))

        self.draw_surface.fill(self.color_key)
        self.draw_surface.set_colorkey(self.color_key)
        pygame.draw.rect(self.draw_surface,
                         self.bat_colour,
                         pygame.Rect(0,
                                     0,
                                     self.rect.width,
                                     self.rect.height))
        self.draw_surface.set_alpha(255)
        self.final_draw_surface = pygame.transform.rotate(self.draw_surface,
                                                          (self.rotation * 180 / math.pi))

        self.start_normal_vec = [0.0, -1.0]
        self.normal_vec = [0.0, -1.0]

    def rotate(self, rotation):
        self.rotation += rotation

        cos_rotation = math.cos(-self.rotation)
        sin_rotation = math.sin(-self.rotation)
        self.normal_vec[0] = self.start_normal_vec[0] * cos_rotation - self.start_normal_vec[1] * sin_rotation
        self.normal_vec[1] = self.start_normal_vec[0] * sin_rotation + self.start_normal_vec[1] * cos_rotation
        self.update_real_bounds()
        self.final_draw_surface = pygame.transform.rotate(self.draw_surface,
                                                          (self.rotation * 180 / math.pi))

    def process_event(self, event):
        if event.type == KEYDOWN:
            if event.key == self.control_scheme.left:
                self.move_left = True
            if event.key == self.control_scheme.right:
                self.move_right = True
            if event.key == self.control_scheme.down:
                self.rotate_left = True
            if event.key == self.control_scheme.up:
                self.rotate_right = True

        if event.type == KEYUP:
            if event.key == self.control_scheme.left:
                self.move_left = False
            if event.key == self.control_scheme.right:
                self.move_right = False
            if event.key == self.control_scheme.down:
                self.rotate_left = False
            if event.key == self.control_scheme.up:
                self.rotate_right = False

    def update(self, dt):
        if self.move_left:
            self.position[0] -= dt * self.move_speed

            if self.position[0] < 20.0 + (self.width / 2):
                self.position[0] = 20.0 + (self.width / 2)

            self.rect.centerx = self.position[0]
            self.update_real_bounds()
                
        if self.move_right:
            self.position[0] += dt * self.move_speed

            if self.position[0] > 800 - 20 - (self.width / 2):
                self.position[0] = 800 - 20 - (self.width / 2)

            self.rect.centerx = self.position[0]
            self.update_real_bounds()

        if self.rotate_left:
            self.rotate(10 * dt)
        if self.rotate_right:
            self.rotate(-10 * dt)

    def render(self, screen):
        screen.blit(self.final_draw_surface,
                    [self.rect.centerx - (self.final_draw_surface.get_width() / 2),
                     self.rect.centery - (self.final_draw_surface.get_height() / 2)])

    def update_real_bounds(self):
        cos_rotation = math.cos(-self.rotation)
        sin_rotation = math.sin(-self.rotation)
        half_width = self.width / 2
        half_height = self.height / 2

        top_left = [0.0, 0.0]
        top_left[0] = self.position[0] + ((-half_width * cos_rotation) - (-half_height * sin_rotation))
        top_left[1] = self.position[1] + ((-half_width * sin_rotation) + (-half_height * cos_rotation))

        top_right = [0.0, 0.0]
        top_right[0] = self.position[0] + ((half_width * cos_rotation) - (-half_height * sin_rotation))
        top_right[1] = self.position[1] + ((half_width * sin_rotation) + (-half_height * cos_rotation))

        bottom_left = [0.0, 0.0]
        bottom_left[0] = self.position[0] + ((-half_width * cos_rotation) - (half_height * sin_rotation))
        bottom_left[1] = self.position[1] + ((-half_width * sin_rotation) + (half_height * cos_rotation))

        bottom_right = [0.0, 0.0]
        bottom_right[0] = self.position[0] + ((half_width * cos_rotation) - (half_height * sin_rotation))
        bottom_right[1] = self.position[1] + ((half_width * sin_rotation) + (half_height * cos_rotation))

        self.verts[:] = []
        self.verts.append(top_left)
        self.verts.append(top_right)
        self.verts.append(bottom_left)
        self.verts.append(bottom_right)

        self.edges[:] = []
        self.edges.append([top_left, top_right])
        self.edges.append([top_left, bottom_left])
        self.edges.append([bottom_right, top_right])
        self.edges.append([bottom_right, bottom_left])

    @staticmethod
    def collide_polygon_with_polygon(a, b):
        polygons = [a, b]

        for i in range(0, len(polygons)):
            # for each polygon, look at each edge of the polygon, and determine if it separates
            # the two shapes
            polygon = polygons[i]
            for edge in polygon.edges:
                # grab 2 vertices to create an edge
                # var i2 = (i1 + 1) % polygon.length;
                p1 = edge[0]
                p2 = edge[1]

                # find the line perpendicular to this edge
                normal = [p2[1] - p1[1], p1[0] - p2[0]]

                min_a = None
                max_a = None
                # for each vertex in the first shape, project it onto the line perpendicular to the edge
                # and keep track of the min and max of these values
                for j in range(0, len(a.verts)):
                    projected = (normal[0] * a.verts[j][0]) + (normal[1] * a.verts[j][1])
                    if (min_a is None) or (projected < min_a):
                        min_a = projected

                    if (max_a is None) or (projected > max_a):
                        max_a = projected

                # for each vertex in the second shape, project it onto the line perpendicular to the edge
                # and keep track of the min and max of these values
                min_b = None
                max_b = None
                for j in range(0, len(b.verts)):
                    projected = (normal[0] * b.verts[j][0]) + (normal[1] * b.verts[j][1])
                    if (min_b is None) or (projected < min_b):
                        min_b = projected

                    if (max_b is None) or (projected > max_b):
                        max_b = projected

                # if there is no overlap between the projects, the edge we are looking at separates the two
                # polygons, and we know there is no overlap
                if (max_a < min_b) or (max_b < min_a):
                    return False

        return True
