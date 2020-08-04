import pygame
import sys
import os
import spritesheet



"""
platforms.platformS
"""


class Menu(object):
    def __init__(self):
        object.__init__(self)
        self.x = worldx
        self.y = 5
        self.font_size = 42
        self.max_font_size = 104
        self.font = pygame.font.Font('ARCADECLASSIC.TTF', self.font_size)
        self.cs = spritesheet.spritesheet(os.path.join('images/object', 'coin100.png'))
        self.coin_ani_count = 0
        self.coin_rotation_rate = .2
        self.coin_ani = self.cs.load_strip((0, 0, 100, 100), 16, (0, 0, 0))
        self.score_spacer = 5
        self.score_width = 0
        self.transition_speed = 10
        self.transition_count = 0
        self.score_width = 0
        self.transition_diff = round((self.x + (self.score_width / 2) / (worldx / 2)))
        self.game_win = False
        for i in range(0, len(self.coin_ani)):
            size = self.font_size
            self.coin_ani[i] = pygame.transform.scale(self.coin_ani[i], (size, size))


    def game_over(self, world):
        #print("font_size: {f}".format(f=self.font_size))
        self.font = pygame.font.Font('ARCADECLASSIC.TTF', self.font_size)
        coin_score = self.font.render(str(player.coin_count), 2, white)
        self.score_width = coin_score.get_width()
        if self.game_win == True:
            if self.x + self.score_width >= worldx // 2:
                for i in range(0, len(self.coin_ani)):
                    print("font_size: {f}".format(f=self.font_size))
                    self.coin_ani[i] = pygame.transform.scale(self.coin_ani[i], (self.font_size, self.font_size))
                    print("font_size: {f}".format(f=self.font_size))
                #print(self.x + self.score_width)
                world.blit(coin_score, (self.x - self.score_spacer - self.score_width, round(self.y)))
                world.blit(self.coin_ani[round(self.coin_ani_count)], (self.x - self.score_spacer - self.score_width - self.score_spacer - self.font_size, round(self.y)))
                self.coin_ani_count += self.coin_rotation_rate
                if self.coin_ani_count >= len(self.coin_ani) - 1:
                    self.coin_ani_count = 0
                self.x -= self.transition_speed
                if self.y < worldy // 2:
                    self.y += abs(((self.y - (worldy / 2)) // self.transition_diff)) * 3
                if self.font_size < self.max_font_size:
                    self.font_size += 1


                self.score_spacer += round((self.max_font_size - self.font_size) // self.transition_diff)
            else:
                world.blit(coin_score, (self.x - self.score_spacer - self.score_width, self.y))
                world.blit(self.coin_ani[round(self.coin_ani_count)], (self.x - self.score_spacer - self.score_width - self.score_spacer - self.font_size, self.y))
                self.coin_ani_count += self.coin_rotation_rate
                if self.coin_ani_count >= len(self.coin_ani) -1:
                    self.coin_ani_count = 0

class HUD(object):
    def __init__(self):
        self.font = pygame.font.Font('ARCADECLASSIC.TTF', 42)
        self.hs = spritesheet.spritesheet(os.path.join('images/object', 'health_bar.png'))
        self.health_bar = self.hs.load_strip((0, 0, 100, 100), 2, (0, 0, 0))
        self.cs = spritesheet.spritesheet(os.path.join('images/object', 'coin100.png'))
        self.coin_ani_count = 0
        self.coin_rotation_rate = .2
        self.coin_ani = self.cs.load_strip((0, 0, 100, 100), 16, (0, 0, 0))
        self.coin_width = 40
        self.spacer = 5
        for i in range(0, len(self.coin_ani)):
            self.coin_ani[i] = pygame.transform.scale(self.coin_ani[i], (40,40))

    def draw(self, world):
        coin_score = self.font.render(str(player.coin_count), 2, white)
        score_width = coin_score.get_width()
        world.blit(coin_score, (worldx - self.spacer - score_width, self.spacer))
        world.blit(self.coin_ani[round(self.coin_ani_count)], (worldx - self.spacer - score_width - self.spacer - self.coin_width, self.spacer))
        self.coin_ani_count += self.coin_rotation_rate
        if self.coin_ani_count >= len(self.coin_ani) -1:
            self.coin_ani_count = 0
        self.health_bar[0] = pygame.transform.scale(self.health_bar[0], (int((player.hp / player.max_hp)* 100), 100))
        world.blit(self.health_bar[1], (worldx - 105, 10))
        world.blit(self.health_bar[0], (worldx - 105, 10))



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

        #print(self.chosen_ledge)


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

        # Chest Collision
        for chest in chests:
            if self.x + self.width > chest.x and self.x < chest.x + chest.width and self.y + self.width > chest.y and self.y < chest.y + chest.width:
                chest.triggered = True





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
        if self.hp <= 1:
            self.hp = self.max_hp

class Platform(object):
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

class enemy(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walk_count = 0
        self.direction = 0
        self.run_r = []
        self.run_l = []
        self.jump_r = []
        self.jump_l = []
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
        if self.is_jump and self.jump_vel > 0:
            if self.direction >= 0:
                world.blit(self.jump_r[0], (self.x, self.y))
            else:
                world.blit(self.jump_l[0], (self.x, self.y))
        elif self.is_jump and self.jump_vel < 0:
            if self.direction >= 0:
                world.blit(self.jump_r[1], (self.x, self.y))
            else:
                world.blit(self.jump_l[1], (self.x, self.y))
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
            #print("right>")
            self.collision(self.vel, 0)

        # Walking Left
        elif self.direction == -1:
            #print("left<")
            self.collision(self.vel * -1, 0)

        # Jumping
        if self.is_jump is True:
            #print("jumping!")
            if self.collision(0, self.jump_vel * - 1):
                self.is_jump = False
                self.jump_vel = self.max_jump_vel
                #print("jump: {j}".format(j=self.jump_vel))
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
                self.jump_vel = self.max_jump_vel



    def collision(self, x, y):
        collision = False
        count = 0
        while collision is False and count < len(platforms):
            if self.x + self.width + x > platforms[count].dimensions[0] and self.x + x < platforms[count].dimensions[1] and self.y + self.height + y > platforms[count].dimensions[2] and self.y + y < platforms[count].dimensions[3]:
                collision = True
                if self.y + self.height < platforms[count].dimensions[2]:
                    self.current_platform[0] = (platforms[count].dimensions[0], platforms[count].dimensions[2])
                    self.current_platform[1] = (platforms[count].dimensions[1], platforms[count].dimensions[2])
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
        # loading sprites
        self.bs = spritesheet.spritesheet(os.path.join('images/red_guy', 'blink.png'))
        self.rs = spritesheet.spritesheet(os.path.join('images/red_guy', 'run_r.png'))
        self.js = spritesheet.spritesheet(os.path.join('images/red_guy', 'jump.png'))
        self.still = self.bs.image_at((0, 0, 100, 100), (0, 0, 0))
        self.still = pygame.transform.scale(self.still, (48, 48))
        self.run_r = self.rs.load_strip((0, 0, 100, 100),  18, (0, 0, 0))
        self.idle = self.bs.load_strip((0, 0, 100, 100),  11, (0, 0, 0))
        self.jump_r = self.js.load_strip((0, 0, 100, 100), 2, (0, 0, 0))
        self.run_l = []
        self.jump_l = []
        # character variables
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
        self.find_ledges()
        self.jump_height, self.jump_width = self.find_max_height()
        self.chosen_ledge = []
        self.jump_point = 1900
        self.choose_ledge()
        self.current_platform = [(0,0), (0,0)]




        for i in range(0, len(self.jump_r)):
            self.jump_r[i] = pygame.transform.scale(self.jump_r[i], (48,48))
            self.jump_l.append(pygame.transform.flip(self.jump_r[i], True, False))
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
            max_height += self.jump_vel
            max_width += self.vel
            self.jump_vel -= uni_grav_acel

        self.jump_vel = self.max_jump_vel
        return round(max_height), round(max_width * 2)


    def ai(self):
        self.throw_count += 1
        if self.throw_count >= 100 and len(projectiles) < 5:
            self.throw_acorn()
            self.throw_count = 0
        if self.is_jump is False and self.chosen_ledge != [0,0,'0']:
            self.choose_ledge()

        if self.chosen_ledge == [0,0,'0']:
            self.stand()
        elif self.x + self.width <= self.chosen_ledge[0] and self.y + self.height > self.chosen_ledge[1]: #if npc is to the left of and below the chosen ledge
            self.move_right()
            #print("right>")
            if self.is_jump is False:
                if self.jump_point == self.current_platform[1][0]:
                    if self.x >= self.jump_point - self.vel:
                        self.jump()
                elif self.x + self.width >= self.jump_point:  #if npc is not currently jumping and right edge of npc is past jump point
                    self.jump()

        elif self.x >= self.chosen_ledge[0] and self.y + self.height > self.chosen_ledge[1]: #if npc is to the right of and below the chosen ledge
                self.move_left()
                if self.is_jump is False:
                    #print("x: {x} jump_point: {j}".format(x=self.x, j=self.jump_point))
                    if self.jump_point == self.current_platform[0][0]:
                        #print("here?")
                        if self.x <= self.jump_point - self.vel:
                            self.jump()
                    elif self.x <= self.jump_point:
                        #print("jump!")
                        self.jump()






    def find_jump_point(self):
        height_diff = self.chosen_ledge[1] - (self.y + self.height)
        jump_width = 0
        collide = False
        while height_diff < 0 and height_diff > -2000:
            height_diff += self.jump_vel - uni_grav_acel
            jump_width += self.vel

        if self.chosen_ledge[2] == 'l': #moving right
            if self.chosen_ledge[0] - jump_width < self.current_platform[1][0]:
                self.jump_point = self.chosen_ledge[0] - jump_width
            else:
                self.jump_point = self.current_platform[1][0]
        else: # moving left
            if self.chosen_ledge[0] + jump_width > self.current_platform[0][0]:
                self.jump_point = self.chosen_ledge[0] + jump_width
            else:
                self.jump_point = self.current_platform[0][0]



    def find_ledges(self):
        temp = []
        for i in level_platforms:
            if i.label != 'ground':
                temp.append([i.x, i.surface, 'l', i.label, i.height])
                temp.append([i.x+i.width, i.surface, 'r', i.label, i.height])
                #print("x: {x}, surface: {s}".format(x=i.x+i.width, s=i.surface))
        self.ledges = sorted(temp, key = lambda x:x[1])


    def choose_ledge(self):
        #print("choosing")
        self.chosen_ledge = [0,0,'0']
        for i in range(len(self.ledges)-1, -1, -1):
            if self.ledges[i][1] <= self.y + self.height and self.chosen_ledge[1] < self.ledges[i][1]:  #if ledge above npc's head and lower than current ledge
                if self.x <= self.ledges[i][0] and self.ledges[i][2] == 'l':
                    if self.current_platform[1][0] + self.jump_width >= self.ledges[i][0]:
                        self.chosen_ledge = self.ledges[i]
                        self.find_jump_point()
                        #print("new! {l}".format(l=self.chosen_ledge))
                elif self.x >= self.ledges[i][0] and self.ledges[i][2] == 'r':
                    if self.current_platform[0][0] - self.jump_width <= self.ledges[i][0]:
                        self.chosen_ledge = self.ledges[i]
                        self.find_jump_point()
                        #print("new! {l}".format(l=self.chosen_ledge))
                else:
                    self.chosen_ledge = [0,0,'0']




    def throw_acorn(self):
        tx = player.x - self.x
        ty = player.y - self.y
        z = 100 / (abs(tx) + abs(ty))
        dx = tx * z
        dy = ty * z
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
        self.throw_count = 0



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
        self.throw_count += 1
        #print(self.throw_count)
        if self.throw_count >= 100 and len(projectiles) < 5:
            self.throw_acorn()
            #print("throw!")
            self.throw_count = 0
        if self.y <= player.y and pygame.time.get_ticks() % 100 == 0:
            self.jump()




    def throw_acorn(self):
        if player.direction == 0:
            tx = player.x - self.x
            ty = player.y - self.y
        elif player.direction == 1:
            tx = (player.x - self.x)
            ty = player.y - self.y
        else:
            tx = (player.x - self.x)
            ty = player.y - self.y
        z = 100 / (abs(tx) + abs(ty))
        dx = tx * z
        dy = ty * z
        projectiles.append(acorn(self.x, self.y, dx, dy))

class Ani_Item(object):
    def __init__(self, x, y):
        object.__init__(self)
        self.x = x
        self.y = y
        self.ss = []
        self.img_ani = []
        self.ani_count = 0
        self.rotation_rate = 0
        self.width = 0
        self.height = 0
        self.settled = False
        self.hit_box = [self.x, self.y, self.x + self.width, self.y + self.height]

        for i in range(0, len(self.img_ani)):
            self.img_ani[i] = pygame.transform.scale(self.img_ani[i], (40,40))

    def draw(self, world):
        if self.settled is False:
            self.gravity()
        world.blit(self.img_ani[round(self.ani_count)], (self.x, self.y))
        self.ani_count += self.rotation_rate
        if self.ani_count >= len(self.img_ani) -1:
            self.ani_count = 0

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

class Coin(Ani_Item):
    def __init__(self, x, y):
        object.__init__(self)
        self.x = x
        self.y = y
        self.ss = spritesheet.spritesheet(os.path.join('images/object', 'coin100.png'))
        self.img_ani = self.ss.load_strip((0, 0, 100, 100), 16, (0, 0, 0))
        self.ani_count = 0
        self.rotation_rate = .3
        self.width = 40
        self.height = 40
        self.settled = False
        #self.coordinates = [self.x, self.y, self.x + self.width, self.y + self.height]

        for i in range(0, len(self.img_ani)):
            self.img_ani[i] = pygame.transform.scale(self.img_ani[i], (self.width, self.height))

class Chest(Ani_Item):
    def __init__(self, x, y):
        object.__init__(self)
        self.x = x
        self.y = y
        self.ss = spritesheet.spritesheet(os.path.join('images/object', 'chest100.png'))
        self.img_ani = self.ss.load_strip((0, 0, 100, 100), 6, (0, 0, 0))
        self.ani_count = 0
        self.width = 60
        self.height = 60
        self.coin_value = 50
        self.settled = False
        self.triggered = False

        for i in range(0, len(self.img_ani)):
            self.img_ani[i] = pygame.transform.scale(self.img_ani[i], (self.width, self.height))
        #self.coordinates = [self.x, self.y, self.x + self.width, self.y + self.height]

    def draw(self, world):
        if self.settled is False:
            self.gravity()
        if self.triggered:
            if self.ani_count < len(self.img_ani) - 1:
                world.blit(self.img_ani[round(self.ani_count)], (self.x, self.y))
                self.ani_count += .25
            else:
                delete_chest(self)
                if chests == []:
                    menu.game_win = True
        else:
            world.blit(self.img_ani[0], (self.x, self.y))


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
            #print("hit!")


class acorn(projectile):
    def __init__(self, x, y, dx, dy):
        projectile.__init__(self, x, y, dx, dy)
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.ass = spritesheet.spritesheet(os.path.join('images/object', 'sm_acorn.png'))
        self.img = self.ass.image_at((0, 0, 24, 19), (0, 0, 0))
        self.vel = 15
        self.img_count = 0
        self.damage = 1
        self.width = self.img.get_width()
        self.height = self.img.get_height()



def draw_world(world):
    world.blit(backdrop, backdropbox)
    #print(menu.game_win)
    if menu.game_win == False:
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

        for enemy in enemies:
            pygame.draw.circle(world, red, (enemy.chosen_ledge[0], enemy.chosen_ledge[1]), 4)
            pygame.draw.circle(world, blue, enemy.current_platform[0], 4)
            pygame.draw.circle(world, blue, enemy.current_platform[1], 4)
            pygame.draw.circle(world, black, (enemy.jump_point, enemy.chosen_ledge[1]), 4)

        if grid_on == True:
            draw_grid(world)
        if pnums == True:
            draw_pnums(world)

    else:
        menu.game_over(world)

    for chest in chests:
        chest.draw(world)


def delete_chest(trip_chest):
    try:
        player.coin_count += trip_chest.coin_value
        chests.remove(trip_chest)
        print(chests)

    except:
        print("Chest not found!")


def load_level(level):
    for platform in level[0]:
        platforms.append(platform)
    for coin in level[1]:
        coins.append(coin)
    for chest in level[2]:
        chests.append(chest)
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

def display_pnums(pnums):
    if pnums == False:
        pnums = True
    else:
        pnums = False
    return pnums

def draw_pnums(world):
    pfont = pygame.font.SysFont('0', 40)
    for plat in platforms:
        plabel = pfont.render(str(plat.label), 2, black)
        world.blit(plabel, (plat.x + (plat.width //2), (plat.y + (plat.height//2))))

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
menu = Menu()
backdrop = pygame.image.load(os.path.join('images', 'Background1920x1080.png')).convert()
backdropbox = world.get_rect()
ground = (os.path.join('images', 'full_ground1920x64.png'))
sml_platform = (os.path.join('images', '1TilePlatform64x64.png'))
mdm_platform = (os.path.join('images', '2TilePlatform128x64.png'))
grid_on = False
pnums = False
game_win = False


# key presses

# world variables
uni_jump_vel = 16
uni_grav_acel = 1.1
uni_run_vel = 5

red = (227, 41, 44)
black = (0, 0, 0)
blue = (41, 156, 227)
white = (254, 254, 254)


"""
LEVEL CREATION
"""
level_platforms = []
level_coins = []
level_chests = []
level_enemies = []
level_player = []


level_platforms.append(Platform(0, worldy-64, 1920, 64, ground, "ground"))
level_platforms.append(Platform(0, 348, 128, 64, mdm_platform, 1))
level_platforms.append(Platform(160, 288, 64, 64, sml_platform, 2))
level_platforms.append(Platform(320, 160, 64, 64, sml_platform, 3))
level_platforms.append(Platform(446, 96, 64, 64, sml_platform, 4))
level_platforms.append(Platform(1664, 832, 128, 64, mdm_platform, 5))
level_platforms.append(Platform(1408, 704, 128, 64, mdm_platform, 6))
level_platforms.append(Platform(1152, 512, 128, 64, mdm_platform, 7))
level_platforms.append(Platform(896, 384, 128, 64, mdm_platform, 8))
level_platforms.append(Platform(worldx-64, 960, 64, 64, sml_platform, 9))
level_platforms.append(Platform(1280, 640, 64, 64, sml_platform, 10))
level_platforms.append(Platform(1040, 500, 64, 64, sml_platform, 11))
level_platforms.append(Platform(1536, 768, 64, 64, sml_platform, 12))
level_platforms.append(Platform(640, 640, 128, 64, mdm_platform, 13))
level_platforms.append(Platform(448, 448, 64, 64, sml_platform, 14))
level_platforms.append(Platform(576, 576, 64, 64, sml_platform, 15))
level_platforms.append(Platform(320, 320, 64, 64, sml_platform, 16))


for i in level_platforms:
    cx = i.x + 12
    cy = i.y - 22
    if i.width == 64 or i.width == 128:
        level_coins.append(Coin(cx, cy))
    if i.width == 128:
        level_coins.append(Coin(cx+64, cy))

coin_x = 100
for i in range(0, 15):
    level_coins.append(Coin(coin_x, worldy-100))
    coin_x += 40

level_enemies.append(red_guy(1400, 980))
level_enemies.append(red_guy(660, 600))
#level_enemies.append(blue_guy(200, 400))

level_player = [worldx - 100, worldy-200]

level_chests.append(Chest(1700, 900))

demo_level = [level_platforms, level_coins, level_chests, level_enemies, level_player]












# create world platforms.platforms
platforms = []
coins = []
chests = []
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
            if event.key == pygame.K_p:
                pnums = display_pnums(pnums)
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
