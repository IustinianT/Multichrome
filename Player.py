from UtilityFunctions import *
from Projectile import *
from Effects import *
from Items import *
from Healthbar import *

##### PLAYER
class Player():
    def __init__(self, x, y, vel, hp, collision_damage, width, element, colour):
        self.max_vel = vel
        self.vel = vel
        self.width = width
        self.height = width
        self.x = x
        self.y = y
        self.colour = colour
        self.start_hp = hp
        self.max_hp = hp
        self.hp = hp
        self.type = "player"
        
        self.max_collision_damage = collision_damage
        self.collision_damage = collision_damage

        self.element = element
        self.can_change_fire = False
        self.can_change_ice = False
        self.can_change_poison = False
        self.debuff_fire = [False,0,-1]
        self.debuff_ice = [False,1,-1]
        self.debuff_poison = [False,0,-1]
        self.debuff_void = [False,-1]
        self.debuffs = set()

        self.can_change_explosive = False
        self.can_change_bullet = True
        self.can_change_laser = False

        self.items = []
        self.scrap_items = []
        self.fortified = [False,5]
        # rage: enraged_status; duration; damage_increase; cooldown; delay_multiplier; max_cooldown
        self.rage = [False,0,0,0,0,0]
        # rage_hunter: enraged_status; duration; movement_speed_increase; dummy_value; delay_multiplier; max_duration
        self.rage_hunter = [False,0,0,0,0,0]
        self.prepared = [False,0,5,True]
        self.blood_thirst = 0

        self.coins = 0
        # can/can't buy, cooldown
        self.can_interact = [True,2]

    ##### DRAW PLAYER
    def draw_player(self, screen):
        pygame.draw.rect(screen, (self.colour), (self.x, self.y, self.width, self.height))

    ##### PLAYER MOVEMENT
    def movement_and_inputs(self):
        keys = pygame.key.get_pressed()
        diagonal_vel = math.sqrt(math.pow(self.vel,2)/2)
        ##### INPUTS
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.y -= diagonal_vel
                self.x -= diagonal_vel
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.y += diagonal_vel
                self.x -= diagonal_vel
            else:
                self.x -= self.vel
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.y -= diagonal_vel
                self.x += diagonal_vel
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.y += diagonal_vel
                self.x += diagonal_vel
            else:
                self.x += self.vel
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.y -= diagonal_vel
                self.x -= diagonal_vel
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.y -= diagonal_vel
                self.x += diagonal_vel
            else:
                self.y -= self.vel
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.y += diagonal_vel
                self.x -= diagonal_vel
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.y += diagonal_vel
                self.x += diagonal_vel
            else:
                self.y += self.vel

    def lock_movement(self, screen):
        screen_x = screen.get_width()
        screen_y = screen.get_height()
        if self.x + self.width >= screen_x:
            self.x = screen_x - self.width -1 
        if self.x <= 0:
            self.x = 1
        if self.y + self.height >= screen_y:
            self.y = screen_y - self.height -1
        if self.y <= 0:
            self.y = 1

    def collided_enemy(self, enemy, healthbar):
        distance = distance_hypotenuse(self.x + self.width/2, self.y + self.height/2, enemy.x, enemy.y)
        if distance - enemy.width - self.width/2 <= 0:
            enemy.hp -= self.collision_damage
            self.hp -= enemy.collision_damage
            if self.colour != enemy.colour:
                if self.prepared[0] == True:
                    self.prepared[0] = False
                    self.prepared[1] = self.prepared[2]
                else:
                    if enemy.colour == red:
                        self.debuff_fire = [True, enemy.effect_fire, enemy.duration]
                        self.debuffs.add("fire")
                    if enemy.colour == blue:
                        self.debuff_ice = [True, enemy.effect_ice, enemy.duration]
                        self.debuffs.add("ice")
                    if enemy.colour == green_dark:
                        self.debuff_poison = [True, enemy.effect_poison, enemy.duration]
                        self.debuffs.add("poison")
                    if enemy.colour == purple:
                        self.debuff_void = [True, enemy.effect_void]
                        self.debuffs.add("void")

    def collided_bullet(self, bullet, bullets, healthbar, enemy_ranged, enemy_boss):
        distance = distance_hypotenuse(bullet.x, bullet.y, self.x + self.width/2, self.y + self.width/2)
        if distance - bullet.width - self.width/2 <= 0:
            enemy = bullet.shot_by
            self.hp -= enemy.damage
            if self.colour != bullet.colour:
                if self.prepared[0] == True:
                    self.prepared[0] = False
                    self.prepared[1] = self.prepared[2]
                else:
                    if bullet.colour == red:
                        self.debuff_fire = [True,enemy.effect_fire, enemy.duration]
                        self.debuffs.add("fire")
                    if bullet.colour == blue:
                        self.debuff_ice = [True,enemy.effect_ice, enemy.duration]
                        self.debuffs.add("ice")
                    if bullet.colour == green_dark:
                        self.debuff_poison = [True,enemy.effect_poison, enemy.duration]
                        self.debuffs.add("poison")
                    if bullet.colour == purple:
                        self.debuff_void = [True,enemy.effect_void, enemy.duration]
                        self.debuffs.add("void")
            bullets.remove(bullet)

    def alive(self):
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        if self.hp <= 0 or (self.debuff_void[1] <= 0 and self.debuff_void[0] == True):
            print("GAME OVER")
            return False
        return True

    def set_element(self, element, elements, weapon):
        self.colour = elements[element]

    def apply_debuff(self):
        if self.check_fire() == True:
            self.hp -= self.debuff_fire[1]
            self.debuff_fire[2] -= 1
        if self.check_poison() == True:
            self.hp *= self.debuff_poison[1]
            self.debuff_poison[2] -= 1
        if self.check_ice() == True:
            self.vel = self.max_vel * self.debuff_ice[1]
            self.debuff_ice[2] -= 1
        if self.check_void() == True:
            self.debuff_void[1] -= 1

    def check_fire(self):
        return self.debuff_fire[0]

    def check_ice(self):
        return self.debuff_ice[0]

    def check_poison(self):
        return self.debuff_poison[0]
    
    def check_void(self):
        return self.debuff_void[0]

    def debuff_expire_check(self):
        if self.debuff_fire[2] <= 0 and self.debuff_fire[2] != -0.02:
            self.debuff_fire[0] = False
            self.debuffs.discard("fire")
        if self.debuff_ice[2] <= 0 and self.debuff_ice[2] != -0.02:
            self.debuff_ice[0] = False
            self.debuffs.discard("ice")
            self.vel = self.max_vel
        if self.debuff_poison[2] <= 0 and self.debuff_poison[2] != -0.02:
            self.debuff_poison[0] = False
            self.debuffs.discard("poison")
        self.check_rage()

    def apply_item_buffs(self, screen, weapon):
        if self.rage[0] == True and self.rage[1]>0:
            weapon.bullet_damage = weapon.max_bullet_damage + 3*self.rage[2]
            weapon.explosive_damage = weapon.max_explosive_damage + 2*self.rage[2]
            weapon.laser_damage = weapon.max_laser_damage + 4*self.rage[2]
            weapon.shoot_delay = weapon.max_shoot_delay*self.rage[4]
            effect = Effect(self.x+self.width/2, self.y+self.width/2, self.width, [255*(self.rage[1]/10),0,0])
            effect.create_effect(screen)

        elif self.rage_hunter[0] == True and self.rage_hunter[1]>0:
            weapon.shoot_delay = weapon.max_shoot_delay*self.rage_hunter[4]
            self.vel = self.max_vel + self.rage_hunter[2]
            effect = Effect(self.x+self.width/2, self.y+self.width/2, self.width, [255*(self.rage_hunter[1]/10),0,0])
            effect.create_effect(screen)

        if self.prepared[1]>0 and self.prepared[0]==False and self.prepared[3]==True:
            self.prepared[1] -= 0.02
            if self.prepared[1] <= 0:
                self.prepared[0] = True

    def shooting(self, screen, w, bullets):
        direction = 1
        clicks = pygame.mouse.get_pressed()
        if pygame.mouse.get_pressed()[0] and w.can_shoot == True:
            pos = pygame.mouse.get_pos()
            if w.type != "laser":
                if w.multishot == 0:
                    ## FIND DISTANCE AND DIRECTION OF SHOT FROM MOUSE
                    bullet_normalised = normalise_distance(pos[0], pos[1], self.x+self.width/2, self.y+self.height/2, 10)
                    bullet_pos_x = self.x + self.width/2 + bullet_normalised[0]
                    bullet_pos_y = self.y + self.height/2 + bullet_normalised[1]
                    speed_x = bullet_normalised[0]
                    speed_y = bullet_normalised[1]
                    if w.type == "bullet":
                        projectile = Projectile_bullet(bullet_pos_x, bullet_pos_y, speed_x, speed_y, self.colour, w.bounces, self, w.bullet_size, w.explosive_bullet_size)
                    if w.type == "explosive":
                        projectile = Projectile_explosive(bullet_pos_x, bullet_pos_y, speed_x, speed_y, self.colour, w.bounces, self, w.bullet_size, w.explosive_bullet_size)
                    bullets.append(projectile)                
                elif w.multishot >= 1:
                    if pos[0] - (self.x+self.width/2) >= 0:
                        direction = 1
                    else: 
                        direction = -1
                    for i in range(-1*w.multishot,w.multishot+1,2):
                        degrees = 5
                        try:
                            angle = math.atan((pos[1]-(self.y+self.width/2))/(pos[0]-(self.x+self.width/2)))+(degrees)*(math.pi/180)*i
                        except:
                            print("maths error: small program bug")
                        if angle > math.pi/2:
                            angle = math.pi - angle
                            x = 1*direction*-1
                            y = math.tan(angle)*x*-1
                        elif angle < -math.pi/2:
                            angle = math.pi + angle
                            x = 1*direction*-1
                            y = math.tan(angle)*x
                        else:
                            x = 1*direction
                            y = math.tan(angle)*x
                        bullet_normalised = normalise_distance(self.x+self.width/2+x, self.y+self.width/2+y, self.x+self.width/2, self.y+self.height/2, 10)
                        bullet_pos_x = self.x + self.width/2 + bullet_normalised[0]
                        bullet_pos_y = self.y + self.height/2 + bullet_normalised[1]
                        speed_x = bullet_normalised[0]
                        speed_y = bullet_normalised[1]
                        if w.type == "bullet":
                            projectile = Projectile_bullet(bullet_pos_x, bullet_pos_y, speed_x, speed_y, self.colour, w.bounces, self, w.bullet_size, w.explosive_bullet_size)
                        if w.type == "explosive":
                            projectile = Projectile_explosive(bullet_pos_x, bullet_pos_y, speed_x, speed_y, self.colour, w.bounces, self, w.bullet_size, w.explosive_bullet_size)
                        bullets.append(projectile)
            if w.type == "laser":
                projectile = Projectile_laser(self.x+self.width/2, self.y+self.width/2, pos[0], pos[1], self.colour, w.bounces, w.laser_size, self, screen, w.bullet_size, w.explosive_bullet_size)
                bullets.append(projectile)
            w.start_shot_time = t.time()
            if self.rage[0] == False and self.rage_hunter[0] == False:
                w.shoot_delay = w.max_shoot_delay
            w.can_shoot = False
        ### CHECK IF THE PLAYER SHOOTING DELAY EXPIRED
        if w.can_shoot == False:
            current_shot_time = t.time()
            if current_shot_time - w.start_shot_time >= w.shoot_delay:
                w.can_shoot = True

    def check_rage(self):
        if self.rage[0] == True and self.rage[1]<=0:
            self.rage[0] = False
            self.rage[3] = self.rage[5]
        elif self.rage[0] == True and self.rage[1]>0:
            self.rage[1] -= 0.02
        elif self.rage_hunter[0] == True and self.rage_hunter[1]<=0:
            self.rage_hunter[0] = False
        elif self.rage_hunter[0] == True and self.rage_hunter[1]>0:
            self.rage_hunter[1] -= 0.02
        elif self.rage[0] == False:
            self.rage[3] -= 0.02

    def enrage(self):
        if self.check_item_in_items("hunter_instincts"):
            self.rage_hunter[0] = True
            self.rage_hunter[1] = self.rage_hunter[5]

    def check_item_collision(self, item, room):
        if distance_hypotenuse(self.x+self.width/2, self.y+self.width/2, item.x, item.y) - (self.width+(item.width/2)) <= 0:
            if not self.check_item_in_items(item.name):
                self.items.append(item)
                print(f"added NEW item: {item.name}")
            else:
                self.add_one_to_item_amount(item.name)
            room.items.remove(item)
        
    def add_one_to_item_amount(self, item_name):
        for item in self.items:
            if item.name == item_name:
                item.amount += 1

    def check_item_in_items(self, item_name):
        for player_item in self.items:
            if player_item.name == item_name:
                return True
        return False

    def check_item_in_scrap_items(self, item_name):
        for player_item in self.scrap_items:
            if player_item.name == item_name:
                return True
        return False

    def select_item_in_items(self, item_name):
        for item in self.items:
            if item.name == item_name:
                return item
        return False

    def select_item_in_scrap(self, item_name):
        for item in self.scrap_items:
            if item.name == item_name:
                return item
        return False

    def check_buy_item(self, merchant):
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            for item in merchant.items:
                distance = distance_hypotenuse(pos[0], pos[1], item.x, item.y)
                if distance - item.width <= 0 and self.coins - merchant.prices[f"{item.rarity}"] >= 0 and self.can_interact[0] == True:
                    self.coins -= merchant.prices[f"{item.rarity}"]
                    if self.check_item_in_items(item.name):
                        self.add_one_to_item_amount(item.name)
                    elif self.check_item_in_items(item.name) == False:
                        self.items.append(item)
                    price = merchant.prices[f"{item.rarity}"]
                    print(f"BOUGHT: {item.name} for COINS: {price}")
                    merchant.items.remove(item)
                    self.can_interact[0] = False
                    self.can_interact[1] = 2

    def check_items_to_scrap(self):
        for item in self.items:
            if item.stackable[1] > 0:
                if item.amount > item.stackable[1]:
                    item.amount -= 1
                    print(f"took away: {item.amount}")
                    if self.check_item_in_scrap_items(item.name):
                        scrap_item = self.select_item_in_scrap(item.name)
                        scrap_item.amount += 1
                    elif self.check_item_in_scrap_items(item.name) == False:
                        self.scrap_items.append(Item(250,250,15,item.colour,item.description,item.icon,item.rarity,item.name,item.stackable[0],item.stackable[1]))

    def add_recycled(self, scrap, recycled):
        if scrap.name == recycled.name:
            print(f"Scrap item '{scrap.name}' is worn out.")
        else:
            if self.check_item_in_items(recycled.name):
                self.add_one_to_item_amount(recycled.name)
                print(f"Added 1 to: {recycled.name}")
            elif self.check_item_in_items(recycled.name):
                self.items.append(recycled)
                print(f"Added item: {recycled.name}")

    def recycle(self, items_common, items_rare, items_epic, items_legendary):
        scrap = random.choice(self.scrap_items)
        if scrap.amount == 1:
            remove_item = self.select_item_in_scrap(scrap.name)
            self.scrap_items.remove(remove_item)
        elif scrap.amount > 1:
            take_away_item = self.select_item_in_scrap(scrap.name)
            take_away_item.amount -= 1
        if scrap.rarity == "weapon":
            return
        elif scrap.rarity == "common":
            recycled = random.choice(items_common)
        elif scrap.rarity == "rare":
            recycled = random.choice(items_rare)
        elif scrap.rarity == "epic":
            recycled = random.choice(items_epic)
        elif scrap.rarity == "legendary":
            recycled = random.choice(items_legendary)
        self.add_recycled(scrap,recycled)

    def add_coins(self, enemy, map):
        if enemy.type == "melee":
            self.coins += 1+map.stage
        elif enemy.type == "ranged":
            self.coins += 3+map.stage
        elif enemy.type == "bonus":
            self.coins += 14+map.stage
        elif enemy.type == "boss":
            self.coins += 25+map.stage

    def lifesteal_boss(self, projectile, weapon, damage):
        if self.hp < self.max_hp+self.blood_thirst and projectile.shot_by.type == "player":
            self.hp += (damage+weapon.extra_damage_boss)*self.blood_thirst

    def lifesteal_enemy(self, projectile, weapon, damage):
        if self.hp < self.max_hp+self.blood_thirst and projectile.shot_by.type == "player":
            self.hp += (damage)*self.blood_thirst

    def save_info(self):
        with open("SAVE_SCRAPS.txt","w") as info_scrap:
            for scrap in self.scrap_items:
                info_scrap.write(f"{scrap.name};{scrap.amount};\n")
        with open("SAVE_ITEMS.txt","w") as info_items:
            print(self.items)
            for item in self.items:
                info_items.write(f"{item.name};{item.amount};\n")
        with open("SAVE_PLAYER.txt","w") as info_player:
            info_player.write(f"{self.coins};{self.hp};{self.max_hp};{self.x};{self.y};\n")
        print("SAVED PLAYER INFO")

    def load_info(self, items, items_weapon):
        with open("SAVE_SCRAPS.txt","r") as info_scrap:
            for line in info_scrap:
                temp_info = line.split(";")
                scrap_item = select_item(temp_info[0],items, items_weapon)
                temp_item = Item(scrap_item.x,scrap_item.y,scrap_item.width,scrap_item.colour,scrap_item.description,scrap_item.icon,scrap_item.rarity,scrap_item.name,scrap_item.stackable[0],scrap_item.stackable[1])
                temp_item.amount = int(temp_info[1])
                self.scrap_items.append(temp_item)

        with open("SAVE_ITEMS.txt","r") as info_items:
            for line in info_items:
                temp_info = line.split(";")
                item = select_item(temp_info[0], items, items_weapon)
                print(f"{item.name}")
                temp_item = Item(item.x,item.y,item.width,item.colour,item.description,item.icon,item.rarity,item.name,item.stackable[0],item.stackable[1])
                temp_item.amount = int(temp_info[1])
                self.items.append(temp_item)

        with open("SAVE_PLAYER.txt","r") as info_player:
            for line in info_player:
                temp_info = line.split(";")
                self.coins = float(temp_info[0])
                self.hp = float(temp_info[1])
                self.max_hp = float(temp_info[2])
                self.x = float(temp_info[3])
                self.y = float(temp_info[4])
        print("LOADED PLAYER INFO")
