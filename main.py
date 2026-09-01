"""
title: Brick Breaker
author: Jordan Chan
date: 2025-2-6
"""

import pygame
from random import randint # Use to pick a random number
import time # Use to keep track of the time

from window import Window
from sprite import mySprite
from text import Text
from paddle import Paddle
from brick import Brick
from ball import Ball


def create_bricks(bricks):
    """
    Make the bricks
    :param bricks: list
    :return: None
    """
    for x in range(0, 7): # Makes 35 bricks in total
        for y in range(0, 5):
            new_brick = Brick(60, 40) # Make new brick
            new_brick.setPOS(70*x+60, 50*y+100) # set the position
            lucky = randint(1, 17) # Decide if the brick can spawn a ball
            if lucky == 1: # Brick can make a ball
                new_brick.can_make_ball()
            bricks.append(new_brick) # Add the brick into the list for bricks


def main():
    """
    Main function
    """
    pygame.init() # Initialize pygame

    window = Window("Brick Breaker", 600, 600, 60) # Creates the window

    paddle = Paddle(100, 8) # Creates paddle
    paddle.setPOS((window.get_width() - paddle.get_width())/2, 550) # Sets the paddle position
    paddle.set_speed(9)
    

    black_heading = Paddle(window.get_width(), 60, (0, 0, 0)) # Make the black heading for the top of the screen

    ready_text = Text("Press Space to Start") # Start text
    ready_text.setPOS(165, 450)

    text1 = Text("Score: 0", "Arial", 30) # Score text
    text1.setPOS(0, 0)
    
    text2 = Text("BRICK BREAKER!") # Heading text
    text2.setPOS(175, 0)

    level_text = Text("Level: 1", "Arial", 20) # Level text
    level_text.setPOS(500, 0)

    lives = 3  # Variable to keep track of the lives
    lives_text = Text(f"Lives: {lives}", "Arial", 20) # Text displaying the lives
    lives_text.setPOS(500, 30)

    game_over_text = Text("Game Over. Press Space to Restart") # Text to show the game ended
    game_over_text.setPOS(60, 400)
    
    ball_list = [] # Store the ball objects. Example of aggregation
    start_ball = Ball(20, 20, (255, 255, 255), (window.get_width() - 20)/2, (window.get_height() - 20)/2 + 70, 2.5)  # First ball
    ball_list.append(start_ball)

    bricks = [] # Store the brick objects
    create_bricks(bricks) # Make bricks
    
    power_ups = 1 # Keeps track of power ups left
    paddle_extend = False # Keep track of if the paddle is extended
    power_up_text = Text(f"Power ups: {power_ups}", "Arial", 20) # Shows how many power ups the user can use
    power_up_text.setPOS(0, 30)

    game_over = False # Keeps track of if the game has ended
    started = False # Keeps track of if the game has started
    score = 0 # Track the score
    level = 1 # Track the level

    while True: # Kee running until the user quits

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # User click the red x to leave
                pygame.quit()
                exit()
        
        pressed_keys = pygame.key.get_pressed() # Get key pressed

        if started == False: # Game has not yet started
            if pressed_keys[pygame.K_SPACE]: # Start the game after the user pressees space
                started = True
        
        if started == True: # Ga,e started
            pressed_keys = pygame.key.get_pressed() # Get key press
            paddle.horizontal_movement(pressed_keys) # Check for the paddle movements
            paddle.checkBoundaries(window.get_width(), window.get_height(), 0, 0) # Check for the paddle's boundaries

            if power_ups > 0: # Player can use power up
                if pressed_keys[pygame.K_w] == 1: # Pressed the "w" key
                    for ball in ball_list:
                        ball.set_speed(2) # Slow down the ball's speed
                    power_ups -= 1 # Make it so the user can't use power ups anymore
                elif pressed_keys[pygame.K_s] == 1: # Pressed the "s" key
                    paddle_extend = True # Extend the paddle
                    start_time = time.time() # Get the current time
                    power_ups -= 1 # Make it so player can't use power ups anymore
                
            if paddle_extend is True:
                paddle.change_width(150) # Extend paddle
                if time.time() - start_time > 8: # Can only extend for eight seconds
                    paddle.change_width(100) # Change width back to normal
                    paddle_extend = False # Paddle no longer extended


            for ball in ball_list:
                if ball.checkBoundaries(window.get_width(), window.get_height(), 0, black_heading.get_height()): # Ball fell to the bottom of the screen
                    ball_list.remove(ball) # Remove ball
                    if len(ball_list) == 0: # No more balls
                        lives -= 1 # Take off a life
                        if lives != 0: # Player still have lives left
                            new_ball = Ball(20, 20, (255, 255, 255), (window.get_width() - 20)/2, (window.get_height() - 20)/2 + 70, 2.5) # Make new ball
                            ball_list.append(new_ball)
                            lives_text.update_text(f"Lives: {lives}") # Display number of life left
                        else: # Player has not life left
                            lives_text.update_text(f"Lives: {lives}")
                            game_over = True # Game ends
                        power_ups = 1 # Make it so the user can use power ups

                if paddle.is_collision(ball.get_width(), ball.get_height(), ball.get_pos()): # Ball and paddle collision
                    ball_pos = ball.get_pos()
                    ball_x = ball_pos[0]

                    paddle_pos = paddle.get_pos()
                    paddle_x = paddle_pos[0]

                    if ball_x >= paddle_x and ball_x + ball.get_width() <= paddle_x + paddle.get_width(): # Hit the top or bottom of the paddle
                        ball.reverse_directionY()
                    else:
                        if ball_x >= paddle_x and ball_x + ball.get_width() > paddle_x + paddle.get_width() and ball.get_directionX() == 1: # Hit the right corner of paddle
                            ball.reverse_directionY()
                        elif ball_x + ball.get_width() <= paddle_x + paddle.get_width() and ball_x < paddle_x and ball.get_directionX() == -1: # Hit the left corner of paddle
                            ball.reverse_directionY()
                        else: # Hit the left or right side of the paddle
                            ball.reverse_directionY()
                            ball.reverse_directionX()
            
                        
                    while paddle.is_collision(ball.get_width(), ball.get_height(), ball.get_pos()): # Ball and paddle hitting each other
                        ball.checkBoundaries() # Move the ball out
                    
                    ball.set_speed(5.5) # Speed up the ball
                
                
                for brick in bricks:
                    if brick.is_collision(ball.get_width(), ball.get_height(), ball.get_pos()): # Ball and brick collision
                        ball.brick_collision(ball, brick) # Check which side hit
                        if brick.make_ball() is True: # Brick can spawn ball
                            brick_position = brick.get_pos()
                            new_ball = Ball(20, 20, (255, 255, 255), brick_position[0], brick_position[1], 5.5) # Make new ball at the brick position
                            if ball.get_directionX() == -1: # Make the new ball go in the same direction as the ball that hit the brick
                                new_ball.reverse_directionY()
                            ball_list.append(new_ball)
                        bricks.remove(brick) # Remove brick
                        score += 1 # Increase score
                        text1.update_text(f"Score: {score}")
                        ball.set_speed(5.5)
                
                power_up_text.update_text(f"Power ups: {power_ups}")
                    

        window.clear_screen()

        if started == False: # Game has not yet started
            window.get_surface().blit(ready_text.get_surface(), ready_text.get_pos()) # Display start text
        
        if len(bricks) == 0: # No more bricks left
            level += 1 # Next level
            level_text.update_text(f"Level: {level}")
            pos_x = 1
            for ball in ball_list:
                ball.setPOS((window.get_width() - 20)/2 +30*pos_x, (window.get_height() - 20)/2 + 70) # MOve the balls to the start position
                ball.set_speed(2.5) # Slow it down
                if ball.get_directionY() == -1: # Make the ball go to bottom right corner
                    ball.reverse_directionY()
                if ball.get_directionX() == -1: # Make the ball go to bottom right corner
                    ball.reverse_directionX()
                pos_x +=1
            paddle.setPOS((window.get_width() - paddle.get_width())/2, 550) # Set paddle back to middle
            create_bricks(bricks) # Make new bricks
            power_ups = 1 # Increase power up by one
        
        # Blit the sprites
        window.get_surface().blit(paddle.get_surface(), paddle.get_pos())
        window.get_surface().blit(black_heading.get_surface(), black_heading.get_pos())
        window.get_surface().blit(text1.get_surface(), text1.get_pos())
        window.get_surface().blit(level_text.get_surface(), level_text.get_pos())
        window.get_surface().blit(lives_text.get_surface(), lives_text.get_pos())
        window.get_surface().blit(power_up_text.get_surface(), power_up_text.get_pos())

        if game_over is True: # Game ended
            window.get_surface().blit(game_over_text.get_surface(), game_over_text.get_pos()) # Display end text
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_SPACE]: # User wants to play again
                break


        window.get_surface().blit(text2.get_surface(), text2.get_pos())

        for ball in ball_list: # Blit the balls
            window.get_surface().blit(ball.get_surface(), ball.get_pos())

        for object in bricks: # Blit the bricks
            window.get_surface().blit(object.get_surface(), object.get_pos())

        window.update_frame()
    
    main() # Use recursion to retart the game

# --- Main program code ---
if __name__ == "__main__":
   main() # Run the main function







