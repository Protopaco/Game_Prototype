import random
import os
import spritesheet
import pygame
pygame.init()

tile_height = 64
tile_width = 64

# creating 'Ground' classes
class Ground(object):
    def __init__(self, worldx, worldy):
        self.x = 0
        self.y = worldy - tile_height
        self.surface = self.y + 14
        self.img = None
        self.width = worldx
        self.height = tile_height
        self.label = 'ground'
        self.right_edge = self.x + self.width
        self.bottom_edge = self.y + self.height
        self.dimensions = [self.x, self.right_edge, self.surface, self.bottom_edge]

    def draw(self, world):
        world.blit(self.img, (self.x, self.y))

# 'solid_ground' is the basic, one piece ground tile for beginning levels
class solid_ground(Ground):
    def __init__(self, worldx, worldy):
        Ground.__init__(self, worldx, worldy)
        self.img = pygame.image.load(os.path.join('images', 'full_ground1920x64.png'))

# creating 'Platform' classes, each type of platform will be a different classe for ease of use
class Platform(object):
    def __init__(self, x, y, label):
        self.x = x
        self.y = y
        self.surface = y + 14
        self.img = None
        self.width = 0
        self.height = 0
        self.coin = 0
        self.chest = False
        self.label = label
        self.right_edge = self.x + self.width
        self.bottom_edge = self.y + self.height
        self.dimensions = [self.x, self.right_edge, self.surface, self.bottom_edge]


    def draw(self, world):
        world.blit(self.img, (self.x, self.y))

# one tile, small platform, no coins, no chest, base class for more tiles later
class one_tile(Platform):
    def __init__(self, x, y, label):
        Platform.__init__(self, x, y, label)
        self.x = x
        self.y = y
        self.surface = y + 14
        self.img = pygame.image.load(os.path.join('images', '1TilePlatform64x64.png'))
        self.width = tile_width
        self.height = tile_height
        self.coin = 0
        self.chest = False
        self.label = label
        self.right_edge = self.x + self.width
        self.bottom_edge = self.y + self.height
        self.dimensions = [self.x, self.right_edge, self.surface, self.bottom_edge]

# one tile platform, with one coin
class one_tile_coin(one_tile):
    def __init__(self, x, y, label):
        one_tile.__init__(self, x, y, label)
        self.coin = 1

# one tile platform, with chest on it
class one_tile_chest(one_tile):
    def __init__(self, x, y, label):
        one_tile.__init__(self, x, y, label)
        self.chest = True

# two tile platform, base class for other two tile platforms
class two_tile(Platform):
    def __init__(self, x, y, label):
        Platform.__init__(self, x, y, label)
        self.x = x
        self.y = y
        self.surface = y + 14
        self.img = pygame.image.load(os.path.join('images', '2TilePlatform128x64.png'))
        self.width = tile_width * 2
        self.height = tile_height * 2
        self.coin = 0
        self.chest = False
        self.label = label
        self.right_edge = self.x + self.width
        self.bottom_edge = self.y + self.height
        self.dimensions = [self.x, self.right_edge, self.surface, self.bottom_edge]

# two tile platform, with two coins on it
class two_tile_coin(two_tile):
    def __init__(self, x, y, label):
        two_tile.__init__(self, x, y, label)
        self.coin = 2

# base method for creating platforms in the world, just calls other methods to create different kinds of platforms
def create_platforms(worldx, worldy, jump_width, jump_height):
    return_platforms = []

    ground = create_ground(worldx, worldy)
    platforms = pyramid_pattern(worldx, worldy, jump_width, jump_height)

    return_platforms.append(ground)
    for plat in platforms:
        return_platforms.append(plat)

    return return_platforms





# creates the ground, starting with just "solid_ground" but different grounds will be added later
def create_ground(worldx, worldy):
    return solid_ground(worldx, worldy)

# create the chest(goal) in middle third and top third of screen, random location
# this is for the first 'pyramid_pattern', more patterns to come later
def pyramid_pattern(worldx, worldy, jump_width, jump_height):
    platform_list = []
    chest_plat_x = random.randrange(worldx // 3, (worldx // 3) * 2)
    chest_plat_y = random.randrange(0, worldy // 3)
    chest = one_tile_chest(chest_plat_x, chest_plat_y, 'chest')
    platform_list.append(chest)
    generated_platforms = recurse_pyramid(chest.x, chest.x + chest.width, chest.surface, jump_width, jump_height, 0)
    for plat in generated_platforms:
        platform_list.append(plat)
    return platform_list

# populates the rest of the
def recurse_pyramid(current_left_x, current_right_x, current_surface, jump_width, jump_height, plat_label):
    # choose left platform type:
    plat_label += 1
    left_plat_type = platform_types[random.randrange(0, len(platform_types) - 1)]
    new_left_plat_x = random.randrange(jump_width * -1, current_left_x)
    new_left_plat_y = random.randrange(current_surface, current_surface + jump_height)
    new_left_plat = left_plat_type(new_left_plat_x, new_left_plat_y, plat_label)

    return [new_left_plat]








#types of platforms
platform_types = [one_tile, one_tile_coin, two_tile, two_tile_coin]

# base class for level creation
# starts by creating the platforms
# then adds coins
# then adds chests
# then adds enemies
# finally adds player
# returns list of lists

def level_creator(worldx, worldy, jump_width, jump_height):
    level_platforms = []
    level_coins = []
    level_chests = []
    level_enemies = []
    level_player = []

    level_platforms = create_platforms(worldx, worldy, jump_width, jump_height)

    return level_platforms
    pass



