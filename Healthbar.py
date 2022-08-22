from UtilityFunctions import *

# HEALTHBAR
class Healthbar:
    def __init__(self, x, y, width, height, colour):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.max_size = width

    def draw_healthbar(self, screen, p):
        if p.hp/p.max_hp >= 0 and p.hp/p.max_hp <= 1:
            self.colour[0] = 255*(1-p.hp/p.max_hp)
            self.colour[1] = 255*(p.hp/p.max_hp)
            self.width = self.max_size * (p.hp/p.max_hp)
        else:
            self.colour[0] = 0
            self.colour[1] = 255
            self.colour[2] = 0
            self.width = self.max_size
        pygame.draw.rect(screen, (self.colour), (self.x, self.y, self.width, self.height))
