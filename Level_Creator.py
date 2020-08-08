import random
import os
import spritesheet
import pygame
#import Main
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
        self.height = tile_height
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
    coin_list = []
    chest_list = []
    platforms = pyramid_pattern(worldx, worldy, jump_width, jump_height)

    return_platforms.append(create_ground(worldx, worldy))
    for plat in platforms:
        return_platforms.append(plat)
        if plat.coin > 0:
            coin_list.append([plat.x + (tile_width // 2) - 20, plat.y - 20])
        if plat.coin > 1:
            coin_list.append([plat.x + (tile_width * 1.5) - 20, plat.y - 20])
        if plat.chest == True:
            chest_list.append([plat.x + (tile_width // 2) - 20, plat.y - 40])

    return return_platforms, coin_list, chest_list





# creates the ground, starting with just "solid_ground" but different grounds will be added later
def create_ground(worldx, worldy):
    return solid_ground(worldx, worldy)

def pyramid_pattern(worldx, worldy, jump_width, jump_height):
    temp_list = [one_tile_chest(worldx // 2, 150, 'chest')]
    y_level = 150 + jump_height - 10
    x_left = worldx // 2
    x_i_left = (worldx // 2) - tile_width
    x_i_right = (worldx // 2) + tile_width
    x_right = worldx // 2 + tile_width
    level_count = 2
    tile_count = 0
    while y_level < worldy - tile_height:
        while tile_count <= level_count:
            left_plat_type = platform_types[random.randrange(0, len(platform_types)-1)]
            right_plat_type = platform_types[random.randrange(0, len(platform_types)-1)]
            x_left -= jump_width + tile_width * level_count
            x_i_left -= 12
            x_right += jump_width + tile_width * level_count
            x_i_right += 12
            if x_left > 0:
                temp_list.append(left_plat_type(x_left, y_level, str(tile_count)))
            if tile_count < 2:
                temp_list.append(left_plat_type(x_i_left, y_level-5, str(tile_count)))
                temp_list.append(right_plat_type(x_i_right, y_level -5, str(tile_count)))
            if x_right + tile_width < worldx:
                temp_list.append(right_plat_type(x_right, y_level, str(tile_count)))
            tile_count += level_count
        y_level += jump_height - 10
        tile_count = 0
        level_count += 1
        x_left = worldx // 2
        x_right = worldx //2 + tile_width





    return temp_list
"""
# create the chest(goal) in middle third and top third of screen, random location
# this is for the first 'pyramid_pattern', more patterns to come later
def pyramid_pattern(worldx, worldy, jump_width, jump_height):
    platform_list = []
    label_count = 0
    chest_plat_x = random.randrange(worldx // 3, (worldx // 3) * 2)
    chest_plat_y = random.randrange(100, worldy // 3)
    chest = one_tile_chest(chest_plat_x, chest_plat_y, 'chest')
    platform_list.append(chest)
    generated_platforms_l = recurse_pyramid_l(chest.x, chest.x + chest.width, chest.surface, jump_width, jump_height, worldy)
    generated_platforms_r = recurse_pyramid_r(chest.x + chest.width, chest.surface, jump_width, jump_height, worldy)

    for plat in generated_platforms_l:
        label_count += 1
        plat.label = label_count
        if plat.x > 0 and plat.x + plat.width < worldx:
            platform_list.append(plat)

    for plat in generated_platforms_r:
        label_count += 1
        plat.label = label_count
        #platform_list.append(plat)
        if plat.x > 0 and plat.x + plat.width < worldx:
            platform_list.append(plat)


    print(label_count)
    return platform_list


def recurse_pyramid_r(current_right_x, current_surface, jump_width, jump_height, worldy):
    right_pyramid_list = []
    right_list = []
    # create right platform
    right_plat_type = platform_types[random.randrange(0, len(platform_types) - 1)]
    temp = right_plat_type(0, 0, '0')
    temp_x = random.randrange(current_right_x, current_right_x + jump_width)
    temp_y = current_surface + jump_height - tile_height #random.randrange(current_surface, current_surface + jump_height)
    right_plat = right_plat_type(temp_x, temp_y, 'temp')
    if right_plat.surface < worldy - jump_height - tile_height:
        right_list = recurse_pyramid_r(right_plat.x + right_plat.width, right_plat.surface, jump_width, jump_height, worldy)

    right_pyramid_list.append(right_plat)

    if right_list != []:
        for plat in right_list:
            right_pyramid_list.append(plat)

    return right_pyramid_list



# populates the rest of the
def recurse_pyramid_l(current_left_x, current_right_x, current_surface, jump_width, jump_height, worldy):
    pyramid_list = []
    left_list = []
    right_list = []
    # choose left platform
    left_plat_type = platform_types[random.randrange(0, len(platform_types))]
    temp = left_plat_type(0, 0, '0')
    temp_x = random.randrange(current_left_x - temp.width - jump_width, current_left_x - temp.width)
    temp_y = current_surface + jump_height - tile_height #random.randrange(current_surface, current_surface + jump_height)
    left_plat = left_plat_type(temp_x, temp_y, 'temp')

    # create right platform
    right_plat_type = platform_types[random.randrange(0, len(platform_types))]
    right_plat = right_plat_type(0, 0, '0')
    right_plat.x = random.randrange(current_right_x, current_right_x + jump_width)
    right_plat.y = current_surface + jump_height - tile_height #random.randrange(current_surface, current_surface + jump_height)
    right_plat.surface = right_plat.y + 14

    if left_plat.surface < worldy - jump_height:
        left_list = recurse_pyramid_l(left_plat.x, left_plat.x + left_plat.width, left_plat.surface, jump_width, jump_height, worldy)

    if right_plat.surface < worldy - jump_height - 50:
        right_list = recurse_pyramid_r(right_plat.x + right_plat.width, right_plat.surface, jump_width, jump_height, worldy)

    pyramid_list.append(left_plat)
    #pyramid_list.append(right_plat)

    if left_list != []:
        for plat in left_list:
            pyramid_list.append(plat)

    if right_list != []:
        for plat in right_list:
            pyramid_list.append(plat)

    return pyramid_list
"""

#types of platforms
platform_types = [one_tile_coin, two_tile_coin]

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

    level_platforms, level_coins, level_chests = create_platforms(worldx, worldy, jump_width, jump_height)
    level_enemies = [[0, 0]]#, [worldx - 50, 0]]

    return [level_platforms, level_coins, level_chests, level_enemies, level_player]




