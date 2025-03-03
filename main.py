"""
title: Brick Breaker
author: Jordan Chan
date: 2025-2-6
"""


import pygame
from random import randint

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

    def is_collision(self, width, height, pos):
        """
        Uses the width, height, and position of the external sprite to check for collision
        """
        if pos[0] + width >= self.__x and pos[0] <= self.__x + self.get_width():
            if pos[1] + height >= self.__y and pos[1] <= self.__y + self.get_height():
                return True
        return False
    
    def make_box(self):
        return pygame.Rect(self.__x, self.__y, self.__width, self.__height)



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
        self.__create_ball = False
    
    def can_make_ball(self):
        self.__create_ball = True
        self._SURFACE.fill((52, 171, 235))
    
    def make_ball(self):
        return self.__create_ball


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
        if x_position > (max_x - self.get_width()): # Right
            x_position = max_x - self.get_width()
            self.reverse_directionX()
        if x_position < min_x: # Left
            x_position = min_x
            self.reverse_directionX()
        if y_position > (max_y - self.get_height()): # Bottom
            y_position = max_y - self.get_height()
            self.reverse_directionY()
            return True
        if y_position < min_y: # Top
            y_position = min_y
            self.reverse_directionY()
        self.setPOS(x_position, y_position)
        return False
    

    def brick_collision(self, ball, brick):
        ball_rectangle = ball.make_box()
        brick_rectangle = brick.make_box()

        if ball_rectangle.colliderect(brick_rectangle):

            left_overlap = brick_rectangle.right - ball_rectangle.left
            right_overlap = ball_rectangle.right - brick_rectangle.left
            top_overlap = brick_rectangle.bottom -ball_rectangle.top
            bottom_overlap = ball_rectangle.bottom - brick_rectangle.top

            if left_overlap < right_overlap and left_overlap < top_overlap and left_overlap < bottom_overlap: # Left
                self.reverse_directionX()
            elif right_overlap < left_overlap and right_overlap < top_overlap and right_overlap < bottom_overlap: # Right
                self.reverse_directionX()
            elif top_overlap < left_overlap and top_overlap < right_overlap and top_overlap < bottom_overlap: # Top
                self.reverse_directionY()
            elif bottom_overlap < left_overlap and bottom_overlap < right_overlap and bottom_overlap < top_overlap: # Bottom
                self.reverse_directionY()



def create_bricks(bricks):
    for x in range(0, 7):
        for y in range(0, 5):
            new_brick = Brick(60, 40)
            new_brick.setPOS(70*x+60, 50*y+100)
            lucky = randint(1, 17)
            if lucky == 1:
                new_brick.can_make_ball()
            bricks.append(new_brick)


def main():
    pygame.init() # Initialize pygame

    window = Window("Brick Breaker", 600, 600, 60) # Creates the window

    paddle = Paddle(100, 8)
    paddle.setPOS((window.get_width() - paddle.get_width())/2, 550)
    paddle.set_speed(9)
    

    black_heading = Paddle(window.get_width(), 60, (0, 0, 0))

    ready_text = Text("Press Space to Start")
    ready_text.setPOS(165, 450)

    text1 = Text("Score: 0", "Arial", 30)
    text1.setPOS(0, 0)
    
    text2 = Text("BRICK BREAKER!")
    text2.setPOS(175, 0)

    level_text = Text("Level: 1", "Arial", 20)
    level_text.setPOS(500, 0)

    lives = 3   
    lives_text = Text(f"Lives: {lives}", "Arial", 20)
    lives_text.setPOS(500, 30)

    game_over_text = Text("Game Over. Press Space to Restart")
    game_over_text.setPOS(10, 400)
    
    ball_list = []
    start_ball = Ball(20, 20, (255, 255, 255), (window.get_width() - 20)/2, (window.get_height() - 20)/2 + 70, 2.5) 
    ball_list.append(start_ball)

    bricks = []
    create_bricks(bricks)
    
    power_ups = 1
    power_up_text = Text(f"Power ups: {power_ups}", "Arial", 20)
    power_up_text.setPOS(0, 30)

    game_over = False
    started = False
    score = 0
    level = 1

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        pressed_keys = pygame.key.get_pressed()

        if started == False:
            if pressed_keys[pygame.K_SPACE]:
                started = True
        
        if started == True:
            pressed_keys = pygame.key.get_pressed()
            paddle.horizontal_movement(pressed_keys)
            paddle.checkBoundaries(window.get_width(), window.get_height(), 0, 0)

            if power_ups > 0:
                if pressed_keys[pygame.K_w] == 1:
                    for ball in ball_list:
                        ball.set_speed(2)
                    power_ups -= 1

            for ball in ball_list:
                if ball.checkBoundaries(window.get_width(), window.get_height(), 0, black_heading.get_height()):
                    ball_list.remove(ball)
                    if len(ball_list) == 0:
                        lives -= 1
                        if lives != 0:
                            new_ball = Ball(20, 20, (255, 255, 255), (window.get_width() - 20)/2, (window.get_height() - 20)/2 + 70, 2.5)
                            ball_list.append(new_ball)
                            lives_text.update_text(f"Lives: {lives}")
                        else:
                            lives_text.update_text(f"Lives: {lives}")
                            game_over = True
                        power_ups = 1

                if paddle.is_collision(ball.get_width(), ball.get_height(), ball.get_pos()):
                    ball_pos = ball.get_pos()
                    ball_x = ball_pos[0]

                    paddle_pos = paddle.get_pos()
                    paddle_x = paddle_pos[0]

                    if ball_x >= paddle_x and ball_x + ball.get_width() <= paddle_x + paddle.get_width():
                        ball.reverse_directionY()
                    else:
                        if ball_x >= paddle_x and ball_x + ball.get_width() > paddle_x + paddle.get_width() and ball.get_directionX() == 1:
                            ball.reverse_directionY()
                        elif ball_x + ball.get_width() <= paddle_x + paddle.get_width() and ball_x < paddle_x and ball.get_directionX() == -1:
                            ball.reverse_directionY()
                        else:
                            ball.reverse_directionY()
                            ball.reverse_directionX()
            
                        
                    while paddle.is_collision(ball.get_width(), ball.get_height(), ball.get_pos()):
                        ball.checkBoundaries()
                    
                    ball.set_speed(5.5)
                
                
                for brick in bricks:
                    if brick.is_collision(ball.get_width(), ball.get_height(), ball.get_pos()):
                        ball.brick_collision(ball, brick)
                        if brick.make_ball() is True:
                            brick_position = brick.get_pos()
                            new_ball = Ball(20, 20, (255, 255, 255), brick_position[0], brick_position[1], 5.5)
                            if ball.get_directionX() == -1:
                                new_ball.reverse_directionY()
                            ball_list.append(new_ball)
                        bricks.remove(brick)
                        score += 1
                        text1.update_text(f"Score: {score}")
                        ball.set_speed(5.5)
                
                power_up_text.update_text(f"Power ups: {power_ups}")
                    

        window.clear_screen()

        if started == False:
            window.get_surface().blit(ready_text.get_surface(), ready_text.get_pos())
        
        if len(bricks) == 0:
            level += 1
            level_text.update_text(f"Level: {level}")
            #started = False
            pos_x = 1
            for ball in ball_list:
                ball.setPOS((window.get_width() - 20)/2 +30*pos_x, (window.get_height() - 20)/2 + 70)
                ball.set_speed(2.5)
                if ball.get_directionY() == -1:
                    ball.reverse_directionY()
                if ball.get_directionX() == -1:
                    ball.reverse_directionX()
                pos_x +=1
            paddle.setPOS((window.get_width() - paddle.get_width())/2, 550)
            create_bricks(bricks)
            power_ups = 1
        

        window.get_surface().blit(paddle.get_surface(), paddle.get_pos())
        window.get_surface().blit(black_heading.get_surface(), black_heading.get_pos())
        window.get_surface().blit(text1.get_surface(), text1.get_pos())
        window.get_surface().blit(level_text.get_surface(), level_text.get_pos())
        window.get_surface().blit(lives_text.get_surface(), lives_text.get_pos())
        window.get_surface().blit(power_up_text.get_surface(), power_up_text.get_pos())

        if game_over is True:
            window.get_surface().blit(game_over_text.get_surface(), game_over_text.get_pos())
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_SPACE]:
                break


        window.get_surface().blit(text2.get_surface(), text2.get_pos())

        for ball in ball_list:
            window.get_surface().blit(ball.get_surface(), ball.get_pos())

        for object in bricks:
            window.get_surface().blit(object.get_surface(), object.get_pos())

        window.update_frame()
    
    main()

# --- Main program code ---
if __name__ == "__main__":
   main()







