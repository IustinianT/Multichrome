from Interactable import *

# MERCHANT
class Merchant(Interactable):
    def __init__(self, merchant_stats, items, id):
        Interactable.__init__(self, merchant_stats["x"], merchant_stats["y"], merchant_stats["width"], "square", merchant_stats["colour"],white, "")
        # multiplier range: 0.9 <= x <= 1.5
        self.min_multiplier = 0.9
        self.max_multiplier = 1.5
        self.price_multiplier = random.randint(self.min_multiplier*1000, self.max_multiplier*1000)/1000
        self.colour = merchant_stats["colour"]
        self.items = []
        self.interacted = False
        self.prices = {"common":int((merchant_stats["common_price"]+merchant_stats["price_scaling"])*self.price_multiplier), "rare":int((merchant_stats["rare_price"]+merchant_stats["price_scaling"])*self.price_multiplier), "epic":int((merchant_stats["epic_price"]+merchant_stats["price_scaling"])*self.price_multiplier), "legendary":int((merchant_stats["legendary_price"]+merchant_stats["price_scaling"])*self.price_multiplier)}
        self.can_interact = True
        self.reroll_price = -6
        self.reroll_price_increase = -1*self.reroll_price
        self.shape = "square"
        self.id = id

    def draw_merchant(self,screen):
        font = pygame.font.SysFont('arial', 35)
        for value in self.colour:
            value = value * (math.pow(self.price_multiplier/self.max_multiplier,2))
        pygame.draw.rect(screen, (self.colour), (self.x, self.y, self.width, self.width))
        reroll = font.render(f"Cost:{self.reroll_price}", False, white)
        screen.blit(reroll, (self.x+self.width/5, self.y+self.width/3))

    def display_items(self, screen):
        if self.interacted == True:
            index = -1
            for item in self.items:
                item.x = screen.get_width()/2 + 50*index
                item.y = self.y + screen.get_height()/4
                index += 1
                item.create_item(screen)
                
    def effect_on_interaction(self, items, p):
        self.reset_on_no_items(items)
        if self.check_interaction() and self.can_interact == True:
                print("INTERACTED")
                print()
                if self.interacted == False:
                    if p.coins >= self.reroll_price:
                        p.coins -= self.reroll_price
                        self.interacted = True
                        self.can_interact = False

    def reset_on_no_items(self,items):
        if len(self.items) <= 0:
            self.can_interact = True
            self.interacted = False
            self.reset_current(items)
            if self.check_same_item():
                self.remove_repetition(items)
            self.reroll_price += 6

    def reset_current(self, items):
        while len(self.items) > 0:
            self.items.pop()
        for i in range(3):
            random_item = random.choice(items)
            random_item.x,random_item.y = -100,-100
            self.items.append(random_item)

    def check_same_item(self):
        for i in range(0,len(self.items)):
            for j in range(1,len(self.items)):
                if i != j and self.items[i] == self.items[j]:
                    return True
        return False

    def display_prices(self, screen, room, merchant_stats):
        self.prices = {"common":int((merchant_stats["common_price"]+merchant_stats["price_scaling"])*self.price_multiplier), "rare":int((merchant_stats["rare_price"]+merchant_stats["price_scaling"])*self.price_multiplier), "epic":int((merchant_stats["epic_price"]+merchant_stats["price_scaling"])*self.price_multiplier), "legendary":int((merchant_stats["legendary_price"]+merchant_stats["price_scaling"])*self.price_multiplier)}
        if self.interacted == True:
            font = pygame.font.SysFont('arial', 20)
            for item in self.items:
                price = font.render(str(int(self.prices[f"{item.rarity}"])), False, white)
                screen.blit(price, (item.x-item.width/2, item.y+screen.get_height()/30))

    def remove_repetition(self, items):
        while self.check_same_item() == True:
            self.reset_current(items)

    def save_info(self):
        with open(f"SAVE_MERCHANT{self.id}.txt","w") as info_merchant:
            info_merchant.write(f"0;{self.price_multiplier};{self.id};\n")
            info_merchant.write(f"1;{self.reroll_price};{self.reroll_price_increase};\n")
            for item in self.items:
                info_merchant.write(f"2;{item.name};\n")
            info_merchant.write(f"3;{self.interacted};\n")

    def load_info(self, items, items_weapon):
        with open(f"SAVE_MERCHANT{self.id}.txt","r") as info_merchant:
            for line in info_merchant:
                temp_info = line.split(";")
                if temp_info[0] == "0":
                    self.price_multiplier = float(temp_info[1])
                    self.id = int(temp_info[2])
                elif temp_info[0] == "1":
                    self.reroll_price = int(temp_info[1])
                    self.reroll_price_increase = int(temp_info[2])
                elif temp_info[0] == "2":
                    self.items.append(select_item(temp_info[1],items,items_weapon))
                elif temp_info[0] == "3":
                    if temp_info[1].lower() == "true":
                        self.interacted = True
                    elif temp_info[1].lower() == "false":
                        self.interacted = False
