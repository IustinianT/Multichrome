from UtilityFunctions import *
from Projectile import *

# COMPANION
class Companion():
    ##### COMPANION SPINS AROUND THE POSITION OF THE PLAYER, BLOCKS BULLETS AND ATTACKS WITH THE PLAYER'S WEAPON OCASSIONALLY
    def __init__(self,vel,width,shoot_delay):
        self.x = 0
        self.y = 0
        self.vel = vel
        self.width = width
        self.shoot_delay = shoot_delay
        self.max_shoot_delay = shoot_delay
        self.can_shoot = False
        self.angle = 0
        self.distance = 0
        self.exists = False
        self.type = "companion"

    def create_companion(self, screen, player):
        pygame.draw.circle(screen,(player.colour),(self.x,self.y),self.width)

    def movement(self, player, weapon):
        self.distance = player.width + player.width/4
        speed_x,speed_y = find_direction_speed(self.distance,self.angle)
        self.angle += self.vel
        self.x = player.x+player.width/2+speed_x
        self.y = player.y+player.width/2+speed_y

    def collided_bullet(self, bullet, bullets):
        distance = math.sqrt(math.pow(self.x-bullet.x,2)+math.pow(self.y-bullet.y,2))
        if distance-self.width-bullet.width <= 0 and bullet.shot_by.type != "player" and bullet.shot_by.type != "companion":
            bullets.remove(bullet)

    def shooting(self, screen, o, w, p, enemy, bullets):
        if self.can_shoot == False:
            self.shoot_delay -= 0.02
            # CHECK IF SHOOT DELAY FOR COMPANION IS 0 
            if self.shoot_delay <= 0:
                self.can_shoot = True

        if self.can_shoot == True and len(o.enemies)>0:
            enemy = random.choice(o.enemies)
            bullet_normalised = normalise_distance(enemy.x, enemy.y, self.x, self.y, w.bullet_vel)
            speed_x = bullet_normalised[0]
            speed_y = bullet_normalised[1]
            if w.type == "bullet":
                bullet_companion = Projectile_bullet(self.x, self.y, speed_x, speed_y, p.colour, w.bounces, p, w.bullet_size, w.explosive_bullet_size)
                bullets.append(bullet_companion)                
                self.shoot_delay = self.max_shoot_delay
                self.can_shoot = False
            elif w.type == "explosive":
                bullet_companion = Projectile_explosive(self.x, self.y, speed_x, speed_y, p.colour, w.bounces, p, w.bullet_size, w.explosive_bullet_size)
                bullets.append(bullet_companion)                
                self.shoot_delay = self.max_shoot_delay
                self.can_shoot = False
            elif w.type == "laser":
                bullet_companion = Projectile_laser(self.x, self.y, self.x+speed_x, self.y+speed_y, p.colour, w.bounces, w.laser_size, p, screen, w.bullet_size, w.explosive_bullet_size)
                bullets.append(bullet_companion)                
                self.shoot_delay = self.max_shoot_delay
                self.can_shoot = False
