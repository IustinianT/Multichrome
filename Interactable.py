from UtilityFunctions import *

# INTERACTABLE
class Interactable():
    def __init__(self, x, y, width, shape, shape_colour, text_colour, text):
        self.x = x
        self.y = y
        self.width = width
        self.shape = shape
        self.text = text
        self.shape_colour = shape_colour
        self.text_colour = text_colour

    def check_interaction(self):
        if self.shape == "square":
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if pos[0] >= self.x and pos[0] <= self.x + self.width and pos[1] >= self.y and pos[1] <= self.y + self.width:
                    return True
        elif self.shape == "circle":
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                distance = distance_hypotenuse(self.x, self.y, pos[0], pos[1])
                if distance-self.width <= 0:
                    return True
        return False

    def display_interactable_and_text(self, screen):
        font = pygame.font.SysFont('arial', 30)
        if self.shape == "circle":
            pygame.draw.circle(screen, (self.shape_colour), [self.x,self.y], self.width)
            text = font.render(self.text, False, self.text_colour)
            screen.blit(text, (self.x+self.width*3/2,self.y-self.width/2))
        elif self.shape == "square":
            pygame.draw.rect(screen, (self.shape_colour), [self.x, self.y], self.width, self.width)
            text = font.render(self.text, False, self.text_colour)
            screen.blit(text, (self.x+self.width*3/2,self.y+self.width/2))
