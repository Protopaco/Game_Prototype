import pygame
import sys
import os
import spritesheet
import p_forms
import math



"""
platforms.platformS
"""

class HUD(object):
    def __init__(self):
        self.font = pygame.font.Font('ARCADECLASSIC.TTF', 42)
        self.coin_still = pygame.image.load(os.path.join('images/object', 'coin_still100.png'))
        self.coin_still = pygame.transform.scale(self.coin_still, (40, 40))
        self.coin_still_width = self.coin_still.get_width()
        self.cs = spritesheet.spritesheet(os.path.join('images/object', 'coin100.png'))
        self.coin_ani_count = 0
        self.coin_rotation_rate = .2
        self.coin_ani = self.cs.load_strip((0, 0, 100, 100), 16, (0, 0, 0))
        for i in range(0, len(self.coin_ani)):
            self.coin_ani[i] = pygame.transform.scale(self.coin_ani[i], (40,40))

    def draw(self, world):
        coin_score = self.font.render(str(player.coin_count), 2, black)
        score_width = coin_score.get_width()
        world.blit(coin_score, (worldx - 5 - score_width, 5))
        """
        world.blit(self.coin_still, (worldx - 5 - score_width - 5 - self.coin_still_width, 5))
        """
        world.blit(self.coin_ani[round(self.coin_ani_count)], (worldx - 5 - score_width - 5 - self.coin_still_width, 5))
        self.coin_ani_count += self.coin_rotation_rate
        if self.coin_ani_count >= len(self.coin_ani) -1:
            self.coin_ani_count = 0

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
        self.gravity = uni_grav_acel
        self.max_jump_vel = 20
        self.jump_vel = self.max_jump_vel
        self.is_falling = False
        self.vel = uni_run_vel
        self.coin_count = 0
        self.jump_height = self.find_max_height()
        self.ledges = []
        self.chosen_ledge = [worldx, worldy, 'x']
        self.current_platform = [(0,0), (0,0)]
        self.find_ledges()
        self.choose_ledge()


    def find_ledges(self):
        for i in level_platforms:
            self.ledges.append([i.x, i.surface, 'l'])
            self.ledges.append([i.x+i.width, i.surface, 'r'])


    def choose_ledge(self):
        if abs(self.chosen_ledge[1] - (self.y + self.height)) < self.jump_height + self.height:
            self.chosen_ledge = [worldx, worldy, 'x']
        for i in self.ledges:
            height_diff = i[1] - (self.y + self.height)
            if height_diff < 0 and abs(height_diff) < self.jump_height - self.height:
                if abs(self.x - self.chosen_ledge[0]) > abs(self.x - i[0]):
                    self.chosen_ledge = [i[0], i[1], i[2]]

        print(self.chosen_ledge)


    def find_max_height(self):
        max_height = 0
        while self.jump_vel > 0:
            max_height += self.jump_vel
            self.jump_vel -= uni_grav_acel
        self.jump_vel = self.max_jump_vel
        return round(max_height)



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
        self.choose_ledge()
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
            if self.collision(0, self.jump_vel * - 1):
                self.is_jump = False
            self.jump_vel -= uni_grav_acel

        # Gravity
        if not self.is_jump:
            self.not_falling = self.collision(0, self.gravity)
            if not self.not_falling:
                self.gravity += uni_grav_acel
            else:
                self.gravity = uni_grav_acel
                self.is_jump = False
                self.jump_vel = self.max_jump_vel

        # Coin Collision
        for coin in coins:
            if self.x + self.width > coin.x and self.x < coin.x + coin.width and self.y + self.width > coin.y and self.y < coin.y + coin.width:
                self.coin_count += 1
                coins.pop(coins.index(coin))



    def collision(self, x, y):
        collision = False
        count = 0
        #print("collision: {x}, {y}".format(x=x, y=y))
        while collision is False and count < len(platforms):
            if self.x + self.width + x > platforms[count].dimensions[0] and self.x + x < platforms[count].dimensions[1] and self.y + self.height + y > platforms[count].dimensions[2] and self.y + y < platforms[count].dimensions[3]:
                collision = True
            elif self.x + x < 0 or self.x + self.width + x > worldx:
                collision = True
            elif self.x + self.width + x > platforms[count].dimensions[0] and self.x + x < platforms[count].dimensions[1] and self.y + self.height > platforms[count].dimensions[2] - y and self.y + y < platforms[count].dimensions[3]:
                collision = True
                self.y = platforms[count].dimensions[2] + self.height
                self.x += x
                self.current_platform[0] = (platforms[count].dimensions[0], platforms[count].dimensions[2])
                self.current_platform[1] = (platforms[count].dimensions[1], platforms[count].dimensions[2])
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


    def hit(self, projectile):
        self.hp -= projectile.damage
        projectiles.remove(projectile)
        print("hp: {h}".format(h=self.hp))


class enemy(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walk_count = 0
        self.direction = 0
        self.run_r = []
        self.run_l = []
        self.jump_img = []
        self.idle = []
        self.vel = 0
        self.hp = 0
        self.max_hp = 0
        self.height = 0
        self.width = 0
        self.gravity = uni_grav_acel
        self.jump_vel = 0
        self.is_falling = True
        self.run_count = 0
        self.max_jump_vel = 0
        self.current_platform = [(0,0), (0,0)]


    def draw(self, world):
        self.move()
        if self.is_jump and self.jump_vel > 1:
            world.blit(self.jump_img[0], (self.x, self.y))
        elif self.is_jump and self.jump_vel < 1:
            world.blit(self.jump_img[1], (self.x, self.y))
        elif self.direction == 0:
            if self.idle_count > len(self.idle)-1:
                self.idle_count = 0
            world.blit(self.idle[round(self.idle_count)], (self.x, self.y))
            self.idle_count += .2
        elif self.direction > 0:
            world.blit(self.run_r[self.run_count], (self.x, self.y))
            self.run_count += 1
        elif self.direction < 0:
            world.blit(self.run_l[self.run_count], (self.x, self.y))
            self.run_count += 1
        if self.run_count > len(self.run_r)-1:
            self.run_count = 0

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
                #self.jump_vel = self.max_jump_vel
            self.jump_vel -= uni_grav_acel

        # Gravity
        if not self.is_jump:
            if self.collision(0, self.gravity) == False:
                self.is_falling = True
                if self.is_falling:
                    self.gravity += uni_grav_acel
            else:
                self.gravity = uni_grav_acel
                self.is_jump = False
                self.is_falling = False
                self.jump_vel = uni_jump_vel



    def collision(self, x, y):
        collision = False
        count = 0
        while collision is False and count < len(platforms):
            if self.x + self.width + x > platforms[count].dimensions[0] and self.x + x < platforms[count].dimensions[1] and self.y + self.height + y > platforms[count].dimensions[2] and self.y + y < platforms[count].dimensions[3]:
                collision = True
                self.current_platform[0] = (platforms[count].dimensions[0], platforms[count].dimensions[2])
                self.current_platform[1] = (platforms[count].dimensions[1], platforms[count].dimensions[2])
            elif self.x + x < 0 or self.x + self.width + x > worldx:
                collision = True
            elif self.x + self.width + x > platforms[count].dimensions[0] and self.x + x < platforms[count].dimensions[1] and self.y + self.height > platforms[count].dimensions[2] - y and self.y + y < platforms[count].dimensions[3]:
                collision = True
                #print(platforms.platforms[count].label)
                self.y = platforms[count].dimensions[2] + self.height
                self.x += x
                self.current_platform[0] = (platforms[count].dimensions[0], platforms[count].dimensions[2])
                self.current_platform[1] = (platforms[count].dimensions[1], platforms[count].dimensions[2])
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
        """
        if self.x + 10 < player.x:
            self.move_right()
        elif self.x - 10 > player.x:
            self.move_left()
        else:
            self.stand()
        if self.y > player.y and pygame.time.get_ticks() % 100 == 0:
            self.jump()
        """


class red_guy(enemy):
    def __init__(self, x, y):
        enemy.__init__(self, x, y)
        self.bs = spritesheet.spritesheet(os.path.join('images/red_guy', 'blink.png'))
        self.rs = spritesheet.spritesheet(os.path.join('images/red_guy', 'run_r.png'))
        self.js = spritesheet.spritesheet(os.path.join('images/red_guy', 'jump.png'))
        self.still = self.bs.image_at((0, 0, 100, 100), (0, 0, 0))
        self.still = pygame.transform.scale(self.still, (48, 48))
        self.run_r = self.rs.load_strip((0, 0, 100, 100),  18, (0, 0, 0))
        self.idle = self.bs.load_strip((0, 0, 100, 100),  11, (0, 0, 0))
        self.jump_img = self.js.load_strip((0, 0, 100, 100), 2, (0, 0, 0))
        self.run_l = []
        self.walk_count = 0
        self.vel = 3
        self.x = x
        self.y = y
        self.direction = 0
        self.width = 48
        self.height = 48
        self.is_jump = False
        self.gravity = uni_grav_acel
        self.run_count = 0
        self.idle_count = 0
        self.max_jump_vel = 20
        self.jump_vel = self.max_jump_vel
        self.throw_count = 0
        self.ledges = []
        self.chosen_ledge = [worldx, worldy, 'x']
        self.current_platform = [(0,0), (0,0)]
        self.jump_point = 0
        self.find_ledges()
        self.jump_height, self.jump_width = self.find_max_height()



        for i in range(0, len(self.jump_img)):
            self.jump_img[i] = pygame.transform.scale(self.jump_img[i], (48,48))
        for i in range(0, len(self.idle)):
            self.idle[i] = pygame.transform.scale(self.idle[i], (48,48))
        for i in range(0, len(self.run_r)):
            self.run_r[i] = pygame.transform.scale(self.run_r[i], (48,48))

        for i in range(0, len(self.run_r)):
            self.run_l.append(pygame.transform.flip(self.run_r[i], True, False))


    def find_max_height(self):
        max_height = 0
        max_width = 0
        while self.jump_vel > 0:
            self.jump_vel -= uni_grav_acel
            max_height += self.jump_vel
            max_width += self.vel

        self.jump_vel = self.max_jump_vel
        print("max_height: {m}".format(m = max_height))
        test_max = ((self.max_jump_vel ** 2) * (math.sin(90) ** 2)) / (2 * uni_grav_acel)
        print("test_max: {t}".format(t = test_max))
        return round(max_height), round(max_width)


    def ai(self):
        """
        if self.x + 10 < player.x:
            self.move_right()
        elif self.x - 10 > player.x:
            self.move_left()
        else:
            self.stand()
        if self.y > player.y and pygame.time.get_ticks() % 100 == 0:
            self.jump()
        """
        self.throw_count += 1
        if self.throw_count >= 100 and len(projectiles) < 5:
            self.throw_acorn()
            self.throw_count = 0
        if self.is_jump == False and self.is_falling == False:
            self.choose_ledge()
            if self.x + self.width < self.chosen_ledge[0]:
                self.move_right()
                if self.x + self.width >= self.jump_point:
                    self.jump()
            else:
                self.move_left()


    def find_jump_point(self):
        height_diff = self.chosen_ledge[1] - (self.y + self.height)
        jump_width = 0
        while height_diff < 0:
            height_diff += self.jump_vel - uni_grav_acel
            jump_width += self.vel
            print("jump_width: {j}".format(j=jump_width))
        self.jump_point = self.chosen_ledge[0] - jump_width



    def find_ledges(self):
        for i in level_platforms:
            self.ledges.append([i.x, i.surface, 'l'])
            self.ledges.append([i.x+i.width, i.surface, 'r'])


    def choose_ledge(self):
        if abs(self.chosen_ledge[1] - (self.y + self.height)) < self.jump_height + self.height:
            self.chosen_ledge = [worldx, worldy, 'x']
        for i in self.ledges:
            height_diff = i[1] - (self.y + self.height)
            if height_diff < 0 and abs(height_diff) < self.jump_height - self.height:
                if abs(self.x - self.chosen_ledge[0]) > abs(self.x - i[0]):
                    self.chosen_ledge = [i[0], i[1], i[2]]
        self.find_jump_point()
        print(self.jump_point)

        print(self.chosen_ledge)









    def throw_acorn(self):
        tx = player.x - self.x
        ty = player.y - self.y
        z = 100 / (abs(tx) + abs(ty))
        dx = tx * z
        dy = ty * z
        #print('player({x}, {y})'.format(x=player.x, y=player.y))
        #print('self({x}, {y})'.format(x=self.x, y=self.y))
        #print("dx: {x}, dy: {y}".format(x=dx, y=dy))
        #print("throw!")
        projectiles.append(acorn(self.x, self.y, dx, dy))


class blue_guy(enemy):
    def __init__(self, x, y):
        enemy.__init__(self, x, y)
        self.bs = spritesheet.spritesheet(os.path.join('images/blue_guy', 'blink.png'))
        self.rs = spritesheet.spritesheet(os.path.join('images/blue_guy', 'run_r3.png'))
        self.js = spritesheet.spritesheet(os.path.join('images/blue_guy', 'jump.png'))
        self.still = self.bs.image_at((0, 0, 100, 100), (0, 0, 0))
        self.still = pygame.transform.scale(self.still, (48, 48))
        self.run_r = self.rs.load_strip((0, 0, 100, 100),  18, (0, 0, 0))
        self.idle = self.bs.load_strip((0, 0, 100, 100),  11, (0, 0, 0))
        self.jump_img = self.js.load_strip((0, 0, 100, 100), 2, (0, 0, 0))
        self.run_l = []
        self.walk_count = 0
        self.vel = 3
        self.x = x
        self.y = y
        self.direction = 0
        self.width = 48
        self.height = 48
        self.is_jump = False
        self.gravity = uni_grav_acel
        self.run_count = 0
        self.idle_count = 0
        self.max_jump_vel = 20
        self.jump_vel = self.max_jump_vel



        for i in range(0, len(self.jump_img)):
            self.jump_img[i] = pygame.transform.scale(self.jump_img[i], (48,48))
        for i in range(0, len(self.idle)):
            self.idle[i] = pygame.transform.scale(self.idle[i], (48,48))
        for i in range(0, len(self.run_r)):
            self.run_r[i] = pygame.transform.scale(self.run_r[i], (48,48))

        for i in range(0, len(self.run_r)):
            self.run_l.append(pygame.transform.flip(self.run_r[i], True, False))

    def ai(self):
        if self.x > player.x + 100 and self.x < player.x + 200:
            self.move_left()
        elif self.x < player.x - 100 and self.x > player.x - 200:
            self.move_right()
        else:
            self.stand()
        if self.y <= player.y and pygame.time.get_ticks() % 100 == 0:
            self.jump()

class Coin(object):
    def __init__(self, x, y):
        object.__init__(self)
        self.x = x
        self.y = y
        self.cs = spritesheet.spritesheet(os.path.join('images/object', 'coin100.png'))
        self.coin_ani = self.cs.load_strip((0, 0, 100, 100), 16, (0, 0, 0))
        self.coin_ani_count = 0
        self.coin_rotation_rate = .3
        self.width = 40
        self.height = 40
        self.settled = False
        self.coin_coordinates = [self.x, self.y, self.x + self.width, self.y + self.height]

        for i in range(0, len(self.coin_ani)):
            self.coin_ani[i] = pygame.transform.scale(self.coin_ani[i], (40,40))

    def draw(self, world):
        if self.settled is False:
            self.gravity()
        world.blit(self.coin_ani[round(self.coin_ani_count)], (self.x, self.y))
        self.coin_ani_count += self.coin_rotation_rate
        if self.coin_ani_count >= len(self.coin_ani) -1:
            self.coin_ani_count = 0

    def collision(self, y):
        collision = False
        count = 0
        while collision is False and count < len(platforms):
            if self.x + self.width > platforms[count].dimensions[0] and self.x < platforms[count].dimensions[1] and self.y + self.height + y > platforms[count].dimensions[2] and self.y + y < platforms[count].dimensions[3]:
                collision = True
            count += 1
        if collision == False:
            self.y = int(y + self.y)
        return collision

    def gravity(self):
        if self.collision(uni_grav_acel) is True:
            self.settled = True

class projectile(object):
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.img = 0
        self.img_count = 0
        self.vel = 1
        self.width = 0
        self.height = 0
        self.damage = 0

    def draw(self, world):
        self.move()
        self.hit()
        world.blit(self.img, (round(self.x), round(self.y)))


    def move(self):
        z = self.vel / (abs(self.dx) + abs(self.dy))
        self.x += self.dx * z
        self.y += self.dy * z

    def hit(self):
        if self.x + self.width > player.x and self.x < player.x + player.width  and self.y + self.height > player.y and self.y < player.y + player.height:
            player.hit(self)
            print("hit!")


class acorn(projectile):
    def __init__(self, x, y, dx, dy):
        projectile.__init__(self, x, y, dx, dy)
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.ass = spritesheet.spritesheet(os.path.join('images/object', 'sm_acorn.png'))
        self.img = self.ass.image_at((0, 0, 24, 19), (0, 0, 0))
        self.vel = 10
        self.img_count = 0
        self.damage = 1
        self.width = self.img.get_width()
        self.height = self.img.get_height()



def draw_world(world):
    world.blit(backdrop, backdropbox)
    hud.draw(world)
    for plat in platforms:
        plat.draw(world)
    player.draw(world)
    for enemy in enemies:
        enemy.draw(world)
    for coin in coins:
        coin.draw(world)
    for proj in projectiles:
        proj.draw(world)
        if proj.x > worldx or proj.y > worldy or proj.x < 0 or proj.y < 0:
            projectiles.remove(proj)

    pygame.draw.circle(world, black, (player.chosen_ledge[0], player.chosen_ledge[1]), 4)
    pygame.draw.circle(world, red, (enemies[0].chosen_ledge[0], enemies[0].chosen_ledge[1]), 4)
    pygame.draw.circle(world, blue, enemies[0].current_platform[0], 4)
    pygame.draw.circle(world, blue, enemies[0].current_platform[1], 4)

    pygame.draw.circle(world, blue, player.current_platform[0], 4)
    pygame.draw.circle(world, blue, player.current_platform[1], 4)


    if grid_on == True:
            draw_grid(world)


def load_level(level):
    for platform in level[0]:
        platforms.append(platform)
    for coin in level[1]:
        coins.append(coin)
    for chest in level[2]:
        chest.append(chest)
    for enemy in level[3]:
        enemies.append(enemy)
    player.x = level[4][0]
    player.y = level[4][1]

def draw_grid(world):
    gridfont = pygame.font.SysFont('0', 20)
    for x in range(64, worldx, 32):
        xlabel = gridfont.render(str(x), 2, black)
        world.blit(xlabel, (x, 32))
        world.blit(xlabel, (x, 320))
        world.blit(xlabel, (x, 704))
        world.blit(xlabel, (x, 1068))

        pygame.draw.line(world, black, (x, 0), (x, worldy))
    for y in range(64, worldy, 32):
        ylabel = gridfont.render(str(y), 2, black)
        world.blit(ylabel, (16, y))
        world.blit(ylabel, (480, y))
        world.blit(ylabel, (960, y))
        world.blit(ylabel, (1960, y))

        pygame.draw.line(world, black, (0, y), (worldx, y))


def display_grid(grid_on):
    if grid_on == False:
        grid_on = True
    else:
        grid_on = False
    return grid_on

"""
SETUP
"""
# run once code
# world creation
worldx = 1920
worldy = 1080
fps = 40
ani = 4
clock = pygame.time.Clock()
pygame.init()
world = pygame.display.set_mode([worldx, worldy], pygame.FULLSCREEN)
hud = HUD()
backdrop = pygame.image.load(os.path.join('images', 'Background1920x1080.png')).convert()
backdropbox = world.get_rect()
ground = (os.path.join('images', 'full_ground1920x64.png'))
sml_platform = (os.path.join('images', '1TilePlatform64x64.png'))
mdm_platform = (os.path.join('images', '2TilePlatform128x64.png'))
grid_on = False


# key presses

# world variables
uni_jump_vel = 16
uni_grav_acel = 1.1
uni_run_vel = 5

red = (227, 41, 44)
black = (0, 0, 0)
blue = (41, 156, 227)


"""
LEVEL CREATION
"""
level_platforms = []
level_coins = []
level_chest = []
level_enemies = []
level_player = []


level_platforms.append(p_forms.platform(0, worldy-64, 1920, 64, ground, "ground"))
level_platforms.append(p_forms.platform(0, 348, 128, 64, mdm_platform, "platform one"))
level_platforms.append(p_forms.platform(160, 288, 64, 64, sml_platform, "platform two"))
level_platforms.append(p_forms.platform(320, 160, 64, 64, sml_platform, "platform three"))
level_platforms.append(p_forms.platform(446, 96, 64, 64, sml_platform, "platform four"))
level_platforms.append(p_forms.platform(1664, 832, 128, 64, mdm_platform, "platform five"))
level_platforms.append(p_forms.platform(1408, 704, 128, 64, mdm_platform, 'platform six'))
level_platforms.append(p_forms.platform(1152, 512, 128, 64, mdm_platform, 'platform seven'))
level_platforms.append(p_forms.platform(896, 384, 128, 64, mdm_platform, 'platform eight'))
level_platforms.append(p_forms.platform(worldx-64, 960, 64, 64, sml_platform, 'platform nine'))
level_platforms.append(p_forms.platform(1280, 640, 64, 64, sml_platform, 'platform ten'))
level_platforms.append(p_forms.platform(1088, 512, 64, 64, sml_platform, 'platform ten'))
level_platforms.append(p_forms.platform(1536, 768, 64, 64, sml_platform, 'platform ten'))
level_platforms.append(p_forms.platform(640, 640, 128, 64, mdm_platform, 'platform eight'))
level_platforms.append(p_forms.platform(448, 448, 64, 64, sml_platform, "platform two"))
level_platforms.append(p_forms.platform(576, 576, 64, 64, sml_platform, "platform two"))
level_platforms.append(p_forms.platform(320, 320, 64, 64, sml_platform, "platform two"))


for i in level_platforms:
    cx = i.x + 12
    cy = i.y - 22
    if i.width == 64 or i.width == 128:
        level_coins.append(Coin(cx, cy))
    if i.width == 128:
        level_coins.append(Coin(cx+64, cy))
"""
level_coins.append(Coin(32, 320))
level_coins.append(Coin(96, 320))
level_coins.append(Coin(192, 256))
level_coins.append(Coin(352, 288))
level_coins.append(Coin(480, 416))
level_coins.append(Coin(576, 544))
level_coins.append(Coin(640, 608))
level_coins.append(Coin(704, 608))
level_coins.append(Coin(445, 0))
level_coins.append(Coin(200, 240))
level_coins.append(Coin(325, 110))
level_coins.append(Coin(445, 0))
level_coins.append(Coin(200, 240))
level_coins.append(Coin(325, 110))
level_coins.append(Coin(445, 0))
level_coins.append(Coin(200, 240))
level_coins.append(Coin(325, 110))
level_coins.append(Coin(445, 0))
"""

coin_x = 100
for i in range(0, 15):
    level_coins.append(Coin(coin_x, worldy-100))
    coin_x += 40

level_enemies.append(red_guy(800, 900))
level_enemies.append(blue_guy(200, 400))

level_player = [worldx - 100, worldy-200]

demo_level = [level_platforms, level_coins, level_chest, level_enemies, level_player]












# create world platforms.platforms
platforms = []
coins = []
chest = []
enemies = []
projectiles = []
player = Player(0,0)




load_level(demo_level)
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
            if event.key == pygame.K_g:
                grid_on = display_grid(grid_on)
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
