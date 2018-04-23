import pygame


class Wall:
    def __init__(self, top_left, bottom_right):
        self.rect = pygame.Rect(top_left, (bottom_right[0]-top_left[0], bottom_right[1]-top_left[1]))
        self.wall_colour = pygame.Color(200, 200, 200, 200)

        self.bounce_factor = 0.85

        if abs(top_left[0] - bottom_right[0]) > abs(top_left[1] - bottom_right[1]):
            self.is_horiz = True
            self.is_vert = False
        else:
            self.is_horiz = False
            self.is_vert = True

    def render(self, screen):
        pygame.draw.rect(screen, self.wall_colour, self.rect)
