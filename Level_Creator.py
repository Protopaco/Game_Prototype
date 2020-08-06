import random
import os
import spritesheet
import pygame
pygame.init()



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

class one_tile(Platform):
    def __init__(self, x, y, label):
        Platform.__init__(self, x, y, label)
        self.x = x
        self.y = y
        self.surface = y + 14
        self.img = pygame.image.load(os.path.join('images', '1TilePlatform64x64.png'))
        self.width = 64
        self.height = 64
        self.coin = 0
        self.chest = False
        self.label = label
        self.right_edge = self.x + self.width
        self.bottom_edge = self.y + self.height
        self.dimensions = [self.x, self.right_edge, self.surface, self.bottom_edge]

class one_tile_coin(one_tile):
    def __init__(self, x, y, label):
        one_tile.__init__(self, x, y, label)
        self.coin = 1

class one_tile_chest(one_tile):
    def __init__(self, x, y, label):
        one_tile.__init__(self, x, y, label)
        self.chest = True





