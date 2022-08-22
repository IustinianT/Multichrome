from UtilityFunctions import *

# ITEMS
class Item():
    def __init__(self, x, y, width, colour, description, icon, rarity, name, stackable, max_items):
        self.x = x
        self.y = y
        self.width = width
        self.colour = colour
        self.description = description
        self.icon = icon
        self.rarity = rarity
        self.name = name
        self.amount = 1
        self.stackable = [stackable,max_items]

    def create_item(self, screen):
        pygame.draw.circle(screen, (self.colour), (self.x, self.y), self.width)

    def display_icon(self, screen, x, y):
        screen.blit(self.icon,(x, y))

    def set_colour(self):
        if self.rarity == "common":
            self.colour = green_item
        elif self.rarity == "rare":
            self.colour = blue_item
        elif self.rarity == "epic":
            self.colour = purple_item
        elif self.rarity == "legendary":
            self.colour = yellow

    def apply_effect(self, player, player_stats, weapon, weapon_stats, c, companion):
        if self.name == "rubber_bullet":
            max_bounce = self.stackable[1]
            if self.amount < max_bounce:
                weapon.bounces = 1*(self.amount)
            else:
                weapon.bounces = max_bounce
        elif self.name == "light_ammo":
            weapon.max_shoot_delay = 10/(3*self.amount+10)
        elif self.name == "fortified_body":
            percent_hp = player.hp/player.max_hp
            player.max_hp = player_stats["hp"] + 8*self.amount
            player.hp = player.max_hp*percent_hp
            player.collision_damage = player_stats["collision_damage"] + 10*self.amount
            player.fortified[0] = True
            player.fortified[1] = 5*self.amount
        elif self.name == "calculated_rage" and player.rage[0] == False and player.rage[3] <= 0:
            # rage: enraged_status; duration; damage_increase; cooldown; delay_multiplier; max_cooldown
            player.rage[0] = True
            player.rage[1] = 5
            player.rage[2] = self.amount/2
            player.rage[4] = 1/math.log(0.35*self.amount+3, math.e)
            player.rage[5] = 15
            player.rage[3] = player.rage[5]
        elif self.name == "stronger_form":
            percent_hp = player.hp/player.max_hp
            player.max_hp = player_stats["hp"] + 3*self.amount
            player.hp = player.max_hp*percent_hp
        elif self.name == "higher_power":
            weapon.bullet_damage = weapon.max_bullet_damage + 2*self.amount
            weapon.explosive_damage = weapon.max_explosive_damage + 1.2*self.amount
            weapon.laser_damage = weapon.max_laser_damage + 2.4*self.amount
            weapon.bullet_size = weapon.max_bullet_size + 0.2*self.amount
            weapon.explosive_bullet_size = weapon.max_explosive_bullet_size + 0.2*self.amount
            weapon.laser_size = weapon.max_laser_size + 5*self.amount
        elif self.name == "dethroning_shiv":
            weapon.extra_damage_boss = 4*self.amount
        elif self.name == "hot_mag":
            player.can_change_fire = True
            weapon.effect_fire = weapon_stats["fire_effect"]+weapon_stats["fire_effect_growth"]*self.amount
        elif self.name == "crippling_shot":
            player.can_change_ice = True
            weapon.effect_ice = weapon_stats["ice_effect"]*math.pow(weapon_stats["ice_effect_growth"],self.amount)
        elif self.name == "poisoned_bullets":
            player.can_change_poison = True
            weapon.effect_poison = weapon_stats["poison_effect"]*math.pow(weapon_stats["poison_effect_growth"],self.amount)
        elif self.name == "prepared" and player.prepared[1]<=0:
            player.prepared[0] = True
            player.prepared[2] = 15*math.pow(0.95,self.amount)
            player.prepared[3] = True
        elif self.name == "worthy_companion":
            c.exists = True
            c.max_shoot_delay = 10/(3*self.amount+10)
        elif self.name == "blood_thirst":
            max_lifesteal = self.stackable[1]/100
            if 0.01*self.amount < max_lifesteal:
                player.blood_thirst = 0.01*self.amount
            else:
                player.blood_thirst = max_lifesteal
        elif self.name == "multishot":
            max_multishot = self.stackable[1]
            if self.amount < max_multishot:
                weapon.multishot = self.amount
            elif self.amount >= max_multishot:
                weapon.multishot = max_multishot
        elif self.name == "hunter_instincts" and player.rage_hunter[5]==0:
            # rage_hunter: enraged_status; duration; movement_speed_increase; dummy_value; delay_multiplier; max_duration
            player.rage_hunter[0] = True
            player.rage_hunter[1] = player.rage_hunter[5]
            player.rage_hunter[2] = math.log(self.amount+1, math.e)
            player.rage_hunter[3] = 0
            player.rage_hunter[4] = 1/math.log(0.25*self.amount+3, math.e)
            player.rage_hunter[5] = 3+0.2*(self.amount-1)
        elif self.name == "speed_stimulant":
            player.vel = player.max_vel+math.log(2*self.amount+1,math.e)
        elif player.can_change_explosive == False and self.name == "explosive_rounds":
            player.can_change_explosive = True
        elif player.can_change_laser == False and self.name == "laser_shot":
            player.can_change_laser = True
