from UtilityFunctions import *

class Explosion():
    def __init__(self, x, y, width, colour, linger):
        self.x = x
        self.y = y
        self.width = width
        self.colour = colour
        self.linger = linger

    def create_explosion(self, screen):
        temp_colour = []
        for i in range(len(self.colour)):
            temp_colour.append(self.colour[i])
        for i in range(len(temp_colour)):
            temp_colour[i] *= self.linger
        return pygame.draw.circle(screen, (temp_colour), (self.x, self.y), self.width)

class Effect():
    def __init__(self, x, y, width, colour):
        self.x = x
        self.y = y
        self.width = width
        self.colour = colour

    def create_effect(self, screen):
        pygame.draw.circle(screen, self.colour, (self.x,self.y), self.width)
