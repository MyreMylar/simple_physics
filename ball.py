import pygame
import math
import random


class Ball:

    def __init__(self, start_pos, colour):
        self.ball_speed = 350.0
        random_vec = self.make_random_start_vector()
        self.velocity = [random_vec[0] * self.ball_speed, random_vec[1] * self.ball_speed]
        self.rect = pygame.Rect((start_pos[0]-5, start_pos[1]-5), (10, 10))
        self.ball_colour = colour
        self.position = [float(start_pos[0]), float(start_pos[1])]
        self.start_position = [self.position[0], self.position[1]]

        self.max_bat_bounce_angle = 5.0 * math.pi / 12.0  # 75 degrees

        self.collided_with_things = []

        self.terminal_velocity = 20.0
        self.number_of_bounces = 0

        self.verts = []
        self.verts.append(self.rect.topleft)
        self.verts.append(self.rect.topright)
        self.verts.append(self.rect.bottomleft)
        self.verts.append(self.rect.bottomright)

        self.edges = []
        self.edges.append([self.rect.topleft, self.rect.topright])
        self.edges.append([self.rect.topleft, self.rect.bottomleft])
        self.edges.append([self.rect.bottomright, self.rect.topright])
        self.edges.append([self.rect.bottomright, self.rect.bottomleft])

    @staticmethod
    def make_random_start_vector():
        # make a normalised angle aiming roughly toward one of the goals
        y_random = random.uniform(-0.5, 0.5)
        x_random = 1.0 - abs(y_random)

        if random.randint(0, 1) == 1:
            x_random = x_random * -1.0
        
        return [x_random, y_random]

    def reset(self):
        self.number_of_bounces = 0
        self.position = [self.start_position[0], self.start_position[1]]
        random_vec = self.make_random_start_vector()
        self.velocity = [random_vec[0] * self.ball_speed, random_vec[1] * self.ball_speed]
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

    def update(self, dt, gravity, walls, bats):
        collided_this_frame = False
        collided_horiz_this_frame = False
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                collided_this_frame = True
                if wall not in self.collided_with_things:
                    self.collided_with_things.append(wall)

                    if wall.is_horiz:
                        # this does basic bounce reflection depending on if the wall is horizontal or vertical
                        self.velocity[1] = self.velocity[1] * -1
                        collided_horiz_this_frame = True
                    else:
                        # this does basic bounce reflection depending on if the wall is horizontal or vertical
                        self.velocity[0] = self.velocity[0] * -1 

                    # this scales our bounce by the ball's bounciness
                    self.velocity[1] = self.velocity[1] * wall.bounce_factor
                    self.velocity[0] = self.velocity[0] * wall.bounce_factor

                    self.number_of_bounces += 1

        for bat in bats:
            if bat.collide_polygon_with_polygon(bat, self):
                collided_this_frame = True
                if bat not in self.collided_with_things:
                    self.collided_with_things.append(bat)
                    
                    collided_horiz_this_frame = True

                    v_n = self.dot(self.velocity, bat.normal_vec)
                    n_n = self.dot(bat.normal_vec, bat.normal_vec)
                    u_div = (v_n / n_n)
                    u = [u_div * bat.normal_vec[0], u_div * bat.normal_vec[1]]
                    w = [self.velocity[0] - u[0], self.velocity[1] - u[1]]

                    friction = 1
                    elasticity = bat.bounce_factor  # this scales our bounce by the bat's bounciness
                    w_friction = [w[0] * friction, w[1] * friction]
                    u_elasticity = [u[0] * elasticity, u[1] * elasticity]
                    new_velocity = [w_friction[0] - u_elasticity[0], w_friction[1] - u_elasticity[1]]
                    self.velocity = new_velocity

                    self.number_of_bounces += 1

        if not collided_this_frame:
            self.collided_with_things.clear()

            # apply gravity to our ball's velocity every frame
            self.velocity[0] = self.velocity[0] + dt * gravity[0]
            self.velocity[1] = self.velocity[1] + dt * gravity[1]

            # make sure we don't accelerate our ball forever
            velocity_magnitude = math.sqrt((self.velocity[0]**2) + (self.velocity[1]**2)) * dt
            if velocity_magnitude > self.terminal_velocity:
                self.velocity[0] = self.velocity[0] / velocity_magnitude * self.terminal_velocity
                self.velocity[1] = self.velocity[1] / velocity_magnitude * self.terminal_velocity

        if collided_horiz_this_frame:
            # make sure we stop our ball from falling when we are resting on a surface
            if abs(self.velocity[1]) < 1.0:
                self.velocity[1] = 0.0
                self.velocity[0] = 0.0

            if abs(self.velocity[1]) < 50.0:
                # remove any Bounces added this frame because we are barely moving
                self.number_of_bounces -= 1

        # apply our ball's velocity to it's position
        self.position[0] = self.position[0] + dt * self.velocity[0]
        self.position[1] = self.position[1] + dt * self.velocity[1]
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

        self.verts[:] = []
        self.verts.append(self.rect.topleft)
        self.verts.append(self.rect.topright)
        self.verts.append(self.rect.bottomleft)
        self.verts.append(self.rect.bottomright)

        self.edges[:] = []
        self.edges.append([self.rect.topleft, self.rect.topright])
        self.edges.append([self.rect.topleft, self.rect.bottomleft])
        self.edges.append([self.rect.bottomright, self.rect.topright])
        self.edges.append([self.rect.bottomright, self.rect.bottomleft])

    def render(self, screen):
        pygame.draw.rect(screen, self.ball_colour, self.rect)

    @staticmethod
    def dot(vec_1, vec_2):
        product = vec_1[0] * vec_2[0] + vec_1[1] * vec_2[1]
        return product
