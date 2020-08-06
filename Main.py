import pygame
import sys
import os
import spritesheet
import Level_Creator

pygame.init()

"""
platforms.platformS
"""


class Menu(object):
    def __init__(self):
        object.__init__(self)
        self.x = worldx
        self.score_y = 5
        self.font_size = 42
        self.max_font_size = 90
        self.score_font = pygame.font.Font(game_font, self.font_size)
        self.cs = spritesheet.spritesheet(os.path.join('images/object', 'coin100.png'))
        self.coin_ani_count = 0
        self.coin_rotation_rate = .2
        self.coin_ani = self.cs.load_strip((0, 0, 100, 100), 16, (0, 0, 0))
        self.coin_ani_scale = self.coin_ani[0]
        self.player_ani_count = 0
        self.temp_ani = 0
        self.player_position_x = 0
        self.player_position_y = 0
        self.dx = 0
        self.dy = 0
        self.player_height = player.height
        self.max_player_height = 220
        self.menu_font = pygame.font.Font(game_font, self.max_font_size)
        self.score_spacer = 5
        self.score_width = 0
        self.transition_speed = 10
        self.transition_count = 0
        self.score_width = 0
        self.score_height = self.font_size
        self.transition_diff = round((self.x + (self.score_width / 2) / (worldx / 2)))
        self.win_state = False
        self.blink = 0

        for i in range(0, len(self.coin_ani)):
            self.coin_ani[i] = pygame.transform.scale(self.coin_ani[i], (self.font_size, self.font_size))

    def game_win(self, world):
        self.score_font = pygame.font.Font(game_font, self.font_size)
        coin_score = self.score_font.render(str(player.coin_count), 2, white)
        coin_score_o = self.score_font.render(str(player.coin_count), 2, black)
        self.score_width = coin_score.get_width()
        """
        if self.player_position_x == 0:
            self.player_position_x = player.x
            self.player_position_y = player.y
            tx = (worldx // 2) - self.max_player_height - self.player_position_x
            ty = 160 - self.player_position_y
            z = 100 / (abs(tx) + abs(ty))
            self.dx = tx * z
            self.dy = ty * z
            if player.direction == 1:
                self.dance_ani = player.dance_l
            else:
                self.dance_ani = player.dance_r
        """

        if self.win_state == True:
            if self.x - (self.score_width // 2) > worldx // 2:
                # Moving score to middle the screen
                self.coin_ani_scale = pygame.transform.scale(self.coin_ani[round(self.coin_ani_count)], (self.font_size, self.font_size))
                world.blit(coin_score_o, (self.x - self.score_spacer - self.score_width + 2, round(self.score_y) + 2))
                world.blit(coin_score, (self.x - self.score_spacer - self.score_width, round(self.score_y)))
                world.blit(self.coin_ani_scale, (self.x - self.score_spacer - self.score_width - self.score_spacer - self.font_size - 1, round(self.score_y) - 1))
                self.coin_ani_count += self.coin_rotation_rate
                if self.coin_ani_count >= len(self.coin_ani) - 1:
                    self.coin_ani_count = 0
                self.x -= self.transition_speed
                if self.score_y < worldy // 2:
                    self.score_y += abs(((self.score_y - (worldy / 2)) // self.transition_diff)) * 6
                if self.font_size < self.max_font_size:
                    self.font_size += 1
                self.score_spacer += round((self.max_font_size - self.font_size) // self.transition_diff)
                """
                # Moving player, while dancing to middle of the screen
                    # Scale animation up
                    if self.player_ani_count >= len(player.dance_r) - 1:
                        self.player_ani_count = 0
                    self.temp_ani = pygame.transform.scale(self.dance_ani[self.player_ani_count], (self.player_height, self.player_height))
                    world.blit(self.temp_ani, (self.player_position_x, self.player_position_y))
                    # Move animation to center of screen
                    increment = self.transition_speed / (abs(self.dx) + abs(self.dy))
                    if self.player_position_x <= worldx // 2 - 10 or self.player_position_x >= worldx // 2 + 10:
                        self.player_position_x += round(self.dx * increment)
                    if self.player_position_y <= 150 or self.player_position_y >= 170:
                        self.player_position_y += round(self.dy * increment)
                    print("{x}, {y}".format(x = self.player_position_x, y = self.player_position_y))
                    # Scaling up size of animation
                    self.player_ani_count += 1
                    if self.player_height < self.max_player_height:
                        self.player_height += 5
                """
            else:
                if self.coin_ani[0].get_width != self.font_size:
                    for i in range(0, len(self.coin_ani)):
                        self.coin_ani[i] = pygame.transform.scale(self.coin_ani[i], (self.font_size, self.font_size))
                world.blit(coin_score_o, (self.x - self.score_spacer - self.score_width + 2, round(self.score_y) + 2))
                world.blit(coin_score, (self.x - self.score_spacer - self.score_width, round(self.score_y)))

                world.blit(self.coin_ani[round(self.coin_ani_count)], (self.x - self.score_spacer - self.score_width - self.score_spacer - self.font_size, round(self.score_y)))
                self.coin_ani_count += self.coin_rotation_rate
                if self.coin_ani_count >= len(self.coin_ani) -1:
                    self.coin_ani_count = 0
                you_won = self.menu_font.render("YOU WON!", 2, white)
                you_won_o = self.menu_font.render("YOU WON!", 2, black)
                you_won_width = you_won.get_width()
                play_again = self.menu_font.render("PLAY AGAIN?", 2, white)
                play_again_o = self.menu_font.render("PLAY AGAIN?", 2, black)
                play_again_width = play_again.get_width()
                y_n = self.menu_font.render("(y/n)", 2, white)
                y_n_o = self.menu_font.render("(y/n)", 2, black)
                y_n_width = y_n.get_width()
                self.blink += 1

                world.blit(you_won_o, (round(((worldx // 2) - (you_won_width // 2) + 2)), (round(self.score_y - self.score_spacer - self.max_font_size + 2))))
                world.blit(you_won, (round((worldx // 2) - (you_won_width // 2)), round(self.score_y - self.score_spacer - self.max_font_size)))
                world.blit(play_again_o, (round((worldx // 2) - (play_again_width // 2) + 2), round(self.score_y + self.max_font_size + self.score_spacer + 2)))
                world.blit(play_again, (round((worldx // 2) - (play_again_width // 2)), round(self.score_y +  self.max_font_size + self.score_spacer)))
                if self.blink < 30:
                    world.blit(y_n_o, (round((worldx // 2) - (y_n_width // 2) + 2), round(self.score_y + (self.max_font_size * 2) + (self.score_spacer * 2) + 2)))
                    world.blit(y_n, (round((worldx // 2) - (y_n_width // 2)), round(self.score_y + (self.max_font_size * 2) + (self.score_spacer * 2))))
                if self.blink > 50:
                    self.blink = 0



    def game_loss(self, world):
        pass

class HUD(object):
    def __init__(self):
        self.font = pygame.font.Font(game_font, 42)
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
        coin_score_o = self.font.render(str(player.coin_count), 2, black)

        score_width = coin_score.get_width()
        world.blit(coin_score_o, (worldx - self.spacer - score_width + 1, self.spacer + 1))
        world.blit(coin_score, (worldx - self.spacer - score_width, self.spacer))
        world.blit(self.coin_ani[round(self.coin_ani_count)], (worldx - self.spacer - score_width - self.spacer - self.coin_width, self.spacer))
        self.coin_ani_count += self.coin_rotation_rate
        if self.coin_ani_count >= len(self.coin_ani) -1:
            self.coin_ani_count = 0
        if player.hp >= 0:
            self.health_bar[1] = pygame.transform.scale(self.health_bar[1], (int((player.hp / player.max_hp) * 100), 100))
        world.blit(self.health_bar[0], (worldx - 105, 10))
        world.blit(self.health_bar[1], (worldx - 105, 10))



# classes and functions
class Player(object):
    def __init__(self, x, y):
        object.__init__(self)
        # load character sprite sheets
        self.rs = spritesheet.spritesheet(os.path.join('images/raccoon', 'raccoon_run_r.png'))
        self.ss = spritesheet.spritesheet(os.path.join('images/raccoon', 'raccoon_idle_r.png'))
        self.js = spritesheet.spritesheet(os.path.join('images/raccoon', 'raccoon_jump_r.png'))
        self.ds = spritesheet.spritesheet(os.path.join('images/raccoon', 'raccoon_dance_r.png'))
        self.ks = spritesheet.spritesheet(os.path.join('images/raccoon', 'raccoon_ko_r.png'))
        self.rls = spritesheet.spritesheet(os.path.join('images/raccoon', 'raccoon_run_l.png'))
        self.sls = spritesheet.spritesheet(os.path.join('images/raccoon', 'raccoon_idle_l.png'))
        self.jls = spritesheet.spritesheet(os.path.join('images/raccoon', 'raccoon_jump_l.png'))
        self.dls = spritesheet.spritesheet(os.path.join('images/raccoon', 'raccoon_dance_l.png'))
        self.kls = spritesheet.spritesheet(os.path.join('images/raccoon', 'raccoon_ko_l.png'))
        # create animation lists
        self.run_r = self.rs.load_strip((20, 20, 100, 100),  11, (0, 0, 0))
        self.idle_r = self.ss.load_strip((20, 20, 100, 100),  11, (0, 0, 0))
        self.jump_r = self.js.load_strip((20, 20, 100, 100), 11, (0, 0, 0))
        self.dance_r = self.ds.load_strip((20, 20, 100, 100), 11, (0, 0, 0))
        self.ko_r = self.ks.load_strip((20, 20, 100, 100), 10, (0, 0, 0))
        self.run_l = self.rls.load_strip((20, 20, 100, 100),  11, (0, 0, 0))
        self.idle_l = self.sls.load_strip((20, 20, 100, 100),  11, (0, 0, 0))
        self.jump_l = self.jls.load_strip((20, 20, 100, 100), 11, (0, 0, 0))
        self.dance_l = self.dls.load_strip((20, 20, 100, 100), 11, (0, 0, 0))
        self.ko_l = self.kls.load_strip((20, 20, 100, 100), 10, (0, 0, 0))

        # character variables
        self.x = x
        self.y = y
        self.max_hp = 10
        self.hp = self.max_hp
        self.ani_speed = 2
        self.walk_count = 0
        self.direction = 0
        self.last_direction = 1
        self.is_jump = False
        self.height = 70
        self.width = 40
        self.gravity = uni_grav_acel
        self.max_jump_vel = 20
        self.jump_vel = self.max_jump_vel
        self.is_falling = False
        self.vel = 5
        self.coin_count = 0
        self.current_platform = [(0,0), (0,0)]
        self.melee_length = 50
        self.melee_damage = 150
        self.melee_direction = 0
        self.hit_box = [0, 0, 0, 0]
        self.attack_box = [0, 0, 0, 0]
        self.knocked_out = False
        self.jump_height, self.jump_width = self.find_max_height()


    def draw(self, world):
        self.move()
        if self.knocked_out == True:
            if self.walk_count < len(self.ko_r):
                print("here")
                if self.last_direction > 1:
                    world.blit(self.ko_r[self.walk_count], (round(self.x), round(self.y)))
                else:
                    world.blit(self.ko_l[self.walk_count], (round(self.x), round(self.y)))
                self.walk_count += 1
            else:
               world.blit(self.ko_r[self.walk_count - 1], (round(self.x), round(self.y)))
        else:
            self.hit_box = [self.x + 5, self.y + 5, self.width - 5, self.height - 5]
            if self.last_direction > 0:
                self.attack_box = [self.x, self.y, self.width + self.melee_length, self.height]
            else:
                self.attack_box = [self.x - self.melee_length, self.y, self.width + self.melee_length, self.height]
            #pygame.draw.rect(world, blue, self.attack_box, 1)
            #pygame.draw.rect(world, red, self.hit_box, 1)
            if self.walk_count >= (self.ani_speed * len(self.run_r)) - 1:
                self.walk_count = 0
            if self.direction == 0 and self.last_direction == 1:
                world.blit(self.idle_r[self.walk_count // self.ani_speed], (int(self.x), int(self.y)))
            elif self.direction == 0 and self.last_direction == -1:
                world.blit(self.idle_l[self.walk_count // self.ani_speed], (int(self.x), int(self.y)))
            elif self.is_jump:
                if self.direction == 1:
                    world.blit(self.jump_r[self.walk_count // self.ani_speed], (int(self.x), int(self.y)))
                else:
                    world.blit(self.jump_l[self.walk_count // self.ani_speed], (int(self.x), int(self.y)))
            elif self.direction == 1:
                world.blit(self.run_r[self.walk_count // self.ani_speed], (self.x, self.y))
            elif self.direction == -1:
                world.blit(self.run_l[self.walk_count // self.ani_speed], (self.x, self.y))

            self.walk_count += 1


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
            if self.collision(0, self.jump_vel * - 1):
                self.is_jump = False
            self.jump_vel -= uni_grav_acel

        # Gravity
        if not self.is_jump:
            if not self.collision(0, self.gravity):
                self.is_falling = True
                self.gravity += uni_grav_acel
            else:
                self.gravity = uni_grav_acel
                self.is_jump = False
                self.jump_vel = self.max_jump_vel
                self.is_falling = False

        # Chest Collision
        """
        for chest in chests:
            if self.x + self.width > chest.x and self.x < chest.x + chest.width and self.y + self.width > chest.y and self.y < chest.y + chest.width:
                chest.triggered = True
        """

    def collision(self, x, y):
        collision = False
        count = 0
        #print("collision: {x}, {y}".format(x=x, y=y))
        while collision is False and count < len(platforms):
            if self.x + self.width + x > platforms[count].dimensions[0] and self.x + x < platforms[count].dimensions[1] and self.y + self.height + y > platforms[count].dimensions[2] and self.y + y < platforms[count].dimensions[3]:
                if self.is_falling or self.is_jump:
                    if y > self.y + self.height - platforms[count].dimensions[2]:
                        self.y = platforms[count].dimensions[2] - self.height
                collision = True
            elif self.x + x < 0 or self.x + self.width + x > worldx:
                collision = True
            elif self.x + self.width + x > platforms[count].dimensions[0] and self.x + x < platforms[count].dimensions[1] and self.y + self.height > platforms[count].dimensions[2] - y and self.y + y < platforms[count].dimensions[3]:
                print("here!")
                collision = True
                self.y = platforms[count].dimensions[2] + self.height
                self.x += x
                self.current_platform[0] = (platforms[count].dimensions[0], platforms[count].dimensions[2])
                self.current_platform[1] = (platforms[count].dimensions[1], platforms[count].dimensions[2])
            count += 1
        if collision == False:
            self.x += x
            self.y = int(y + self.y)
        return collision

    def jump(self):
        if self.is_jump is False and self.is_falling is False:
            self.is_jump = True
            self.walk_count = 0

    def move_right(self):
        if self.direction != 1:
            self.direction = 1
            self.last_direction = 1
        self.walk_count = 0

    def move_left(self):
        if self.direction != -1:
            self.direction = -1
            self.last_direction = -1
            self.walk_count = 0

    def stand(self):
        self.last_direction = self.direction
        self.direction = 0

    def melee(self):
        for enemy in enemies:
            if self.attack_box[0] < enemy.x < self.attack_box[0] + self.attack_box[2] or self.attack_box[0] < enemy.x + enemy.height < self.attack_box[0] + self.attack_box[2] :
                if self.attack_box[1] < enemy.y + enemy.height < self.attack_box[1] + self.attack_box[3]:
                    enemy.hit(self.melee_damage)
                elif self.attack_box[1] < enemy.y < self.attack_box[1] + self.attack_box[3]:
                    enemy.hit(self.melee_damage)

    def coin_collected(self, coin):
        self.coin_count += 1
        coins.remove(coin)

    def hit(self, projectile):
        self.hp -= projectile.damage
        projectiles.remove(projectile)
        #print("hp: {h}".format(h=self.hp))
        if self.hp < 1:
            self.walk_count = 0
            self.knocked_out = True

    def find_max_height(self):
        max_height = 0
        max_width = 0
        while self.jump_vel > 0:
            max_height += self.jump_vel
            max_width += self.vel
            self.jump_vel -= uni_grav_acel

        self.jump_vel = self.max_jump_vel
        return round(max_height), round(max_width)


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
        self.run_away_vel = 0
        self.scared = False


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
                #print("falling!")
                #if self.is_falling:
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
                self.x = round(self.x + x)
                self.current_platform[0] = (platforms[count].dimensions[0], platforms[count].dimensions[2])
                self.current_platform[1] = (platforms[count].dimensions[1], platforms[count].dimensions[2])
            count += 1
        if collision == False:
            self.x = round(self.x + x)
            self.y = int(y + self.y)
        #print(collision)
        return collision

    def jump(self):
        if self.is_jump is False and self.is_falling is False:
            self.is_jump = True
            self.walk_count = 0

    def move_right(self):
        if self.direction != 1:
            self.direction = 1
            self.walk_count = 0

    def move_left(self):
        if self.direction != -1:
            self.direction = -1
            self.walk_count = 0

    def stand(self):
        self.direction = 0

    def hit(self, damage):
        print("I'm scared!")
        self.run_away_vel = damage
        self.direction *= -1
        self.scared = True
        self.is_jump = False


    def ai(self):
        pass


class red_guy(enemy):
    def __init__(self, x, y, level_platforms):
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
        self.find_ledges(level_platforms)
        self.jump_height, self.jump_width = self.find_max_height()
        self.chosen_ledge = []
        self.jump_point = worldy
        self.choose_ledge()
        self.current_platform = [(0,0), (0,0)]
        self.label = "red_guy"




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
        if self.scared and self.run_away_vel > 0:
            if self.run_away_vel > 0:
                if self.direction == -1:
                    self.move_left()
                else:
                    self.move_right()
            self.run_away_vel -= 1
        elif self.scared and self.run_away_vel <= 0:
            self.scared = False
            self.run_count = 0
            self.choose_ledge()
        else:
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


    def hit(self, damage):
        self.run_away_vel = damage
        self.direction *= -1
        self.scared = True



    def find_jump_point(self):
        height_diff = self.chosen_ledge[1] - (self.y + self.height)
        jump_width = 0
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



    def find_ledges(self, level_platforms):
        temp = []
        for i in level_platforms:
            if i.label != 'ground':
                temp.append([i.x, i.surface, 'l', i.label, i.height])
                temp.append([i.x+i.width, i.surface, 'r', i.label, i.height])
                #print("x: {x}, surface: {s}".format(x=i.x+i.width, s=i.surface))
        self.ledges = sorted(temp, key = lambda x:x[1])


    def choose_ledge(self):
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
        tx = player.x - self.x
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
        self.player_collision()
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

    def player_collision(self):
        if self.x + self.width > player.x and self.x < player.x + player.width and self.y + self.height > player.y and self.y < player.y + player.height:
            player.coin_collected(self)

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
        if player.x > self.x and player.x < self.x + self.width and player.y + (player.height // 2) > self.y and player.y + (player.height //2 ) < self.y + self.height:
            self.triggered = True
            if self.ani_count < len(self.img_ani) - 1:
                world.blit(self.img_ani[round(self.ani_count)], (self.x, self.y))
                self.ani_count += .25
            else:
                delete_chest(self)
                if chests == []:
                    menu.win_state = True
                    self.triggered = False
                    self.ani_count = 0
        else:
            if self.settled is False:
                self.gravity()
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
    #print(menu.win_state)
    if menu.win_state == False:
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
                try:
                    projectiles.remove(proj)
                except ValueError:
                    print("ValueError trying to remove projectile")
        if e_ledge_finder:
            for enemy in enemies:
                pygame.draw.circle(world, red, (enemy.chosen_ledge[0], enemy.chosen_ledge[1]), 4)
                pygame.draw.circle(world, blue, enemy.current_platform[0], 4)
                pygame.draw.circle(world, blue, enemy.current_platform[1], 4)
                pygame.draw.circle(world, black, (enemy.jump_point, enemy.chosen_ledge[1]), 4)


        if pnums == True:
            draw_pnums(world)

    elif menu.win_state == True:
        menu.game_win(world)
    #elif player.knocked_out == True:
        #menu.game_loss(world)
    if grid_on == True:
        draw_grid(world)
    for chest in chests:
        chest.draw(world)


def delete_chest(trip_chest):
    try:
        player.coin_count += trip_chest.coin_value
        chests.remove(trip_chest)
        print(chests)

    except:
        print("Chest not found!")

def clear_level():
    platforms.clear()
    coins.clear()
    chests.clear()
    enemies.clear()
    for i in enemies:
        print(i.label)


def load_level(level):
    print("Load Level!")
    game_win = False
    for platform in level[0]:
        platforms.append(platform)
    for coin in level[1]:
        coins.append(coin)
    for chest in level[2]:
        chests.append(chest)
    for enemy in level[3]:
        enemies.append(enemy)
    #player.x = level[4][0]
    #player.y = level[4][1]

def create_level():
        level_platforms = []
        level_coins = []
        level_chests = []
        level_enemies = []
        level_player = [Player(0, 0)]
        level_platforms = (Level_Creator.level_creator(worldx, worldy, level_player[0].jump_width, level_player[0].jump_height))
        """
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

        level_enemies.append(red_guy(1400, 980, level_platforms))
        level_enemies.append(red_guy(660, 600, level_platforms))
        level_enemies.append(red_guy(340, 275, level_platforms))

        level_player = [0, 0]

        level_chests.append(Chest(450, 56))

        """
        return [level_platforms, level_coins, level_chests, level_enemies, level_player]

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


def e_ledge_find(e_ledge_finder):
    if e_ledge_finder:
        e_ledge_finder = False
    else:
        e_ledge_finder = True
    return e_ledge_finder

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
display_mode = pygame.display.Info()
worldx = display_mode.current_w
worldy = display_mode.current_h
fps = 40
ani = 4
clock = pygame.time.Clock()
pygame.init()
world = pygame.display.set_mode((worldx, worldy), pygame.FULLSCREEN)
backdrop = pygame.image.load(os.path.join('images', 'Background1920x1080.png')).convert()
backdrop = pygame.transform.scale(backdrop, (worldx, worldy))
backdropbox = world.get_rect()
ground = (os.path.join('images', 'full_ground1920x64.png'))
sml_platform = (os.path.join('images', '1TilePlatform64x64.png'))
mdm_platform = (os.path.join('images', '2TilePlatform128x64.png'))
grid_on = False
pnums = False
e_ledge_finder = False


# key presses

# world variables
uni_grav_acel = 1.098

red = (227, 41, 44)
black = (0, 0, 0)
blue = (41, 156, 227)
white = (254, 254, 254)

game_font = "consolab.ttf"


"""
LEVEL CREATION
"""

demo_level = create_level()

platforms = []
coins = []
chests = []
enemies = []
projectiles = []
player = Player(0,0)
hud = HUD()
menu = Menu()



"""
Main Loop
"""
# game loop
load_level(demo_level)
main = True
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
            if event.key == pygame.K_w:
                e_ledge_finder = e_ledge_find(e_ledge_finder)
            if menu.win_state == True:
                if event.key == pygame.K_y:
                    menu.win_state = False
                    clear_level()
                    del menu
                    menu = Menu()
                    player.hp = player.max_hp
                    demo_level = create_level()
                    load_level(demo_level)
                if event.key == pygame.K_n:
                    main = False
                    sys.exit()
            if event.key == pygame.K_c:
                player.melee()
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
