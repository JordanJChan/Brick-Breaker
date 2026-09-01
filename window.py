import pygame

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
