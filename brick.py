import pygame
from sprite import mySprite

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
