from Enemies import *
from UtilityFunctions import *

# OPERATOR
class Operator:
    def __init__(self, limit_enemies, max_enemies, total_max_enemies_increase, spawn_radius):
        self.limit_enemies = limit_enemies
        self.total_max_enemies = max_enemies
        self.room_max_enemies = max_enemies
        self.current_enemies = 0
        self.enemies = []
        self.total_max_enemies_increase = total_max_enemies_increase
        self.spawn_radius = spawn_radius
        self.bosses_on_screen = 0
        self.can_spawn_boss = True

    def spawn_enemies(self, screen, player, enemy_melee, enemy_ranged, enemy_bonus, elements, elements_list, stage):
        # spawn enemy randomly, but far from player
        screen_x = screen.get_width()
        screen_y = screen.get_height()
        for i in range(0, self.room_max_enemies):
            ## DECIDE THE ELEMENT OF THE ENEMY
            colour_int = random.randint(0,10000)
            if colour_int >= 0 and colour_int <= 8050:
                random_colour = orange
            elif colour_int >= 8051 and colour_int <= 8550:
                random_colour = blue
            elif colour_int >= 8551 and colour_int <= 9050:
                random_colour = green_dark
            elif colour_int >= 9051 and colour_int <= 9550:
                random_colour = red
            elif colour_int >= 9551 and colour_int <= 10000:
                random_colour = purple

            random_x = random.randint(0, screen_x)
            random_y = random.randint(0, screen_y)
            can_spawn = True
            random_spawn_decider = random.randint(0,10000)
            while distance_hypotenuse(random_x, random_y, player.x, player.y) >= self.spawn_radius and can_spawn == True:
                if random_spawn_decider >= 0 and random_spawn_decider <= 5550:
                    enemy = Enemy_melee(random_x, random_y, enemy_melee["width"], random_colour, enemy_melee["damage"]+enemy_melee["damage_growth"]*(stage-1), enemy_melee["collision_damage"], enemy_melee["hp"]*math.pow(enemy_melee["hp_growth"],(stage-1)), enemy_melee["vel"]*math.pow(enemy_melee["vel_growth"],(stage-1)), enemy_melee["element"], enemy_melee["fire_effect"]+enemy_melee["fire_effect_growth"]*(stage-1), enemy_melee["ice_effect"]*math.pow(enemy_melee["ice_effect_growth"],(stage-1)), enemy_melee["poison_effect"]*math.pow(enemy_melee["poison_effect_growth"],(stage-1)), enemy_melee["void_effect"], enemy_melee["duration"])
                    self.enemies.append(enemy)
                    can_spawn = False
                elif random_spawn_decider >= 5551 and random_spawn_decider <= 9900:
                    enemy = Enemy_ranged(random_x, random_y, enemy_ranged["width"], random_colour, enemy_ranged["damage"]+enemy_ranged["damage_growth"]*(stage-1), enemy_ranged["collision_damage"], enemy_ranged["hp"]*math.pow(enemy_ranged["hp_growth"],(stage-1)), enemy_ranged["vel"]*math.pow(enemy_ranged["vel_growth"],(stage-1)), enemy_ranged["shoot_delay"]*math.pow(enemy_ranged["shoot_delay_growth"],(stage-1)), enemy_ranged["element"], enemy_ranged["fire_effect"]+enemy_ranged["fire_effect_growth"]*(stage-1), enemy_ranged["ice_effect"]*math.pow(enemy_ranged["ice_effect_growth"],(stage-1)), enemy_ranged["poison_effect"]*math.pow(enemy_ranged["poison_effect_growth"],(stage-1)), enemy_ranged["void_effect"], enemy_ranged["duration"], enemy_ranged["bullet_size"], enemy_ranged["explosive_bullet_size"], enemy_ranged["bullet_vel"])
                    self.enemies.append(enemy)
                    can_spawn = False
                elif random_spawn_decider >= 9901:
                    enemy = Enemy_bonus(random_x, random_y, enemy_ranged["width"], yellow, enemy_bonus["damage"]+enemy_bonus["damage_growth"], enemy_bonus["collision_damage"], enemy_bonus["hp"]*math.pow(enemy_bonus["hp_growth"],(stage-1)), enemy_bonus["vel"]*math.pow(enemy_bonus["vel_growth"],(stage-1)), enemy_bonus["element"], enemy_bonus["fire_effect"]+enemy_bonus["fire_effect_growth"]*(stage-1), enemy_bonus["ice_effect"]*math.pow(enemy_bonus["ice_effect_growth"],(stage-1)), enemy_bonus["poison_effect"]*math.pow(enemy_bonus["poison_effect_growth"],(stage-1)), enemy_bonus["void_effect"], enemy_bonus["duration"])
                    self.enemies.append(enemy)
                    can_spawn = False

    def spawn_boss(self, screen, enemy_boss, stage, player):
        end = False
        while end == False:
            random_x = random.randint(0, screen.get_width())
            random_y = random.randint(0, screen.get_height())
            distance_from_player = math.sqrt(math.pow(player.x-random_x,2)+math.pow(player.y-random_y,2))
            if distance_from_player > screen.get_width()/2:
                self.enemies.append(Enemy_boss(random_x,random_y, enemy_boss["width"], white, enemy_boss["damage"]+enemy_boss["damage_growth"]*(stage-1), enemy_boss["collision_damage"], enemy_boss["hp"]*math.pow(enemy_boss["hp_growth"],(stage-1)), enemy_boss["vel"]*math.pow(enemy_boss["vel_growth"],(stage-1)), enemy_boss["shoot_delay"]*math.pow(enemy_boss["shoot_delay_growth"],(stage-1)), enemy_boss["element"], enemy_boss["fire_effect"]+enemy_boss["fire_effect_growth"]*(stage-1), enemy_boss["ice_effect"]*math.pow(enemy_boss["ice_effect_growth"],(stage-1)), enemy_boss["poison_effect"]*math.pow(enemy_boss["poison_effect_growth"],(stage-1)), enemy_boss["void_effect"], enemy_boss["duration"], enemy_boss["bullet_size"], enemy_boss["explosive_bullet_size"], enemy_boss["bullet_vel"]))
                end = True
        self.can_spawn_boss = False

    def reset(self):
        self.enemies = []
        if self.total_max_enemies < self.limit_enemies:
            self.total_max_enemies += self.total_max_enemies_increase
        self.room_max_enemies = self.total_max_enemies

    def check_bosses(self):
        temp_bosses = 0
        for enemy in self.enemies:
            if enemy.type == "boss":
                temp_bosses += 1
        self.bosses_on_screen = temp_bosses

    def save_info(self):
        with open("SAVE_OPERATOR.txt","w") as info_operator:
            info_operator.write(f"{self.total_max_enemies};{self.room_max_enemies};{self.can_spawn_boss};\n")
        print("SAVED OPERATOR INFO")

    def load_info(self):
        with open("SAVE_OPERATOR.txt","r") as info_operator:
            for line in info_operator:
                temp_info = line.split(";")
                self.total_max_enemies = int(temp_info[0])
                self.room_max_enemies = int(temp_info[1])
                if temp_info[2].lower() == "true":
                    self.can_spawn_boss = True
                elif temp_info[2].lower() == "false":
                    self.can_spawn_boss = False
        print("LOADED OPERATOR INFO")
