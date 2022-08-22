from UtilityFunctions import *
from Player import *
from Effects import *

##### PROJECTILE
class Projectile():
    def __init__(self, x, y, speed_x, speed_y, colour, bounces, shot_by, bullet_size, explosive_bullet_size):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.colour = colour
        self.type = "defeault_projectile"
        self.width = bullet_size
        self.bounces = bounces
        self.shot_by = shot_by
        self.linger = 0

    def travel(self, screen, bullets):
        screen_x = screen.get_width()
        screen_y = screen.get_height()
        self.x += self.speed_x
        self.y += self.speed_y
        if self.x > screen_x or self.x < 0:
            if self.bounces <= 0:
                bullets.remove(self)
            else:
                self.speed_x *= -1
                self.bounces -= 1
        elif self.y > screen_y or self.y < 0:
            if self.bounces <= 0:
                bullets.remove(self)
            else:
                self.speed_y *= -1
                self.bounces -= 1

    def collided_bullet(self, bullets, enemy, weapon, player, operator, explosions, companion, screen):
        pass

    def apply_debuff(self, p, enemy, weapon):
        if self.colour != enemy.colour:
            if self.colour == red:
                enemy.debuff_fire = [True, weapon.effect_fire, weapon.duration]
            if self.colour == blue:
                enemy.debuff_ice = [True, weapon.effect_ice, weapon.duration]
            if self.colour == green_dark:
                enemy.debuff_poison = [True, weapon.effect_poison, weapon.duration]
        if enemy.colour == purple:
            p.debuff_void = [False,0]

    def deal_damage(self, enemy, p, weapon):
        if weapon.type == "explosive":
            if enemy.type == "boss":
                enemy.hp -= (weapon.explosive_damage/4+weapon.extra_damage_boss)
                p.lifesteal_boss(self, weapon, weapon.explosive_damage/4+weapon.extra_damage_boss)
            else:
                enemy.hp -= weapon.explosive_damage/4
                p.lifesteal_enemy(self, weapon, weapon.explosive_damage/4)
        elif weapon.type == "bullet":
            if enemy.type == "boss":
                enemy.hp -= (weapon.bullet_damage+weapon.extra_damage_boss)
                p.lifesteal_boss(self, weapon, weapon.bullet_damage+weapon.extra_damage_boss)
            else:
                enemy.hp -= weapon.bullet_damage
                p.lifesteal_enemy(self, weapon, weapon.bullet_damage)
        elif weapon.type == "laser":
            if enemy.type == "boss":
                enemy.hp -= (weapon.laser_damage+weapon.extra_damage_boss)
                p.lifesteal_boss(self, weapon, weapon.laser_damage+weapon.extra_damage_boss)
            else:
                enemy.hp -= weapon.laser_damage
                p.lifesteal_enemy(self, weapon, weapon.laser_damage)

    def create_bullet(self, screen):
        pygame.draw.circle(screen, (self.colour), (self.x, self.y), self.width)

class Projectile_bullet(Projectile):
    def __init__(self, x, y, speed_x, speed_y, colour, bounces, shot_by, bullet_size, explosive_bullet_size):
        Projectile.__init__(self, x, y, speed_x, speed_y, colour, bounces, shot_by, bullet_size, explosive_bullet_size)
        self.width = bullet_size
        self.type = "bullet"

    def collided_bullet(self, bullets, enemy, weapon, player, operator, explosion, companion, screen):
        distance = distance_hypotenuse(enemy.x, enemy.y, self.x, self.y)
        if distance - self.width - enemy.width <= 0:
            self.deal_damage(enemy, player, weapon)
            bullets.remove(self)
            self.apply_debuff(player, enemy, weapon)

class Projectile_explosive(Projectile):
    def __init__(self, x, y, speed_x, speed_y, colour, bounces, shot_by, bullet_size, explosive_bullet_size):
        Projectile.__init__(self, x, y, speed_x, speed_y, colour, bounces, shot_by, bullet_size, explosive_bullet_size)
        self.width = explosive_bullet_size
        self.width_explosion = 220
        self.linger = 0.6
        self.type = "explosive"

    def collided_bullet(self, bullets, enemy, weapon, player, operator, explosions, companion, screen):
        distance = distance_hypotenuse(enemy.x, enemy.y, self.x, self.y)
        if distance - self.width - enemy.width <= 0:
            self.deal_damage(enemy, player, weapon)
            explosion = Explosion(self.x, self.y, self.width_explosion, self.colour, self.linger)
            explosion.create_explosion(screen)
            explosions.append(explosion)
            bullets.remove(self)
            self.apply_debuff(player,enemy,weapon)

            for e in operator.enemies:
                distance_explosion = distance_hypotenuse(e.x, e.y, self.x, self.y)
                if distance_explosion - self.width_explosion - e.width <= 0:
                    e.hp -= weapon.explosive_damage
                    self.apply_debuff(player, e, weapon)

class Projectile_laser(Projectile):
    def __init__(self, x, y, mouse_x, mouse_y, colour, bounces, width, shot_by, screen, bullet_size, explosive_bullet_size):
        Projectile.__init__(self, x, y, mouse_x, mouse_y, colour, bounces, shot_by, bullet_size, explosive_bullet_size)
        self.x = x
        self.y = y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.colour = colour
        self.type = "laser"
        self.width = width
        self.linger_max = 0.6
        self.linger = 0.6
        self.laser_width = screen.get_width()*1.5
        self.new_points = [[self.x,self.y], [self.x+self.laser_width,self.y-self.width], [self.x+self.laser_width,self.y+self.width]]
        self.points = [[self.x,self.y], [self.x+self.laser_width,self.y-self.width], [self.x+self.laser_width,self.y+self.width]]
        self.can_damage = True
        self.enemy_coordinates = []
        self.damaged_enemies = []

    def create_bullet(self, screen):
        temp_colour = []
        for i in range(len(self.colour)):
            temp_colour.append(self.colour[i])
      
        self.new_points = self.get_new_points()

        for i in range(len(self.colour)):
            temp_colour[i] *= self.linger
        pygame.draw.polygon(screen, temp_colour, self.new_points)

    def travel(self):
        pass

    def get_new_points(self):
        x = normalise_distance(self.mouse_x, self.mouse_y, self.x, self.y, 1)[0]
        y = normalise_distance(self.mouse_x, self.mouse_y, self.x, self.y, 1)[1]

        direction = 1
        if self.mouse_x - self.x <=0:
            direction = 0
        try:
            radians = math.atan(y/x)+(math.pi*direction)
        except:
            print(f"Division by 0! Y={y} X={x}")
            radians = math.pi

        matrix = [(math.cos(radians),-1*math.sin(radians)), (math.sin(radians),math.cos(radians))]
        for i in range(len(self.points)):
            point = self.points[i]
            point_x = self.x + matrix[0][0]*(self.x-point[0]) + matrix[0][1]*(self.y-point[1])
            point_y = self.y + matrix[1][0]*(self.x-point[0]) + matrix[1][1]*(self.y-point[1])
            point = [point_x,point_y]
            self.new_points[i] = point
        return self.new_points

    def collided_bullet(self, bullets, enemy, weapon, player, operator, explosions, companion, screen):
        # TEST IF THE CENTRE OF THE ENEMY IS INSIDE THE TRIANGLE        
        self.new_points = self.get_new_points()
        self_to_mouse = [self.mouse_x-self.x, self.mouse_y-self.y]
        self_to_corner = [self.new_points[1][0]-self.x, self.new_points[1][1]-self.y]
           
        magnitude = (math.sqrt(math.pow(self_to_mouse[0],2)+math.pow(self_to_mouse[1],2)))*(math.sqrt(math.pow(self_to_corner[0],2)+math.pow(self_to_corner[1],2)))
        max_angle = math.acos(dot_product(self_to_mouse,self_to_corner)/magnitude)

        self_to_enemy = [enemy.x-self.x, enemy.y-self.y]
        magnitude2 = (math.sqrt(math.pow(self_to_mouse[0],2)+math.pow(self_to_mouse[1],2)))*(math.sqrt(math.pow(self_to_enemy[0],2)+math.pow(self_to_enemy[1],2)))
        dot = dot_product(self_to_mouse,self_to_enemy)
        if dot > magnitude2:
            angle_enemy_to_mid = 0
        else:
            angle_enemy_to_mid = math.acos(dot/magnitude2)

        distance_of_enemy = math.sqrt(math.pow((self.x-enemy.x),2)+math.pow((self.y-enemy.y),2))
        if angle_enemy_to_mid <= max_angle and distance_of_enemy <= self.laser_width and enemy not in self.damaged_enemies:
            self.deal_damage(enemy, player, weapon)
            self.apply_debuff(player,enemy,weapon)
            self.damaged_enemies.append(enemy)
