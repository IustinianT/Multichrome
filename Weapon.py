
# WEAPON
class Weapon():
    def __init__(self, element, fire_effect, ice_effect, poison_effect, duration, type, bullet_damage, laser_damage, explosive_damage,  shoot_delay, bullet_size, explosive_bullet_size, laser_size, bullet_vel):
        self.element = element
        self.effect_fire = fire_effect
        self.effect_ice = ice_effect
        self.effect_poison = poison_effect
        self.duration = duration

        self.type = type

        self.extra_damage_boss = 0
        self.max_bullet_damage = bullet_damage
        self.max_laser_damage = laser_damage
        self.max_explosive_damage = explosive_damage
        self.bullet_damage = bullet_damage
        self.laser_damage = laser_damage
        self.explosive_damage = explosive_damage

        self.bullet_vel = bullet_vel
        self.shoot_delay = shoot_delay
        self.max_shoot_delay = shoot_delay
        self.bullet_size = bullet_size
        self.max_bullet_size = bullet_size
        self.explosive_bullet_size = explosive_bullet_size
        self.max_explosive_bullet_size = explosive_bullet_size
        self.laser_size = laser_size
        self.max_laser_size = laser_size
        self.can_shoot = True
        self.start_shot_time = 0
        self.bounces = 0
        self.multishot = 0
