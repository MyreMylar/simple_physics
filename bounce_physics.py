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

    ball = Ball((400, 300))

    clock = pygame.time.Clock() 

    gravity = [0.0, 1000.0]
    running = True  
    while running:

        frame_time = clock.tick(60)
        time_delta = frame_time/1000.0
             
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            # --------------------------------------------------------
            # Challenge 2
            # --------------
            #
            # Add a keyboard key that creates
            # a new ball at a random point on the screen
            # each time you press it.
            #
            # You'll need to:
            #
            # - Create a list to hold the balls
            #   instead of the current single 'ball' variable and
            #   update the code in this file.
            #
            # - add a new if statement to check your key.
            #
            # - Use the random.randint(a, b) function where 'a' is
            #   the lowest value and 'b' is the highest value you want
            #   to get a number between.
            # --------------------------------------------------------

            # --------------------------------------------------------
            # Challenge 3
            # -------------
            #
            # Now see if you can update the code you just finished
            # to randomly change the colour of the balls you create.
            #
            # Remember you can create a pygame.Color variable by passing
            # it three numbers between 0 and 255 representing red, green
            # and blue respectively.
            # --------------------------------------------------------
            if event.type == KEYDOWN:
                if event.key == K_r:
                    ball.reset()

            for bat in bats:
                bat.process_event(event)
                        
        screen.blit(background, (0, 0))  # draw the background surface to our screen

        for wall in walls:
            wall.render(screen)

        for bat in bats:
            bat.update(time_delta)
            bat.render(screen)

        ball.update(time_delta, gravity, walls, bats)
        total_ball_bounces = ball.number_of_bounces

        ball.render(screen)

        bounce_text = font.render("Bounces: " + str(total_ball_bounces), True, pygame.Color("#FFFFFF"))
        screen.blit(bounce_text, bounce_text.get_rect(x=650, y=30))
                
        pygame.display.flip()  # flip all our drawn stuff onto the screen

    pygame.quit()  # exited game loop so quit pygame


if __name__ == '__main__':
    main()
