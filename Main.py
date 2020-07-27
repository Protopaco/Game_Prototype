import pygame
import sys
import os

"""
OBJECTS
"""


# classes and functions
class Player(object):
    def __init__(self, x, y):
        self.walk_right = [pygame.image.load(os.path.join('images/char', 'R%s.png') % frame) for frame in range(1, 10)]
        self.walk_left = [pygame.image.load(os.path.join('images/char', 'L%s.png') % frame) for frame in range(1, 10)]
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
        self.platform_surface = None
        self.jump_vel = uni_jump_vel
        self.on_surface = False
        self.vel = uni_run_vel

    def draw(self, world):
        player.move()
        if self.walk_count > 25:
            self.walk_count = 0
        if self.direction == 0:
            world.blit(self.standing, (int(self.x), int(self.y)))
        elif self.direction == 1:
            self.walk_count += 1
            world.blit(self.walk_right[self.walk_count // 3], (self.x, self.y))
        elif self.direction == -1:
            self.walk_count += 1
            world.blit(self.walk_left[self.walk_count // 3], (self.x, self.y))


    def move(self):

        # Gravity
        for obj in objects:
            if self.x >= obj.x - 40 and self.x + self.width <= obj.x + obj.width:
                self.on_surface = self.y + self.height == obj.surface
                if not self.on_surface:
                    self.falling = True
                    self.platform_surface = [obj.surface, obj.surface + 10]
                    print(obj.label)
                else:
                    self.falling = False
                print(self.falling)

        # Falling
        if self.falling is True:
            self.gravity = (self.gravity * 1.098)
            if self.y + self.height + self.gravity > self.platform_surface[0] and self.y < self.platform_surface[1]:
                self.y = self.platform_surface[0] - self.height
                self.gravity = uni_gravity
            else:
                self.y = int(self.y + self.gravity)

        # Jumping
        if self.is_jump is True:
            if self.gravity <= self.jump_vel:
                self.y -= self.jump_vel

            else:
                self.is_jump = False
                self.jump_vel = uni_jump_vel

        # Walking Right
        if player.direction == 1:
            if self.x + self.width + self.vel < worldx:
                self.x += self.vel

        # Walking Left
        elif player.direction == -1:
            if self.x - self.width > 0:
                self.x -= self.vel

    def jump(self):
        if player.is_jump == False:
            player.is_jump = True
            self.walk_count = 0

    def move_right(self):
        if player.direction != 1:
            player.direction = 1
            player.walk_count = 0

    def move_left(self):
        if player.direction != -1:
            player.direction = -1
            player.walk_count = 0

    def stand(self):
        player.direction = 0







class Object(object):
    def __init__(self, x, y, width, height, filename, label):
        self.x = x
        self.y = y
        self.img = pygame.image.load(filename)
        self.width = width
        self.height = height
        self.surface = y + 14
        self.label = label

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
sml_platform = (os.path.join('images', '1TilePlatform64x64.png'))
mdm_platform = (os.path.join('images', '2TilePlatform128x64.png'))

# key presses



# world variables
uni_gravity = 1
uni_jump_vel = 10
uni_jump_deg = .25
uni_run_vel = 5

red = (227, 41, 44)
black = (0, 0, 0)
blue = (41, 156, 227)

# create world objects
objects = []
enemies = []

player = Player(0, 410)
objects.append(Object(0, 476, 960, 64, ground, "ground"))
objects.append(Object(832, 316, 128, 64, mdm_platform, "platform one"))


main = True

"""
Main Loop
"""
# game loop

while main is True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            main = False
        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == ord('q'):
                sys.exit()
                main = False
            if event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_RIGHT:
                player.move_right()
            if event.key == pygame.K_LEFT:
                player.move_left()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                if player.direction == 1:
                    player.stand()
            elif event.key == pygame.K_LEFT:
                if player.direction == -1:
                    player.stand()



    draw_world(world)
    pygame.display.flip()
    clock.tick(fps)
