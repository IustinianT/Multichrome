from UtilityFunctions import *
from Interactable import *
from Merchant import *

# MAP AND ROOM
class Map:
    def __init__(self, width, height):
        self.size_x = width
        self.size_y = height
        self.display_x = 25
        self.display_y = 25
        self.room_width = 0
        self.room_height = 0
        self.current_room = [0,0]
        self.rooms_explored = set()
        self.stage = 1
        self.rooms = []

    def create_map(self,screen,items_weapon):
        index = 0
        shop_room_index = [random.randint(0,self.size_x-1), random.randint(0,self.size_y-1)]
        for i in range(0, self.size_x):
            for j in range(0, self.size_y):
                if [i,j] == shop_room_index:
                    shop_room_index = [random.randint(0,self.size_x-1), random.randint(0,self.size_y-1)]
                    shop_room = Room(index,[i,j],"shop")
                    shop_room = self.initiate_room_specials(screen, shop_room, items_weapon)
                    self.rooms.append(shop_room)
                else:
                    normal_room = Room(index,[i,j],"encounter_enemy")
                    self.initiate_room_specials(screen, normal_room, items_weapon)
                    self.rooms.append(normal_room)
                index += 1

    def initiate_room_specials(self, screen, room, items_weapon):
        can_add = False
        for room_in_rooms in self.rooms:
            if room.id != room_in_rooms.id:
                can_add = True
        if can_add == True:
            chance_value_recycler = random.randint(0, 10000)
            chance_value_weapon = random.randint(0, 10000)
            if chance_value_recycler <= 1000 and len(room.recycler) <= 0 and room.can_create_recycler == True:
                print("RECYCLER SPAWNED")
                room.recycler.append(Interactable(screen.get_width()/8,screen.get_height()/5,50,"circle",gray,white,"Recycler"))
                room.can_create_recycler = False
            else:
                room.can_create_recycler = False
            if len(items_weapon) > 0 and chance_value_weapon <= 2000 and room.can_create_weapon == True:
                print("WEAPON SPAWNED")
                choise = random.choice(items_weapon)
                room.items.append(choise)
            else:
                room.can_create_weapon = False
        return room

    def draw_map(self, screen):
        display_width = screen.get_width()
        display_height = screen.get_height()
        self.room_width = display_width/self.size_x
        self.room_height = display_height/self.size_y

        for room in self.rooms:
            if room.explored_status == False:
                colour = red_dark
                pygame.draw.rect(screen, (colour), (self.display_x+room.position[0]*(display_width/self.size_x), self.display_y+room.position[1]*(display_height/self.size_y), self.room_width - 50, self.room_height - 50))
            elif room.explored_status == True:
                if room.position != self.current_room and room.type == "encounter_enemy":
                    colour = green_dark
                elif room.type == "shop":
                    colour = yellow_dark
                else:
                    colour = white
                pygame.draw.rect(screen, (colour), (self.display_x+room.position[0]*(display_width/self.size_x), self.display_y+room.position[1]*(display_height/self.size_y), self.room_width - 50, self.room_height - 50))

    def choose_room(self):
        for room in self.rooms:
            if room.position == self.current_room:
                return room

    def explore_room(self):
        room = self.choose_room()
        room.explored_status = True
        if self.check_explored_rooms_id(room) == False:
            self.rooms_explored.add(room)

    def update_explored(self):
        for room in self.rooms:
            if room.explored_status == True:
                if self.check_explored_rooms_id(room) == False:
                    self.rooms_explored.add(room)

    def is_explored(self):
        room = self.choose_room()
        return room.explored_status

    def check_explored_rooms_id(self,room):
        for explored_room in self.rooms_explored:
            if explored_room.id == room.id:
                return True
        return False

    def reset(self, screen, items_weapon):
        room = self.choose_room()
        self.rooms_explored = set()
        self.rooms = []
        self.create_map(screen, items_weapon)
            
    def next_stage_on_map_completion(self, screen, o, merchant_stats, button_next_stage, items_weapon):
        room = self.choose_room()
        button_next_stage.text = f"Stage {self.stage+1}"
        if len(self.rooms_explored) == self.size_x * self.size_y and len(o.enemies) == 0:
            if button_next_stage not in room.interactables and o.can_spawn_boss == False:
                room.interactables.append(button_next_stage)
            room.display_interactables(screen)
            if button_next_stage.check_interaction():
                self.stage += 1
                merchant_stats["price_scaling"] = (self.stage-1)*4
                self.reset(screen, items_weapon)
                o.reset()
                o.can_spawn_boss = True
                self.explore_room()

    def movement(self, screen, p, o, enemy_melee, enemy_ranged, enemy_bonus, enemy_boss, elements, elements_list, bullets, items_weapon, items_common, items_rare, items_epic, items_legendary):
        room = self.choose_room()
        if len(o.enemies) <= 0:
            room.spawn_specials(screen)
            if len(room.recycler) > 0:
                if room.recycler[0].check_interaction() == True and p.can_interact[0] == True:
                    if len(p.scrap_items) > 0:
                        p.recycle(items_common, items_rare, items_epic, items_legendary)
                        p.can_interact[0] = False
                        p.can_interact[1] = 2
                        print("interacted")
                        print()

        screen_size = (screen.get_width(),screen.get_height())

        # CHECK IF ROOM HAS FINISHED (ADD TO CURRENT ROOM) ----- MAP/ROOM MOVEMENT
        if room.finished == True and len(o.enemies) <= 0:
            ## MOVING RIGHT
            if p.x >= screen_size[0]:
                if self.current_room[0] < self.size_x - 1:
                    self.current_room[0] += 1
                    p.x = 1
                    self.next_room_movement(screen, p, o, enemy_melee, enemy_ranged, enemy_bonus, enemy_boss, elements, elements_list, bullets)
                else:
                    p.lock_movement(screen)
            ## MOVING LEFT
            elif p.x + p.width <= 0:
                if self.current_room[0] > 0:
                    self.current_room[0] -= 1
                    p.x = screen_size[0] - 1
                    self.next_room_movement(screen, p, o, enemy_melee, enemy_ranged, enemy_bonus, enemy_boss, elements, elements_list, bullets)
                else:
                    p.lock_movement(screen)
            ## MOVING DOWN
            elif p.y >= screen_size[1]:
                if self.current_room[1] < self.size_y - 1:
                    self.current_room[1] += 1
                    p.y = 1
                    self.next_room_movement(screen, p, o, enemy_melee, enemy_ranged, enemy_bonus, enemy_boss, elements, elements_list, bullets)
                else:
                    p.lock_movement(screen)
            ## MOVING UP
            elif p.y + p.height <= 0:
                if self.current_room[1] > 0:
                    self.current_room[1] -= 1
                    p.y = screen_size[1] - 1
                    self.next_room_movement(screen, p, o, enemy_melee, enemy_ranged, enemy_bonus, enemy_boss, elements, elements_list, bullets)
                else:
                    p.lock_movement(screen)

            self.explore_room()
        elif o.bosses_on_screen > 0 or len(o.enemies) > 0:
            room.finished = False
            p.lock_movement(screen)

    def next_room_movement(self, screen, p, o, enemy_melee, enemy_ranged, enemy_bonus, enemy_boss, elements, elements_list, bullets):
        room = self.choose_room()
        clear_bullets(bullets)
        if not self.check_explored_rooms_id(room):
            if len(self.rooms_explored) < self.size_x*self.size_y-1:
                o.spawn_enemies(screen, p, enemy_melee, enemy_ranged, enemy_bonus, elements, elements_list, self.stage)
            room.finished = False

    def save_info(self):
        with open("SAVE_MAP.txt","w") as info_map:
            info_map.write(f"0;{self.current_room[0]};{self.current_room[1]};{self.stage};\n")
            for room in self.rooms:
                print("ID of room in rooms :",room.id)
                info_map.write(f"1;{room.id};{room.position[0]};{room.position[1]};{room.type};{room.explored_status};{room.finished};{room.merchant};{len(room.recycler)};")
                if len(room.recycler) > 0:
                    info_map.write(f"{room.recycler[0].x};{room.recycler[0].y};\n")
                else:
                    info_map.write("\n")
        print("SAVED MAP INFO")

    def load_info(self):
        with open("SAVE_MAP.txt","r") as info_map:
            for line in info_map:
                temp_info = line.split(";")
                if temp_info[0] == "0":
                    self.current_room = [int(temp_info[1]),int(temp_info[2])]
                    self.stage = int(temp_info[3])
                elif temp_info[0] == "1":
                    temp_room = Room(int(temp_info[1]),[int(temp_info[2]),int(temp_info[3])],temp_info[4])
                    print(temp_room.type,"  ",temp_room.position)
                    if temp_info[5].lower() == "true":
                        temp_room.explored_status = True
                    elif temp_info[5].lower() == "false":
                        temp_room.explored_status = False
                    temp_room.merchant = 0
                    if temp_info[6].lower() == "true":
                        temp_room.finished = True
                    elif temp_info[6].lower() == "false":
                        temp_room.finished = False
                    if temp_info[7] != "0":
                        temp_room.merchant = 1
                    if int(temp_info[8]) > 0:
                        temp_room.recycler.append(Interactable(float(temp_info[9]),float(temp_info[10]),50,"circle",gray,white,"Recycler"))
                    self.rooms.append(temp_room)
                    print("LOADED ROOM")
                    if temp_room.explored_status == True:
                        self.rooms_explored.add(temp_room)
                        print("LOADED EXPLORED ROOM")

        print("LOADED MAP INFO")

    def load_merchant_in_all_rooms(self, items, items_weapon, merchant_stats):
        for room in self.rooms:
            if room.merchant != 0:
                print("MERCHANT TO LOAD :",room.merchant)
                merchant = Merchant(merchant_stats, items, room.id)
                merchant.load_info(items, items_weapon)
                room.merchant = merchant
                print("PRICE MULTIPLIER :",merchant.price_multiplier)

class Room():
    def __init__(self, id, position, type_room):
        self.id = id
        self.position = position
        self.items = []
        self.type = type_room
        self.explored_status = False
        self.finished = False
        self.merchant = 0
        self.interactables = []
        self.recycler = []
        self.can_create_recycler = True
        self.can_create_weapon = True

    def add_item(self, item):
        self.items.append(item)

    def display_items(self, screen):
        for item in self.items:
            item.create_item(screen)

    def clear_items(self):
        for item in self.items:
            self.items.remove(item)

    def shop_initiate(self, screen, items, stage, merchant_stats, p, o):
        if self.merchant == 0 and self.type == "shop":
            merchant = Merchant(merchant_stats, items, self.id)
            self.merchant = merchant
            print(f"MERCHANT SPAWNED: {self.merchant}")
        elif self.merchant != 0:
            if len(o.enemies) <= 0:
                self.merchant.draw_merchant(screen)
                self.merchant.effect_on_interaction(items, p)
                self.merchant.display_items(screen)
                self.merchant.display_prices(screen, self, merchant_stats)
            check_mouse_on_item_room(screen, self.merchant)

    def spawn_specials(self,screen):
        if len(self.recycler) > 0:
            self.recycler[0].display_interactable_and_text(screen)

    def display_interactables(self, screen):
        for interactable in self.interactables:
            interactable.display_interactable_and_text(screen)
