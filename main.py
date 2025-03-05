"""
title: Brick Breaker
author: Jordan Chan
date: 2025-2-6
"""

import pygame
from random import randint # Use to pick a random number
import time # Use to keep track of the time

class Window:
    """
    Class to make the game window
    """
    def __init__(self, title, width, height, fps):
        self.__title = title # Window name
        self.__fps = fps 
        self.__width = width # Window width
        self.__height = height # Window height
        self.__screen_dimensions = (self.__width, self.__height) # # Window dimensions
        self.__Clock = pygame.time.Clock()
        self.__surface = pygame.display.set_mode(self.__screen_dimensions) # Any time a double underscore is used is an example of encapsulation
        self.__surface.fill((128, 128, 128)) # Make the background color gray
        pygame.display.set_caption(self.__title)


    def clear_screen(self): #  Make the screen gray
        self.__surface.fill((128, 128, 128))


    def update_frame(self): # Change the frame of the window
        self.__Clock.tick(self.__fps)
        pygame.display.flip()


    def get_surface(self): # Get the surface of the window
        return self.__surface


    def get_width(self):
        return self.__width # Returns the width of the window


    def get_height(self):
        return self.__height # Returns the height of the window


class mySprite: # Abstraction in mySprite. Only set up the necessary attributes and methods.
    """
    Template to create sprites
    """

    def __init__(self, width=1, height=1, color=(255, 255, 255), x=0, y=0, speed=8):
        # attributes
        self.__width = width
        self.__height = height
        self._dim = (self.__width, self.__height)
        self.__x = x
        self.__y = y
        self.__pos = (self.__x, self.__y)
        self._color = color
        self.__speed = speed
        self._SURFACE = pygame.Surface
        self.__dir_x = 1
        self.__dir_y = 1
    
    # Setters
    def set_width(self, new_width):
        """
        Change the width
        :param new_width: int
        :return: None
        """
        self.__width = new_width 

    def setX(self, x):
        """
        Change x-position
        :param x: int
        :return: None
        """
        self.__x = x
        self.__pos = (self.__x, self.__y) 

    def setY(self, y):
        """
        Change y-position
        :param y: int
        :return: None
        """
        self.__y = y
        self.__pos = (self.__x, self.__y) 

    def setPOS(self, x, y): 
        """
        Change position
        :param x: int
        :param y: int
        :return: None
        """
        self.setX(x)
        self.setY(y)

    def set_speed(self, speed):
        """
        Change speed
        :param speed: float
        :return: None
        """
        self.__speed = speed 

    def set_color(self, color):
        """
        Change color
        :param color: tuple
        :return: None
        """
        self._color = color 

    def reverse_directionX(self):
        self.__dir_x = self.__dir_x*-1 # Change the y-direction

    def reverse_directionY(self):
        self.__dir_y = self.__dir_y*-1 # Change the x-direction

    # Getters
    def get_pos(self):
        return self.__pos 

    def get_surface(self):
        return self._SURFACE

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_directionX(self):
        return self.__dir_x

    def get_directionY(self):
        return self.__dir_y

    def get_speed(self):
        return self.__speed

    def horizontal_movement(self, pressed_keys):
        """
        Method to control the horizontal movement of the paddle
        :param pressed_keys: dict
        :return: None
        """
        if pressed_keys[pygame.K_d] == 1: # Move right
            self.__x += self.__speed
        if pressed_keys[pygame.K_a] == 1: # Left
            self.__x -= self.__speed

        self.__pos = (self.__x, self.__y) # Change the position

    def checkBoundaries(self, max_x, max_y, min_x=0, min_y=0):
        """
        Method for checking boundaries of the paddle
        """
        if self.__x > max_x - self.get_width(): # Right boundary
            self.__x = max_x - self.get_width()
        if self.__x < min_x: # Left boundary
            self.__x = min_x

        self.__pos = (self.__x, self.__y)

    def is_collision(self, width, height, pos):
        """
        Uses the width, height, and position of the external sprite to check for collision
        :param width: int
        :param height: int
        :param pos: tuple
        :return: None
        """
        if pos[0] + width >= self.__x and pos[0] <= self.__x + self.get_width(): # Hits the top or bottom
            if pos[1] + height >= self.__y and pos[1] <= self.__y + self.get_height(): # Hits the left or right
                return True
        return False # No collision
    
    def make_box(self):
        return pygame.Rect(self.__x, self.__y, self.__width, self.__height) # Returns the sprite as pygame.Rect() object


class Text(mySprite):
    """
    Class to make the text sprites
    """
    def __init__(self, text, f_family="Arial", f_size=36, x=0, y=0):
        # Attributes
        mySprite.__init__(self, x=x, y=y)
        self.__text = text
        self.__font_family = f_family
        self.__font_size = f_size
        self.__font = pygame.font.SysFont(self.__font_family, self.__font_size)
        self._SURFACE = self.__font.render(self.__text, True, self._color)
    
    def update_text(self, new_text):
        """
        Method to update the message the text displays
        :param new_text: str
        :return: None
        """
        self.__text = new_text
        self._SURFACE = self.__font.render(self.__text, True, self._color)

class Paddle(mySprite):
    """
    Class for the paddle
    """
    def __init__(self, width=1, height=1, color=(255, 255, 255)):
        mySprite.__init__(self, width, height, color)
        self._SURFACE = pygame.Surface(self._dim, pygame.SRCALPHA, 32)
        self._SURFACE.fill(self._color)
    
    def change_width(self, new_width):
        """
        Method to change the length of the paddle
        :param new_width: float
        :return: None
        """
        self._SURFACE = pygame.transform.scale(self._SURFACE, (new_width, self.get_height()))
        self.set_width(new_width)

class Brick(mySprite):
    """
    Class for the brick
    """
    def __init__(self, width=70, height=30, color=(255, 255, 255)):
        mySprite.__init__(self, width, height, color)
        self._SURFACE = pygame.Surface(self._dim, pygame.SRCALPHA, 32)
        self._SURFACE.fill(self._color)
        self.__create_ball = False # By default, bricks cannot create balls
    
    def can_make_ball(self):
        """
        Make it so the ball can spawn from the brick
        """
        self.__create_ball = True # The brick can make a ball
        self._SURFACE.fill((52, 171, 235)) # Change the color
    
    def make_ball(self):
        """
        Getter method to check if the brick can make ball
        :return: bool
        """
        return self.__create_ball


class Ball(mySprite):
    """
    Class to make the ball
    """
    def __init__(self, width=1, height=1, color=(255, 255, 255), x=0, y=0, speed=8):
        mySprite.__init__(self, width, height, color, x, y, speed)
        self._SURFACE = pygame.Surface(self._dim, pygame.SRCALPHA, 32)
        self._SURFACE.fill(self._color)


    def checkBoundaries(self, max_x=600, max_y=600, min_x=0, min_y=0):
        """
        Method to check for the ball collision with the screen edges and move the ball
        """
        mySprite.checkBoundaries(self, max_x=600, max_y=600, min_x=0, min_y=60) # Polymorphism. The ball boundaries are different from those of the paddle
        position = self.get_pos() # Get ball position
        x_position = position[0] # Ball x-position
        y_position = position[1] # Ball y-position
        speed = self.get_speed() # Get the ball speed

        x_position += speed * self.get_directionX() # Move the ball horizontally
        y_position += speed * self.get_directionY() # Move the ball vertically
        if x_position > (max_x - self.get_width()): # Hits the right side of the screen
            x_position = max_x - self.get_width()
            self.reverse_directionX()
        if x_position < min_x: # Hits the left side of the screen
            x_position = min_x
            self.reverse_directionX()
        if y_position > (max_y - self.get_height()): # Hits the bottom of the screen
            y_position = max_y - self.get_height()
            self.reverse_directionY()
            return True # Lets our program know that it hit the bottom
        if y_position < min_y: # Hits the top of the screen
            y_position = min_y
            self.reverse_directionY()
        self.setPOS(x_position, y_position) # Change the ball position
        return False # Did not hit the bottom of the screen
    

    def brick_collision(self, ball, brick):
        """
        Method to check ball collision with the brick
        :param ball: object
        :param brick: object
        :return: None
        """
        ball_rectangle = ball.make_box() # Make the ball sprite as a pygame.Rect() object
        brick_rectangle = brick.make_box() # Make the brick sprite as a pygame.Rect() object

        if ball_rectangle.colliderect(brick_rectangle): # Collision between the brick and ball

            left_overlap = brick_rectangle.right - ball_rectangle.left # Check the ball and brick overlaps more on the left of the ball
            right_overlap = ball_rectangle.right - brick_rectangle.left # Check the ball and brick overlaps more on the right of the ball
            top_overlap = brick_rectangle.bottom -ball_rectangle.top # Check the ball and brick overlaps more on the top of the ball
            bottom_overlap = ball_rectangle.bottom - brick_rectangle.top # Check the ball and brick overlaps more on the bottom of the ball

            if left_overlap < right_overlap and left_overlap < top_overlap and left_overlap < bottom_overlap: # Left collision
                self.reverse_directionX()
            elif right_overlap < left_overlap and right_overlap < top_overlap and right_overlap < bottom_overlap: # Right collision
                self.reverse_directionX()
            elif top_overlap < left_overlap and top_overlap < right_overlap and top_overlap < bottom_overlap: # Top collision
                self.reverse_directionY()
            elif bottom_overlap < left_overlap and bottom_overlap < right_overlap and bottom_overlap < top_overlap: # Bottom collision
                self.reverse_directionY()


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
    game_over_text.setPOS(10, 400)
    
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







