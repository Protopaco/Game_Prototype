import pygame
import sys
import os

"""
OBJECTS
"""


# classes and functions
class Player(object):
    def __init__(self, x, y):
        self.walkRight = [pygame.image.load(os.path.join('images/char', 'R%s.png') % frame) for frame in range(1, 10)]
        self.walkLeft = [pygame.image.load(os.path.join('images/char', 'L%s.png') % frame) for frame in range(1, 10)]
        self.standing = pygame.image.load(os.path.join('images/char', 'standing.png'))
        self.x = x
        self.y = y
        self.max_hp = 10
        self.hp = self.max_hp
        self.walk_count = 0
        self.direction = 0
        self.is_jump = False
        self.height = 64
        self.width = 32
        self.gravity = uni_gravity
        self.falling = False
        self.platform_surface = 0
        self.jump_vel = uni_jump_vel
        self.on_surface = False

    def draw(self, world):
        if self.walk_count > 26:
            self.walk_count = 0
        if self.direction == 0:
            world.blit(self.standing, (self.x, self.y))

    def move(self, dir = 0):

        # program gravity
        for obj in objects:
            self.on_surface >= self.y + self.height == obj.surface and self.x >= obj.x and self.x + self.width <= obj.x + obj.width
            if self.on_surface:
                self.falling = False
            else:
                self.falling = True
                self.platform_surface = obj.surface

        if self.falling is True and self.is_jump is False:
            self.gravity = (self.gravity * 1.098)
            if self.y + self.height + self.gravity > self.platform_surface:
                self.y = self.platform_surface - self.height
                self.gravity = uni_gravity
            else:
                self.y = int(self.y + self.gravity)
            self.falling = False

        if self.is_jump is True:
            if self.jump_vel > 0 and not self.on_surface:
                self.jump_vel -= uni_jump_deg
                self.y -= self.jump_vel
                print(self.jump_vel)
            elif self.on_surface:
                self.is_jump = False
                self.jump_vel = uni_jump_vel
            else:
                self.is_jump = False
                self.jump_vel = uni_jump_vel


    def jump(self):
        if player.is_jump == False:
            player.is_jump = True
            self.walk_count = 0







class Object(object):
    def __init__(self, x, y, width, height, filename, surface):
        self.x = x
        self.y = y
        self.img = pygame.image.load(filename)
        self.surface = surface
        self.width = width
        self.height = height

    def draw(self, world):
        world.blit(self.img, (self.x, self.y))


def draw_world(world):
    world.blit(backdrop, backdropbox)
    for obj in objects:
        obj.draw(world)
    player.draw(world)

"""
SETUP
"""
# run once code
# world creation
worldx = 960
worldy = 540
fps = 40
ani = 4
clock = pygame.time.Clock()
pygame.init()
world = pygame.display.set_mode([worldx, worldy])
backdrop = pygame.image.load(os.path.join('images', 'Background960x540.png')).convert()
backdropbox = world.get_rect()
ground = (os.path.join('images', 'ground960x64.png'))

# world variables
uni_gravity = 1
uni_jump_vel = 10
uni_jump_deg = .25

red = (227, 41, 44)
black = (0, 0, 0)
blue = (41, 156, 227)

# create world objects
objects = []
enemies = []

player = Player(0,0)
objects.append(Object(0, 476, 960, 64, ground, 490))


main = True

"""
Main Loop
"""
# game loop

while main is True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit();
            sys.exit()
            main = False

        if event.type == pygame.KEYDOWN:
            if event.key == ord('q'):
                sys.exit()
                main = False
            if event.key == ord(' '):
                player.jump()

    player.move()
    draw_world(world)
    pygame.display.flip()
    clock.tick(fps)
