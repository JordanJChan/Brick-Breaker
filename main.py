"""
title: Brick Breaker
author: Jordan Chan
date: 2025-2-6
"""

import pygame

class window:

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

class text:
    pass

class mySprite:
    pass

class paddle:
    pass

class ball:
    pass






