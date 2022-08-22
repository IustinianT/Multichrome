from UtilityFunctions import *
from Projectile import *
from Items import *
from Healthbar import *

##### ENEMY
class Enemy():
    def __init__(self, x, y, width, colour, damage, collision_damage, hp, vel, element, fire_effect, ice_effect, poison_effect, void_effect, duration):
        self.x = x
        self.y = y
        self.width = width
        self.colour = colour
        self.vel = vel
        self.max_vel = vel
        self.hp = hp
        self.max_hp = hp
        self.healthbar_colour = [0,255,0]
        self.height = width
        self.size = "small"

        self.damage = damage
        collision_damage = collision_damage

        self.element = element
        self.debuff_fire = [False,0,0]
        self.debuff_ice = [False,0,0]
        self.debuff_poison = [False,0,0] 
        self.effect_fire = fire_effect
        self.effect_ice = ice_effect
        self.effect_poison = poison_effect
        self.effect_void = void_effect
        self.duration = duration

    def movement(self, screen, player):
        speed = normalise_distance(player.x + player.width/2, player.y + player.height/2, self.x, self.y, self.vel)
        self.x += speed[0]
        self.y += speed[1]

    def draw_enemy(self, screen):
        pass

    def draw_healthbar(self, screen):
        if self.size == "small":
            pygame.draw.rect(screen, (self.healthbar_colour), (self.x-self.width*2, self.y+self.width, self.width*4*(self.hp/self.max_hp), 5))
        if self.size == "big":
            pygame.draw.rect(screen, (self.healthbar_colour), (self.x-self.width, self.y+self.width+5, self.width*2*(self.hp/self.max_hp), 8))   

    def update_healthbar(self):
        if self.hp/self.max_hp >= 0:
            self.healthbar_colour[1] = 255*(self.hp/self.max_hp)
            self.healthbar_colour[0] = 255*(1-self.hp/self.max_hp)

    def alive(self):
        if self.hp <= 0:
            return False
        return True

    def apply_debuff(self, weapon):
        if self.debuff_fire[0] == True:
            if self.colour != red:
                self.hp -= weapon.effect_fire
            self.debuff_fire[2] -= 1
        if self.debuff_ice[0] == True:
            if self.colour != blue:
                self.vel = self.max_vel * weapon.effect_ice
            self.debuff_ice[2] -= 1
        if self.debuff_poison[0] == True and self.colour != green_dark:
            if self.type != "boss":
                self.hp *= weapon.effect_poison
                self.debuff_poison[2] -= 1
        
    def debuff_expire_check(self):
        if self.debuff_fire[2] <= 0:
            self.debuff_fire[0] = False
        if self.debuff_ice[2] <= 0:
            self.debuff_ice[0] = False
            self.vel = self.max_vel
        if self.debuff_poison[2] <= 0:
            self.debuff_poison[0] = False

    def check_fire(self):
        return self.debuff_fire[0]

    def check_ice(self):
        return self.debuff_ice[0]

    def check_poison(self):
        return self.debuff_poison[0]

    def display_debuffs(self,screen, fire, ice, poison):
        if self.size == "small":
            if self.check_fire():
                screen.blit(fire,(self.x-18, self.y-25))
            if self.check_ice():
                screen.blit(ice,(self.x+2, self.y-25))
            if self.check_poison():
                screen.blit(poison,(self.x+22, self.y-25))

        if self.size == "big":
            if self.check_fire():
                screen.blit(fire,(self.x-self.width+25, self.y-self.width-25))
            if self.check_ice():
                screen.blit(ice,(self.x-5, self.y-self.width-25))
            if self.check_poison():
                screen.blit(poison,(self.x+self.width-35, self.y-self.width-25))

    def on_death_spawn_item(self, items_common, items_rare, items_epic, items_legendary, room):
        spawn_item_check = random.randint(0,10000)
        item_rarity_check = random.randint(0,10000)
        if self.type != "boss" and self.type != "bonus":
            if spawn_item_check <= 2500:
                ## COMMON - 74%, RARE - 20%, EPIC - 5%, LEGENDARY - 1%
                if item_rarity_check <= 7400: #7400
                    choise = random.choice(items_common)
                    item = Item(self.x, self.y, 15, choise.colour, choise.description, choise.icon, choise.rarity, choise.name, choise.stackable[0], choise.stackable[1])
                    room.items.append(item)
                if item_rarity_check >= 7401 and item_rarity_check <= 9400: # 7401-9400
                    choise = random.choice(items_rare)
                    item = Item(self.x, self.y, 15, choise.colour, choise.description, choise.icon, choise.rarity, choise.name, choise.stackable[0], choise.stackable[1])
                    room.items.append(item)
                if item_rarity_check >= 9401 and item_rarity_check <= 9900: # 9401-9900
                    choise = random.choice(items_epic)
                    item = Item(self.x, self.y, 15, choise.colour, choise.description, choise.icon, choise.rarity, choise.name, choise.stackable[0], choise.stackable[1])
                    room.items.append(item)
                if item_rarity_check >= 9901 and item_rarity_check <= 10000: # 9901-10000
                    choise = random.choice(items_legendary)
                    item = Item(self.x, self.y, 15, choise.colour, choise.description, choise.icon, choise.rarity, choise.name, choise.stackable[0], choise.stackable[1])
                    room.items.append(item)
        elif self.type == "boss" or self.type == "bonus":
            choise = random.choice(items_epic+items_legendary)
            item = Item(self.x, self.y, 15, choise.colour, choise.description, choise.icon, choise.rarity, choise.name, choise.stackable[0], choise.stackable[1])
            room.items.append(item)
        return room.items

    def rotate(self, degrees):
        if len(self.points)>0:
            radians = degrees*math.pi/180
            matrix = [(math.cos(radians),-1*math.sin(radians)), (math.sin(radians),math.cos(radians))]
            for i in range(0, len(self.points)):
                point = self.points[i]
                point_x = self.x + matrix[0][0]*(self.x-point[0]) + matrix[0][1]*(self.y-point[1])
                point_y = self.y + matrix[1][0]*(self.x-point[0]) + matrix[1][1]*(self.y-point[1])
                self.points[i] = (point_x,point_y)

    def shooting(self, p, bullets):
        pass

##### MELEE ENEMY
class Enemy_melee(Enemy):
    def __init__(self, x, y, width, colour, damage, collision_damage, hp, vel, element, fire_effect, ice_effect, poison_effect, void_effect, duration):
        Enemy.__init__(self, x, y, width, colour, damage, collision_damage, hp, vel, element, fire_effect, ice_effect, poison_effect, void_effect, duration)
        self.hp = hp
        self.vel = vel
        self.max_vel = vel
        self.type = "melee"
        self.max_hp = hp
        self.size = "small"
        self.points = []

        self.damage = damage
        self.collision_damage = collision_damage

        self.element = element
        self.effect_fire = fire_effect
        self.effect_ice = ice_effect
        self.effect_poison = poison_effect
        self.effect_void = void_effect
        self.duration = duration
        
    def draw_enemy(self, screen):
        pygame.draw.circle(screen, (self.colour), ([self.x, self.y]), self.width)

##### RANGED ENEMY
class Enemy_ranged(Enemy):
    def __init__(self, x, y, width, colour, damage, collision_damage, hp, vel, shoot_delay, element, fire_effect, ice_effect, poison_effect, void_effect, duration, bullet_size, explosive_bullet_size, bullet_vel):
        Enemy.__init__(self, x, y, width, colour, damage, collision_damage, hp, vel, element, fire_effect, ice_effect, poison_effect, void_effect, duration)
        self.x = x
        self.y = y
        self.width = width
        self.draw_helper_y = -math.sin(math.pi/6)*self.width
        self.draw_helper_x = -math.cos(math.pi/6)*self.width
        self.points = [(self.x, self.y-self.width), (self.x + self.draw_helper_x, self.y-self.draw_helper_y), (self.x-self.draw_helper_x, self.y-self.draw_helper_y)]
        self.colour = colour
        self.hp = hp
        self.max_hp = hp
        self.vel = vel
        self.max_vel = vel
        self.type = "ranged"
        self.size = "small"
        
        self.collision_damage = collision_damage
        self.damage = damage

        self.element = element
        self.effect_fire = fire_effect
        self.effect_ice = ice_effect
        self.effect_poison = poison_effect
        self.effect_void = void_effect
        self.duration = duration

        self.shoot_delay = shoot_delay
        self.max_shoot_delay = shoot_delay
        self.can_shoot = False
        self.bounces = 0
        self.bullet_size = bullet_size
        self.explosive_bullet_size = explosive_bullet_size
        self.bullet_vel = bullet_vel

    def movement(self, screen, player):
        screen_size = [screen.get_width(), screen.get_height()]
        self.points = [(self.x, self.y-self.width), (self.x + self.draw_helper_x, self.y-self.draw_helper_y), (self.x-self.draw_helper_x, self.y-self.draw_helper_y)]
        distance_player = math.sqrt((player.x - self.x)**2 + (player.y - self.y)**2)
        max_distance = 300
        speed = normalise_distance(self.x, self.y, player.x, player.y, self.vel)
        if distance_player < max_distance - 20:
            if player.x > self.x:
                if player.y > self.y:
                    speed = normalise_distance(player.x, player.y, self.x, self.y, self.vel)
                    self.x -= speed[0]
                    self.y -= speed[1]
                elif player.y < self.y:
                    speed = normalise_distance(player.x, player.y, self.x, self.y, self.vel)
                    self.x -= speed[0]
                    self.y -= speed[1]
            elif player.x < self.x:
                if player.y > self.y:
                    speed = normalise_distance(player.x, player.y, self.x, self.y, self.vel)
                    self.x -= speed[0]
                    self.y -= speed[1]
                elif player.y < self.y:
                    speed = normalise_distance(player.x, player.y, self.x, self.y, self.vel)
                    self.x -= speed[0]
                    self.y -= speed[1]
        elif distance_player > max_distance + 20:
            if player.x > self.x:
                if player.y > self.y:
                    speed = normalise_distance(player.x, player.y, self.x, self.y, self.vel)
                    self.x += speed[0]
                    self.y += speed[1]
                elif player.y < self.y:
                    speed = normalise_distance(player.x, player.y, self.x, self.y, self.vel)
                    self.x += speed[0]
                    self.y += speed[1]
            elif player.x < self.x:
                if player.y > self.y:
                    speed = normalise_distance(player.x, player.y, self.x, self.y, self.vel)
                    self.x += speed[0]
                    self.y += speed[1]
                elif player.y < self.y:
                    speed = normalise_distance(player.x, player.y, self.x, self.y, self.vel)
                    self.x += speed[0]
                    self.y += speed[1]

    def draw_enemy(self, screen):
        pygame.draw.polygon(screen, (self.colour), (self.points))

    def shooting(self, p, bullets):
        if self.can_shoot == False:
            self.shoot_delay -= 0.02
            # CHECK IF SHOOT DELAY FOR RANGED ENEMIES IS 0 
            if self.shoot_delay <= 0:
                self.can_shoot = True
        if self.can_shoot == True:
            # CALCULATE DIRECTION OF BULLET TOWARDS THE PLAYER FROM THE ENEMY
            direction = normalise_distance(p.x + p.width/2, p.y + p.height/2, self.x, self.y, self.bullet_vel)
            bullet_enemy = Projectile_bullet(self.x, self.y, direction[0], direction[1], self.colour, self.bounces, self, self.bullet_size, self.explosive_bullet_size)
            bullets.append(bullet_enemy)                
            self.shoot_delay = self.max_shoot_delay
            self.can_shoot = False

##### BONUS ENEMY
class Enemy_bonus(Enemy):
    def __init__(self, x, y, width, colour, damage, collision_damage, hp, vel, element, fire_effect, ice_effect, poison_effect, void_effect, duration):
        Enemy.__init__(self, x, y, width, colour, damage, collision_damage, hp, vel, element, fire_effect, ice_effect, poison_effect, void_effect, duration)
        self.colour = yellow
        self.direction_x = 1
        self.direction_y = 1
        self.vel = vel
        self.max_vel = vel
        self.hp = hp
        self.type = "bonus"
        self.max_hp = hp
        self.size = "small"
        self.points = []

        self.damage = damage
        self.collision_damage = collision_damage
        
        self.element = element
        self.effect_fire = fire_effect
        self.effect_ice = ice_effect
        self.effect_poison = poison_effect
        self.effect_void = void_effect
        self.duration = duration

    def movement(self, screen, player):
        screen_size = [screen.get_width(), screen.get_height()]
        if self.x <= 0:
            self.direction_x = 1
        elif self.x > screen_size[0]:
            self.direction_x = -1

        if self.y <= 0:
            self.direction_y = 1
        elif self.y > screen_size[1]:
            self.direction_y = -1

        self.dir_x = random.randint(0, 50)/10
        self.dir_y = random.randint(0, 50)/10
        speed = normalise_speed(self.dir_x, self.dir_y, self.vel)
        speed[0] = speed[0] * self.direction_x

        if self.direction_y == 0:
            choices = [-1, 1]
            choice = random.choice(choices)
            speed[1] = speed[1] * choice
        else:
            speed[1] = speed[1] * self.direction_y

        self.x += speed[0]
        self.y += speed[1]

    def draw_enemy(self, screen):
        pygame.draw.circle(screen, (self.colour), ([self.x, self.y]), self.width)

##### ENEMY BOSS
class Enemy_boss(Enemy):
    def __init__(self, x, y, width, colour, damage, collision_damage, hp, vel, shoot_delay, element, fire_effect, ice_effect, poison_effect, void_effect, duration, bullet_size, explosive_bullet_size, bullet_vel):
        Enemy.__init__(self, x, y, width, colour, damage, collision_damage, hp, vel, element, fire_effect, ice_effect, poison_effect, void_effect, duration)
        self.x = x
        self.y = y
        self.width = width
        self.draw_helper = math.sqrt(math.pow(self.width,2)/2)
        self.points = [(self.x-self.width, self.y), (self.x-self.draw_helper, self.y-self.draw_helper), (self.x, self.y-self.width), (self.x+self.draw_helper, self.y-self.draw_helper), (self.x+self.width, self.y), (self.x+self.draw_helper, self.y+self.draw_helper), (self.x, self.y+self.width), (self.x-self.draw_helper, self.y+self.draw_helper)]
        self.colour = colour
        self.hp = hp
        self.max_hp
        self.vel = vel
        self.max_vel = vel
        self.type = "boss"
        self.size = "big"

        self.shoot_delay = shoot_delay
        self.max_shoot_delay = shoot_delay
        self.can_shoot = False
        self.bounces = 0
        self.bullet_size = bullet_size
        self.explosive_bullet_size = explosive_bullet_size
        self.bullet_vel = bullet_vel

        self.damage = damage
        self.collision_damage = collision_damage
        
        self.element = element
        self.effect_fire = fire_effect
        self.effect_ice = ice_effect
        self.effect_poison = poison_effect
        self.effect_void = void_effect
        self.duration = duration

    def change_colour(self, colour):
        self.colour = colour

    def check_health_percentage(self):
        if self.hp > self.max_hp*0.75 and self.hp <= self.max_hp:
            self.change_colour(orange)
        elif self.hp <= self.max_hp*0.75 and self.hp > self.max_hp*0.5:
            self.change_colour(blue)
        elif self.hp <= self.max_hp*0.5 and self.hp > self.max_hp*0.25:
            self.change_colour(green_dark)
        elif self.hp <= self.max_hp*0.25 and self.hp > 0:
            self.change_colour(red)

    def draw_enemy(self, screen):
        pygame.draw.polygon(screen, (self.colour), self.points)

    def shooting(self, p, bullets):
        if self.can_shoot == False:
            self.shoot_delay -= 0.02
            # CHECK IF SHOOT DELAY FOR RANGED ENEMIES IS 0 
            if self.shoot_delay <= 0:
                self.can_shoot = True
        if self.can_shoot == True:
            # CALCULATE DIRECTION IN RELATION TO ITS POSIIONT AND CORNERS
            for i in range(len(self.points)):
                direction = normalise_distance(self.x, self.y, self.points[i][0], self.points[i][1], self.bullet_vel)
                bullet_enemy = Projectile_bullet(self.x, self.y, direction[0], direction[1], self.colour, self.bounces, self, self.bullet_size, self.explosive_bullet_size)
                bullets.append(bullet_enemy)                
                self.shoot_delay = self.max_shoot_delay
                self.can_shoot = False
