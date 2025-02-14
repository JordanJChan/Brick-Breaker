"""
title: Brick Breaker
author: Jordan Chan
date: 2025-2-6
"""


import pygame


class Window:

    def __init__(self, title, width, height, fps):
        self.__title = title
        self.__fps = fps
        self.__width = width
        self.__height = height
        self.__screen_dimensions = (self.__width, self.__height)
        self.__Clock = pygame.time.Clock()
        self.__surface = pygame.display.set_mode(self.__screen_dimensions)
        self.__surface.fill((128, 128, 128))
        pygame.display.set_caption(self.__title)


    def clear_screen(self):
        self.__surface.fill((128, 128, 128))


    def update_frame(self):
        self.__Clock.tick(self.__fps)
        pygame.display.flip()


    def get_surface(self):
        return self.__surface


    def get_width(self):
        return self.__width


    def get_height(self):
        return self.__height


class mySprite:

    def __init__(self, width=1, height=1, color=(255, 255, 255), x=0, y=0, speed=8):
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


    def setX(self, x):
        self.__x = x
        self.__pos = (self.__x, self.__y)

    def setY(self, y):
        self.__y = y
        self.__pos = (self.__x, self.__y)

    def setPOS(self, x, y):
        self.setX(x)
        self.setY(y)

    def set_speed(self, speed):
        self.__speed = speed

    def set_color(self, color):
        self._color = color


    def get_pos(self):
        return self.__pos

    def get_surface(self):
        return self._SURFACE

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def horizontal_movement(self, pressed_keys):
        if pressed_keys[pygame.K_d] == 1:
            self.__x += self.__speed
        if pressed_keys[pygame.K_a] == 1:
            self.__x -= self.__speed

        self.__pos = (self.__x, self.__y)

    def checkBoundaries(self, max_x, max_y, min_x=0, min_y=0):
        if self.__x > max_x - self.get_width():
            self.__x = max_x - self.get_width()
        if self.__x < min_x:
            self.__x = min_x

        self.__pos = (self.__x, self.__y)



class Text(mySprite):
    def __init__(self, text, f_family="Arial", f_size=36, x=0, y=0):
        mySprite.__init__(self, x=x, y=y)
        self.__text = text
        self.__font_family = f_family
        self.__font_size = f_size
        self.__font = pygame.font.SysFont(self.__font_family, self.__font_size)
        self._SURFACE = self.__font.render(self.__text, True, self._color)

class Paddle(mySprite):
    def __init__(self, width=1, height=1, color=(255, 255, 255)):
        mySprite.__init__(self, width, height, color)
        self._SURFACE = pygame.Surface(self._dim, pygame.SRCALPHA, 32)
        self._SURFACE.fill(self._color)


class Ball(mySprite):
    def __init__(self, width=1, height=1, color=(255, 255, 255), x=0, y=0, speed=8):
        mySprite.__init__(self, width, height, color, x, y, speed)
        self._SURFACE = pygame.Surface(self._dim, pygame.SRCALPHA, 32)
        self._SURFACE.fill(self._color)
        self.__DirX = 1
        self.__DirY = 1

    def checkBoundaries(self, max_x, max_y, min_x=0, min_y=0):
        mySprite.checkBoundaries(self, max_x, max_y, min_x=0, min_y=60)
        self.__x += self.__speed * self.__DirX
        self.__y += self.__speed * self.__DirY
        if self.__x > (max_x - self.__width):
            self.__x = max_x - self.__width
            self.__DirX = -1
        if self.__x < min_x:
            self.__x = min_x
            self.__DirX = 1
        if self.__y > (max_y - self.__height):
            self.__y = max_y - self.__height
            self.__DirY = -1
        if self.__y < min_y:
            self.__y = min_y
            self.__DirY = 1
        self.__pos = (self.__x, self.__y)


if __name__ == "__main__":
    pygame.init()

    window = Window("Brick Breaker", 600, 600, 30)

    paddle = Paddle(100, 20)
    paddle.setPOS((window.get_width() - paddle.get_width())/2, 550)

    black_heading = Paddle(window.get_width(), 60, (0, 0, 0))
    #black_heading.setPOS((window.get_width() - paddle.get_width())/2, 0)

    text1 = Text("Score: ")
    text1.setPOS(0, 0)

    text2 = Text("BRICK BREAKER!")
    text2.setPOS(175, 0)

    ball = Ball(10, 10)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pressed_keys = pygame.key.get_pressed()
        paddle.horizontal_movement(pressed_keys)
        paddle.checkBoundaries(window.get_width(), window.get_height(), 0, 0)

        ball.checkBoundaries(window.get_width(), window.get_height(), 0, black_heading.get_height())


        window.clear_screen()


        window.get_surface().blit(paddle.get_surface(), paddle.get_pos())
        window.get_surface().blit(black_heading.get_surface(), black_heading.get_pos())
        window.get_surface().blit(text1.get_surface(), text1.get_pos())

        window.get_surface().blit(text2.get_surface(), text2.get_pos())

        window.get_surface().blit(ball.get_surface(), ball.get_pos())

        window.update_frame()
















