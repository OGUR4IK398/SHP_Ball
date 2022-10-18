import pygame, sys
from random import randint

BLACK = 0, 0, 0
GREEN = 0, 255, 0
pygame.init()

size = width, height = 800, 600
screen = pygame.display.set_mode(size)


class Platform:
    def __init__(self):
        self.width = 100
        self.height = 20
        self.y = 490
        self.x_pos = 350
        self.allowed_left_movement = False
        self.allowed_right_movement = False

    def update(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x_pos, self.y, self.width, self.height), 5)

    def shift(self):
        if self.allowed_right_movement and self.x_pos < width - self.width:
            self.x_pos += 2
        if self.allowed_left_movement and self.x_pos > 0:
            self.x_pos -= 2

    def check_collision_platform(self, ball):
        return ball.ballrect.y + ball.ballrect.width == self.y \
                and (ball.ballrect.x in range(self.x_pos, self.x_pos + self.width + 1)
                     or ball.ballrect.x + ball.ballrect.width in range(self.x_pos, self.x_pos + self.width + 1))

    def collide(self, ball):
        #  and ball.is_out_of_platform
        if self.check_collision_platform(ball):
            ball.speed[1] *= -1


class Ball:
    def __init__(self):
        self.speed = [1, 1]
        self.ball = pygame.image.load("basketball.png")
        self.ballrect = self.ball.get_rect()
        self.ballrect.x = randint(0, width - self.ballrect.width)
        self.ballrect.y = randint(0, height - self.ballrect.height - 300)

    def set_pos(self, pos: list):
        self.ballrect.x = pos[0]
        self.ballrect.y = pos[1]

    def shift(self):
        self.ballrect.x += self.speed[0]
        self.ballrect.y += self.speed[1]
        if (self.ballrect.x < 0) or (self.ballrect.x + self.ballrect.width > width):
            self.speed[0] *= -1
        if self.ballrect.y < 0:
            self.speed[1] *= -1

    def collide_ball(self, b):
        x1 = self.ballrect.centerx
        y1 = self.ballrect.centery
        x2 = b.ballrect.centerx
        y2 = b.ballrect.centery
        r = ((x1 - x2) ** 2 + (y1 - y2) ** 2)**0.5
        return r < self.ballrect.width

    def collide(self):
        self.speed[0] *= -1
        self.speed[1] *= -1

    def update(self, screen):
        screen.blit(self.ball, self.ballrect)


def check_collisions(objects):
    for i in range(len(objects)):
        for j in range(i + 1, len(objects)):
            is_collision = objects[i].collide_ball(objects[j])
            if is_collision:
                objects[i].collide()
                objects[j].collide()


def collisions_with_platform(platform, objects):
    for ball in objects:
        platform.collide(ball)


def main():
    game_over = False
    objects = []
    objects.append(Ball())
    platform = Platform()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    platform.allowed_left_movement = True
                if event.key == pygame.K_d:
                    platform.allowed_right_movement = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    platform.allowed_left_movement = False
                if event.key == pygame.K_d:
                    platform.allowed_right_movement = False
        screen.fill(BLACK)

        platform.shift()
        platform.update(screen)

        # логика
        for i in range(len(objects)):
            objects[i].shift()

        check_collisions(objects)
        collisions_with_platform(platform, objects)

        for object in objects:
            object.update(screen)
        pygame.display.flip()

        pygame.time.wait(2)


if __name__ == '__main__':
    main()

