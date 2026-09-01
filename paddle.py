import pygame
from sprite import mySprite

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
