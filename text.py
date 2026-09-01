import pygame
from sprite import mySprite

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
