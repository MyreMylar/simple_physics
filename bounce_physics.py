import pygame
from pygame.locals import *

from game.wall import Wall
from game.bat import Bat, ControlScheme

from ball import Ball

import random


def main():
   
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Bounce Physics')

    background = pygame.Surface(screen.get_size())
    background = background.convert(screen)
    background.fill((0, 0, 0))
    
    font = pygame.font.Font(None, 26) 

    walls = [Wall((10, 10), (790, 20)), Wall((10, 580), (790, 590)),
             Wall((10, 10), (20, 590)), Wall((780, 10), (790, 590))]

    bats = []

    control_scheme1 = ControlScheme()
    control_scheme1.left = K_LEFT
    control_scheme1.right = K_RIGHT

    bats.append(Bat((400, 500), control_scheme1))

    balls = [Ball((400, 300), pygame.Color(255,255,255))]

    total_ball_bounces = 0

    clock = pygame.time.Clock() 

    gravity = [0.0, 400.0]
    running = True  
    while running:

        frame_time = clock.tick(60)
        time_delta = frame_time/1000.0
             
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            if event.type == KEYDOWN:
                if event.key == K_r:
                    for ball in balls:
                        ball.reset()

                if event.key == K_SPACE:
                    x_pos = random.randint(20, 780)
                    y_pos = random.randint(20, 580)
                    ball_colour = pygame.Color(random.randint(100, 255),
                                               random.randint(100, 255),
                                               random.randint(100, 255))
                    balls.append(Ball((x_pos, y_pos), ball_colour))

            for bat in bats:
                bat.process_event(event)
                        
        screen.blit(background, (0, 0))  # draw the background surface to our screen

        for wall in walls:
            wall.render(screen)

        for bat in bats:
            bat.update(time_delta)
            bat.render(screen)

        total_ball_bounces = 0
        for ball in balls:
            ball.update(time_delta, gravity, walls, bats)
            total_ball_bounces += ball.number_of_bounces
            ball.render(screen)

        bounce_text = font.render("Bounces: " + str(total_ball_bounces), True, pygame.Color(255, 255, 255))
        screen.blit(bounce_text, bounce_text.get_rect(x=650, y=30))
                
        pygame.display.flip()  # flip all our drawn stuff onto the screen

    pygame.quit()  # exited game loop so quit pygame


if __name__ == '__main__':
    main()