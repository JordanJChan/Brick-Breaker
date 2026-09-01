import pygame

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

    def set_directionX(self, dx):
        """Set horizontal direction to -1 or 1."""
        self.__dir_x = int(dx)

    def set_directionY(self, dy):
        """Set vertical direction to -1 or 1."""
        self.__dir_y = int(dy)
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
