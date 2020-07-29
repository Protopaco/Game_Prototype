import pygame
import sys
import os
import spritesheet

"""
OBJECTS
"""


# classes and functions
class Player(object):
    def __init__(self, x, y):
        self.run_r = [pygame.image.load(os.path.join('images/char', 'R%s.png') % frame) for frame in range(1, 10)]
        self.run_l = [pygame.image.load(os.path.join('images/char', 'L%s.png') % frame) for frame in range(1, 10)]
        self.standing = pygame.image.load(os.path.join('images/char', 'standing.png'))
        self.x = x
        self.y = y
        self.max_hp = 10
        self.hp = self.max_hp
        self.walk_count = 0
        self.direction = 0
        self.is_jump = False
        self.height = 48
        self.width = 33
        self.gravity = uni_gravity
        self.jump_vel = uni_jump_vel
        self.is_falling = False
        self.vel = uni_run_vel

    def draw(self, world):
        self.move()
        if self.walk_count > 25:
            self.walk_count = 0
        if self.direction == 0:
            world.blit(self.standing, (int(self.x), int(self.y)))
        elif self.direction == 1:
            self.walk_count += 1
            world.blit(self.run_r[self.walk_count // 3], (self.x, self.y))
        elif self.direction == -1:
            self.walk_count += 1
            world.blit(self.run_l[self.walk_count // 3], (self.x, self.y))


    def move(self):
        # Walking Right
        if self.direction == 1:
            #print("move right")
            self.collision(self.vel, 0)

        # Walking Left
        elif self.direction == -1:
            #print("move left")
            self.collision(self.vel * -1, 0)

        # Jumping
        if self.is_jump is True:
            #print("jumping!")
            if self.collision(0, self.jump_vel * - 1):
                self.is_jump = False
            self.jump_vel -= uni_gravity

        # Gravity
        if not self.is_jump:
            self.not_falling = self.collision(0, self.gravity)
            if not self.not_falling:
                self.gravity += uni_grav_acel
                #print("falling")
            else:
                self.gravity = uni_gravity
                self.is_jump = False
                self.jump_vel = uni_jump_vel




    def collision(self, x, y):
        collision = False
        count = 0
        #print("collision: {x}, {y}".format(x=x, y=y))
        while collision is False and count < len(objects):
            if self.x + self.width + x > objects[count].dimensions[0] and self.x + x < objects[count].dimensions[1] and self.y + self.height + y > objects[count].dimensions[2] and self.y + y < objects[count].dimensions[3]:
                collision = True
            elif self.x + x < 0 or self.x + self.width + x > worldx:
                collision = True
            elif self.x + self.width + x > objects[count].dimensions[0] and self.x + x < objects[count].dimensions[1] and self.y + self.height > objects[count].dimensions[2] - y and self.y + y < objects[count].dimensions[3]:
                collision = True
                #print(objects[count].label)
                self.y = objects[count].dimensions[2] + self.height
                self.x += x
                #print(self.y)
            count += 1
        if collision == False:
            self.x += x
            self.y = int(y + self.y)
        #print(collision)
        return collision

    def jump(self):
        if self.is_jump == False:
            self.is_jump = True
            self.walk_count = 0

    def move_right(self):
        if self.direction != 1:
            self.direction = 1
            self.walk_count = 0
            #self.width = 26

    def move_left(self):
        if self.direction != -1:
            self.direction = -1
            self.walk_count = 0
            #self.width = 26

    def stand(self):
        #self.width = 33
        self.direction = 0


class enemy(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walk_count = 0
        self.direction = 0
        self.run_r = []
        self.run_l = []
        self.jump = []
        self.idle = []
        self.vel = 0
        self.hp = 0
        self.max_hp = 0
        self.height = 0
        self.width = 0
        self.gravity = uni_gravity
        self.jump_vel = 0
        self.is_falling = False


    def draw(self, world):
        self.move()
        if self.walk_count > fps - 5:
            self.walk_count = 0
        print("walk_count: {w}".format(w=self.walk_count))
        print("out of bounds: {b}".format(b= self.walk_count //(fps // len(self.run_l))))
        if self.direction == 0:
            if self.idle_count > len(self.idle):
                self.idle_count = 0
            world.blit(self.idle[self.idle_count], (self.x, self.y))
            self.idle_count += 1
        elif self.direction == 1:
            world.blit(self.run_r[int(self.walk_count // (fps // len(self.run_r)))], (self.x, self.y))
        elif self.direction == -1:
            world.blit(self.run_l[int(self.walk_count // (fps // len(self.run_l)))], (self.x, self.y))

        self.walk_count += 1


    def move(self):
        self.ai()
        # Walking Right
        if self.direction == 1:
            #print("move right")
            self.collision(self.vel, 0)

        # Walking Left
        elif self.direction == -1:
            #print("move left")
            self.collision(self.vel * -1, 0)

        # Jumping
        if self.is_jump is True:
            #print("jumping!")
            if self.collision(0, self.jump_vel * - 1):
                self.is_jump = False
            self.jump_vel -= uni_gravity

        # Gravity
        if not self.is_jump:
            self.not_falling = self.collision(0, self.gravity)
            if not self.not_falling:
                self.gravity += uni_grav_acel
                #print("falling")
            else:
                self.gravity = uni_gravity
                self.is_jump = False
                self.jump_vel = uni_jump_vel

    def collision(self, x, y):
        collision = False
        count = 0
        #print("collision: {x}, {y}".format(x=x, y=y))
        while collision is False and count < len(objects):
            if self.x + self.width + x > objects[count].dimensions[0] and self.x + x < objects[count].dimensions[1] and self.y + self.height + y > objects[count].dimensions[2] and self.y + y < objects[count].dimensions[3]:
                collision = True
            elif self.x + x < 0 or self.x + self.width + x > worldx:
                collision = True
            elif self.x + self.width + x > objects[count].dimensions[0] and self.x + x < objects[count].dimensions[1] and self.y + self.height > objects[count].dimensions[2] - y and self.y + y < objects[count].dimensions[3]:
                collision = True
                #print(objects[count].label)
                self.y = objects[count].dimensions[2] + self.height
                self.x += x
                #print(self.y)
            count += 1
        if collision == False:
            self.x += x
            self.y = int(y + self.y)
        #print(collision)
        return collision

    def jump(self):
        if self.is_jump == False:
            self.is_jump = True
            self.walk_count = 0

    def move_right(self):
        if self.direction != 1:
            self.direction = 1
            self.walk_count = 0
            #self.width = 26

    def move_left(self):
        if self.direction != -1:
            self.direction = -1
            self.walk_count = 0
            #self.width = 26

    def stand(self):
        #self.width = 33
        self.direction = 0

    def ai(self):
        if self.x + 10 < player.x:
            self.move_right()
        elif self.x - 10 > player.x:
            self.move_left()
        else:
            self.stand()





class red_guy(enemy):
    def __init__(self, x, y):
        self.bs = spritesheet.spritesheet(os.path.join('images/red_guy', 'blink.png'))
        self.rs = spritesheet.spritesheet(os.path.join('images/red_guy', 'run_r2.png'))
        self.js = spritesheet.spritesheet(os.path.join('images/red_guy', 'jump.png'))
        self.still = self.rs.image_at((0, 0, 100, 100), (0, 0, 0))
        self.still = pygame.transform.scale(self.still, (48, 48))
        self.run_r = self.rs.load_strip((0, 0, 100, 100),  18, (0, 0, 0))
        self.idle = self.bs.load_strip((0, 0, 100, 100),  11, (0, 0, 0))
        self.jump = self.js.load_strip((0, 0, 100, 100), 2, (0, 0, 0))
        self.run_l = []
        self.walk_count = 0
        self.vel = 3
        self.x = x
        self.y = y
        self.direction = 0
        self.width = 48
        self.height = 48
        self.is_jump = False
        self.gravity = uni_gravity
        self.run_r_count = 0
        self.run_l_count = 0
        self.idle_count = 0


        for i in range(0, len(self.jump)):
            self.jump[i] = pygame.transform.scale(self.jump[i], (48,48))
        for i in range(0, len(self.idle)):
            self.idle[i] = pygame.transform.scale(self.idle[i], (48,48))
        for i in range(0, len(self.run_r)):
            self.run_r[i] = pygame.transform.scale(self.run_r[i], (48,48))
        for i in range(0, len(self.run_r)):
            self.run_l.append(pygame.transform.flip(self.run_r[i], True, False))



class Object(object):
    def __init__(self, x, y, width, height, filename, label):
        self.x = x
        self.y = y
        self.img = pygame.image.load(filename)
        self.width = width
        self.height = height
        self.surface = y + 14
        self.label = label
        self.right_edge = self.x + self.width
        self.bottom_edge = self.y + self.height
        self.dimensions = [self.x, self.right_edge, self.surface, self.bottom_edge]

    def draw(self, world):
        world.blit(self.img, (self.x, self.y))
        #pygame.draw.rect(world, red, (self.x, self.surface, self.width, self.height), 1 )


def draw_world(world):
    world.blit(backdrop, backdropbox)
    for obj in objects:
        obj.draw(world)
    player.draw(world)
    rg1.draw(world)


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
uni_jump_vel = 16
uni_grav_acel = 1.1
uni_run_vel = 5

red = (227, 41, 44)
black = (0, 0, 0)
blue = (41, 156, 227)

# create world objects
objects = []
enemies = []

player = Player(0, 0)
rg1 = red_guy(300, 400)

objects.append(Object(0, 476, 960, 64, ground, "ground"))
objects.append(Object(0, 348, 128, 64, mdm_platform, "platform one"))
objects.append(Object(184, 284, 64, 64, sml_platform, "platform two"))
objects.append(Object(312, 156, 64, 64, sml_platform, "platform two"))
objects.append(Object(440, 28, 64, 64, sml_platform, "platform two"))


main = True

"""
Main Loop
"""
# game loop

while main is True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            main = False
            sys.exit()

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == ord('q'):
                main = False
                sys.exit()
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
