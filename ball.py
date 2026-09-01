import pygame
from sprite import mySprite
from random import choice

class Ball(mySprite):
    """
    Class to make the ball
    """
    def __init__(self, width=1, height=1, color=(255, 255, 255), x=0, y=0, speed=8):
        mySprite.__init__(self, width, height, color, x, y, speed)
        self._SURFACE = pygame.Surface(self._dim, pygame.SRCALPHA, 32)
        self._SURFACE.fill(self._color)
        # Start moving downwards and choose random left or right horizontal direction
        try:
            self.set_directionY(1)
            self.set_directionX(choice([-1, 1]))
        except Exception:
            # In case mySprite hasn't exposed setters, fall back to name-mangled access
            try:
                self._mySprite__dir_y = 1
                self._mySprite__dir_x = choice([-1, 1])
            except Exception:
                pass


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
