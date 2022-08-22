import pygame
import time as t
import math
import random
import os
import ctypes
import sys

# COLOURS
black = [0,0,0]
gray = [192,192,192]
red = [255,0,0]
red_dark = [95,0,0]
green = [0,255,0]
green_item = [14,209,69]
green_dark = [0,75,0]
blue = [135,206,235]
blue_item = [0,168,243]
white = [255,255,255]
yellow = [255,255,0]
yellow_dark = [197,171,49]
orange = [255,70,0]
purple = [127,0,255]
purple_item = [184,61,186]

##### UTILITY FUNCITONS #####
def normalise_distance(mouse_x, mouse_y, player_x, player_y, size):
    magnitude = size
    hypotenuse = math.sqrt((mouse_x-player_x)**2 + (mouse_y-player_y)**2)
    scale_factor = hypotenuse/magnitude
    new_x = (mouse_x-player_x)/scale_factor
    new_y = (mouse_y-player_y)/scale_factor

    return new_x, new_y

def normalise_speed(speed_x, speed_y, new_speed):
    magnitude = math.sqrt((speed_x)**2 + (speed_y)**2)
    scale_factor = magnitude/new_speed
    if scale_factor != 0:
        speed_x = speed_x/scale_factor
        speed_y = speed_y/scale_factor
        speed = [speed_x, speed_y]
        return speed
    speed = [speed_x, speed_y]
    return speed

def distance_hypotenuse(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def find_direction_speed(magnitude,angle):
    radians = angle*math.pi/180
    x = math.cos(radians)
    y = math.sin(radians)
    speed = normalise_speed(x,y,magnitude)
    return speed[0],speed[1]

##### FUNCTION TO HELP REPEAT PROCESS A CERTAIN AMOUNT OF TIMES PER SECOND
def repeat_process_new(start_time, end_time, seconds_frequency):
    if end_time - start_time >= seconds_frequency:
        return True
    return False

##### FUNCTION FOR REMOVING ALL BULLETS FROM SCREEN
def clear_bullets(bullets):
    for i in range(len(bullets)):
        bullets.pop()

def create_display(screen, player):
    displacement_from_edge_x = screen.get_width()/20
    displacement_from_edge_y = screen.get_height()/24
    for i in range(0, len(player.items)):
        player.items[i].x = displacement_from_edge_x+i*player.items[i].width
        player.items[i].y = screen.get_height()-displacement_from_edge_y-player.items[i].width
        player.items[i].display_icon(screen, displacement_from_edge_x+i*player.items[i].width, screen.get_height()-displacement_from_edge_y-player.items[i].width)

def check_mouse_on_item_display(screen, player, room):
    font = pygame.font.SysFont('arial', 20)
    mouse_x,mouse_y = pygame.mouse.get_pos()
    distance_from_item_y = 25
    for item in player.items:
        if mouse_x > item.x and mouse_x < item.x+item.width:
            if mouse_y > item.y and mouse_y < item.y+item.width:
                description = font.render(item.description+f" x{item.amount}", False, white)
                screen.blit(description, (mouse_x, mouse_y-distance_from_item_y))

def check_mouse_on_item_room(screen, room):
    font = pygame.font.SysFont('arial', 20)
    mouse_x,mouse_y = pygame.mouse.get_pos()
    distance_from_item_y = 35
    for item in room.items:
        distance = math.sqrt(math.pow(mouse_x-item.x,2)+math.pow(mouse_y-item.y,2))
        if distance - item.width <= 0:
            description = font.render(item.description, False, white)
            screen.blit(description, (mouse_x-len(item.description)*3.5, mouse_y-distance_from_item_y))

def dot_product(vector1, vector2):
    return vector1[0]*vector2[0]+vector1[1]*vector2[1]

def display_item_and_description(screen,player, healthbar):
    max_image_size = 90
    displacement_from_edge_x = 50
    displacement_from_edge_y = 10
    font_size = 25
    font = pygame.font.SysFont('arial', font_size)
    for i in range(len(player.items)):
        icon = player.items[i].icon
        name = font.render(player.items[i].name+":", False, white)
        description = font.render(player.items[i].description+f" x{player.items[i].amount}", False, white)
        if int((healthbar.y-displacement_from_edge_y)/len(player.items)) < max_image_size:
            y_icon = int((healthbar.y-displacement_from_edge_y)/len(player.items))
        else:
            y_icon = max_image_size
        icon_big = pygame.transform.scale(icon, (y_icon, y_icon))
        screen.blit(icon_big,(displacement_from_edge_x, i*y_icon+10))
        screen.blit(name,(displacement_from_edge_x+y_icon, i*y_icon+10))
        screen.blit(description, (y_icon+len(player.items[i].name)+name.get_width()+displacement_from_edge_x, i*y_icon+10))

def select_item(item_name, items, items_weapon):
    for item in items:
        if item.name == item_name:
            return item
    for item in items_weapon:
        if item.name == item_name:
            return item
    return False

def save_time(total_time):
    with open("SAVE_TIME.txt","w") as info_time:
        info_time.write(f"{total_time}")
        print(f"TOTAL TIME :{total_time}")

def load_time():
    with open("SAVE_TIME.txt","r") as info_time:
        for line in info_time:
            temp_info = line.split("\n")
            if len(temp_info[0]) > 0:
                return int(temp_info[0])
            else:
                return 0

def save_merchant_in_all_rooms(map):
    for room in map.rooms:
        if room.merchant != 0:
            room.merchant.save_info()

def show_controls(screen, controls):
    font = pygame.font.SysFont('arial', 30)
    index = 0
    size = len(controls)
    for key in controls:
        key_value_text = font.render(f"{key}  =>  {controls[f'{key}']}", False, white)
        screen.blit(key_value_text, (screen.get_width()/3, screen.get_height()*((index+1)/size)-screen.get_height()/15))
        index += 1

def generate_item_names(items, items_weapon):
    item_names = []
    final_list = []
    with open("SAVE_ITEMS.txt","r") as info_items:
        for line in info_items:
            temp_data = line.split(";")
            item_names.append(temp_data[0])

    for item in items:
        if item.name in item_names:
            final_list.append(item.name)
        elif item.name not in item_names:
            final_list.append("?")
    for item in items_weapon:
        if item.name in item_names:
            final_list.append(item.name)
        elif item.name not in item_names:
            final_list.append("?")

    return final_list

def show_item_codex(screen, items, items_weapon):
    font = pygame.font.SysFont('arial', 25)
    index = 0
    item_names = generate_item_names(items, items_weapon)
    size = len(items)
    for item_name in item_names:
        if item_name == "?":
            item_name_description_text = font.render(f"?  =>  ?", False, white)
            screen.blit(item_name_description_text, (screen.get_width()/5, screen.get_height()*((index)/(size+2))))
        elif item_name != "?":
            temp_item = select_item(item_name, items, items_weapon)
            item_name_description_text = font.render(f"{temp_item.name}  =>  {temp_item.description}", False, white)
            screen.blit(item_name_description_text, (screen.get_width()/5, screen.get_height()*((index)/(size+2))))
        index += 1
                

def save_game(map, p, o, total_time):
    for room in map.rooms:
        if room.explored_status == True:
            for item in room.items:
                if not p.check_item_in_items(item.name):
                    p.items.append(item)
                    print(f"added NEW item: {item.name}")
                else:
                    p.add_one_to_item_amount(item.name)
                room.items.remove(item)
                print("added item")
    p.save_info()
    map.save_info()
    o.save_info()
    save_time(total_time)
    save_merchant_in_all_rooms(map)

def scrap_amount(player):
    scraps = 0
    for item in player.scrap_items:
        scraps += item.amount
    return scraps

def reset_files():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_names = [filename for filename in os.listdir(dir_path) if filename.startswith("SAVE")]
    for file_name in file_names:
        if "SAVE_MERCHANT" in file_name:
            os.remove(file_name)
        else:
            with open(file_name,'w') as file_info:
                file_info.write("")