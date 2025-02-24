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

    def reverse_directionX(self):
        self.__dir_x = self.__dir_x*-1

    def reverse_directionY(self):
        self.__dir_y = self.__dir_y*-1

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
    
    def update_text(self, new_text):
        self.__text = new_text
        self._SURFACE = self.__font.render(self.__text, True, self._color)

class Paddle(mySprite):
    def __init__(self, width=1, height=1, color=(255, 255, 255)):
        mySprite.__init__(self, width, height, color)
        self._SURFACE = pygame.Surface(self._dim, pygame.SRCALPHA, 32)
        self._SURFACE.fill(self._color)

class Brick(mySprite):
    def __init__(self, width=70, height=30, color=(255, 255, 255)):
        mySprite.__init__(self, width, height, color)
        self._SURFACE = pygame.Surface(self._dim, pygame.SRCALPHA, 32)
        self._SURFACE.fill(self._color)


class Ball(mySprite):
    def __init__(self, width=1, height=1, color=(255, 255, 255), x=0, y=0, speed=8):
        mySprite.__init__(self, width, height, color, x, y, speed)
        self._SURFACE = pygame.Surface(self._dim, pygame.SRCALPHA, 32)
        self._SURFACE.fill(self._color)


    def checkBoundaries(self, max_x=600, max_y=600, min_x=0, min_y=0):
        mySprite.checkBoundaries(self, max_x=600, max_y=600, min_x=0, min_y=60)
        position = self.get_pos()
        x_position = position[0]
        y_position = position[1]
        speed = self.get_speed()

        x_position += speed * self.get_directionX()
        y_position += speed * self.get_directionY()
        if x_position > (max_x - self.get_width()):
            x_position = max_x - self.get_width()
            self.reverse_directionX()
        if x_position < min_x:
            x_position = min_x
            self.reverse_directionX()
        if y_position > (max_y - self.get_height()):
            y_position = max_y - self.get_height()
            self.reverse_directionY()
        if y_position < min_y:
            y_position = min_y
            self.reverse_directionY()
        self.setPOS(x_position, y_position)

    def move(self):
        position = self.get_pos()
        x_position = position[0]
        y_position = position[1]
        speed = self.get_speed()
        x_position += speed * self.get_directionX()
        y_position += speed * self.get_directionY()
        self.setPOS(x_position, y_position)

    def paddle_collision(self, paddle_width, paddle_height, paddle_pos):
        ball_pos = self.get_pos()
        ball_x = ball_pos[0]
        ball_y = ball_pos[1]

        paddle_x = paddle_pos[0]
        paddle_y = paddle_pos[1]
        
        if (ball_y + self.get_height() >= paddle_y) and (ball_y <= paddle_y + paddle_height):
            if (ball_x + self.get_width() >= paddle_x) and (ball_x <= paddle_x + paddle_width):

                if ball_y + self.get_height() <= paddle_y + self.get_speed(): # Hit the top
                    print("Hit the top")
                    self.reverse_directionY()
                # elif ball_y - self.get_height() <= paddle_y + paddle_height: # Hit the bottom
                #     print("Hit the bottom")
                #     self.reverse_directionY()
                elif ball_y >= paddle_y - self.get_speed():
                    print("hit the bottom")
                    self.reverse_directionY()
                # elif ball_x + self.get_width() >= paddle_x + self.get_speed(): # Hit the left
                #     print("Hit the left")
                #     self.reverse_directionX()
                #     self.reverse_directionY()
                # elif ball_x - self.get_width() <= paddle_x + self.get_speed(): # Hit the right
                #     print("Hit the right")
                #     self.reverse_directionX()
                #     self.reverse_directionY()
                else:
                    print("Hit the left or right")
                    self.reverse_directionY()
                    self.reverse_directionX()

                while (ball_y + self.get_height() >= paddle_y) and (ball_y <= paddle_y + paddle_height) and (ball_x + self.get_width() >= paddle_x) and (ball_x <= paddle_x + paddle_width):
                    self.checkBoundaries()
                    new_pos = self.get_pos()
                    ball_x = new_pos[0]
                    ball_y = new_pos[1]


    def collision(self, object_width, object_height, object_pos):
        ball_pos = self.get_pos()
        ball_x = ball_pos[0]
        ball_y = ball_pos[1]

        object_x = object_pos[0]
        object_y = object_pos[1]

        if (ball_y + self.get_height() >= object_y) and (ball_y <= object_y + object_height):
            if (ball_x + self.get_width() >= object_x) and (ball_x <= object_x + object_width):
                return True
        return False



# --- Main program code ---
if __name__ == "__main__":
    pygame.init() # Initialize pygame

    window = Window("Brick Breaker", 600, 600, 60) # Creates the window

    paddle = Paddle(100, 10)
    paddle.setPOS((window.get_width() - paddle.get_width())/2, 550)

    black_heading = Paddle(window.get_width(), 60, (0, 0, 0))
    #black_heading.setPOS((window.get_width() - paddle.get_width())/2, 0)

    text1 = Text("Score: 0")
    text1.setPOS(0, 0)
    

    text2 = Text("BRICK BREAKER!")
    text2.setPOS(175, 0)

    ball = Ball(20, 20, (255, 255, 255), (window.get_width() - 20)/2, (window.get_height() - 20)/2, 5)

    bricks = []

    for x in range(0, 7):
        for y in range(0, 5):
            new_brick = Brick(60, 40)
            new_brick.setPOS(70*x+60, 50*y+100)
            bricks.append(new_brick)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pressed_keys = pygame.key.get_pressed()
        paddle.horizontal_movement(pressed_keys)
        paddle.checkBoundaries(window.get_width(), window.get_height(), 0, 0)

        ball.checkBoundaries(window.get_width(), window.get_height(), 0, black_heading.get_height())
        ball.paddle_collision(paddle.get_width(), paddle.get_height(), paddle.get_pos())


        window.clear_screen()


        window.get_surface().blit(paddle.get_surface(), paddle.get_pos())
        window.get_surface().blit(black_heading.get_surface(), black_heading.get_pos())
        window.get_surface().blit(text1.get_surface(), text1.get_pos())

        window.get_surface().blit(text2.get_surface(), text2.get_pos())

        window.get_surface().blit(ball.get_surface(), ball.get_pos())

        for object in bricks:
            window.get_surface().blit(object.get_surface(), object.get_pos())

        window.update_frame()
















