from Player import *
from Projectile import *
from Effects import *
from Items import *
from Enemies import *
from Map import *
from Interactable import *
from Operator import *
from Weapon import *
from Companion import *
from UtilityFunctions import *

def main():
    # used for screen resolution
    user32 = ctypes.windll.user32
    # initiating pygame
    pygame.init()

    screen_size = initial_width, initial_height = int(user32.GetSystemMetrics(0)*3/4), int(user32.GetSystemMetrics(1)*3/4)
    original_screen_size = screen_size

    width = initial_width
    height = initial_height
    screen = pygame.display.set_mode(screen_size)

    can_change_display = True

    ##### IMAGES AND EFFECTS
    fire_big = pygame.image.load(r"EFFECTS\Effect_fire.png")
    fire = pygame.transform.scale(fire_big, (15,15))
    ice_big = pygame.image.load(r"EFFECTS\Effect_ice.png")
    ice = pygame.transform.scale(ice_big, (15,15))
    poison_big = pygame.image.load(r"EFFECTS\Effect_poison.png")
    poison = pygame.transform.scale(poison_big, (15,15))
    void_big = pygame.image.load(r"EFFECTS\Effect_void.png")
    void = pygame.transform.scale(void_big, (15,15))

    # CONTROLS
    controls = {"Move up":"up arrow / W", "Move left":"left arrow / A", "Move down":"down arrow / S", "Move right":"right arrow / D", "Shoot":"left click", "Interact":"left click", "Quick save":"ctrl S", "Elements: Neutral/Fire/Ice/Poison":"1 / 2 / 3 / 4", "Weapons: Bullet/Explosive/Laser":"open square bracket / close square bracket / #", "Show items":"TAB", "Show map":"M"}

    # ELEMENTS 
    elements_list = [ "neutral", "fire", "ice", "poison", "void"]
    elements = {"fire":red, "ice":blue, "poison":green_dark, "neutral":orange, "void":purple}

    ### STATS
    enemy_melee = {"damage":12, "collision_damage":5, "hp":24, "vel":1.5, "hp_growth":1.70, "damage_growth":5, "vel_growth":1.01, "width":10, "element":"neutral", "fire_effect":2, "ice_effect":0.45, "poison_effect":0.95, "void_effect":6, "fire_effect_growth":2, "ice_effect_growth":0.96, "poison_effect_growth":0.98, "duration":4}
    enemy_ranged = {"damage":8, "collision_damage":2, "hp":16, "vel":2, "hp_growth":1.35, "damage_growth":3, "vel_growth":1.005, "shoot_delay":1, "shoot_delay_growth":0.92, "bullet_vel":7, "width":14, "element":"neutral", "fire_effect":2, "ice_effect":0.65, "poison_effect":0.95, "void_effect":8, "fire_effect_growth":2, "ice_effect_growth":0.96, "poison_effect_growth":0.98, "duration":3, "bullet_size":6, "explosive_bullet_size":10}
    enemy_bonus = {"damage":30, "collision_damage":20, "hp":35, "vel":2, "hp_growth":2, "damage_growth":10, "vel_growth":1.06, "width":10, "element":"neutral", "fire_effect":5, "ice_effect":0.25, "poison_effect":0.95, "void_effect":8, "fire_effect_growth":2, "ice_effect_growth":0.96, "poison_effect_growth":0.98, "duration":6}
    enemy_boss = {"damage":16, "collision_damage":30, "hp":500, "vel":0.7, "hp_growth":2, "damage_growth":2, "vel_growth":1.005, "shoot_delay":0.25, "shoot_delay_growth":0.99, "bullet_vel":7, "width":100, "element":"neutral", "fire_effect":2, "ice_effect":0.85, "poison_effect":0.95, "void_effect":4, "fire_effect_growth":2, "ice_effect_growth":0.96, "poison_effect_growth":0.98, "duration":3, "bullet_size":6, "explosive_bullet_size":10}

    player = {"collision_damage":20, "hp":100, "vel":8, "width":50, "element":"neutral"}
    weapon = {"fire_effect":2, "ice_effect":0.30, "poison_effect":0.90, "fire_effect_growth":2, "ice_effect_growth":0.96, "poison_effect_growth":0.98, "duration":3, "weapon_type":"bullet", "bullet_damage":4, "explosive_damage":6, "laser_damage":10, "shoot_delay":1, "bullet_size":6, "explosive_bullet_size":10, "laser_size":75, "bullet_vel":10}
    companion = {"vel":3, "width":12 , "shoot_delay":0.6, "shoot_delay_growth":1}

    operator = {"limit_enemies":10, "max_enemies":5, "total_max_enemies_increase":1, "spawn_radius":100}
    map_stats = {"width":3, "height":2}
    merchant_stats = {"x":screen.get_width()/2-screen.get_width()/20, "y":screen.get_height()/10, "width":screen.get_width()/10, "colour":[155,106,70], "common_price":6, "rare_price":12, "epic_price":25, "legendary_price":45, "price_scaling":0}

    # ALL ITEMS LIST
    items = []
    items_common = []
    items_rare = []
    items_epic = []
    items_legendary = []
    items_weapon = []

    info = []
    rarity_to_colour = {"common":green_item,"rare":blue_item,"epic":purple_item,"legendary":yellow,"weapon":white}

    ############### READ FROM ITEMS AND ADD STATS ACCORDINGLY ###############
    with open("ITEMS.txt", 'r') as ITEMS:
        for line in ITEMS:
            info.append(line.split('\n')[0])
        for line in info:
            print(line)
            line = line.split(";")
            icon_big = pygame.image.load(fr"ICONS\{line[2].upper()}.png")
            icon = pygame.transform.scale(icon_big, (15,15))
            if line[3] == "stackable":
                if line[2] != "weapon":
                    items.append(Item(250,250,15,rarity_to_colour[line[2]],line[1],icon,line[2],line[0],True,int(line[4])))
                if line[2] == "common":
                    items_common.append(Item(250,250,15,rarity_to_colour[line[2]],line[1],icon,line[2],line[0],True,int(line[4])))
                elif line[2] == "rare":
                    items_rare.append(Item(250,250,15,rarity_to_colour[line[2]],line[1],icon,line[2],line[0],True,int(line[4])))
                elif line[2] == "epic":
                    items_epic.append(Item(250,250,15,rarity_to_colour[line[2]],line[1],icon,line[2],line[0],True,int(line[4])))
                elif line[2] == "legendary":
                    items_legendary.append(Item(250,250,15,rarity_to_colour[line[2]],line[1],icon,line[2],line[0],True,int(line[4])))
                elif line[2] == "weapon":
                    items_weapon.append(Item(250,250,15,rarity_to_colour[line[2]],line[1],icon,line[2],line[0],True,int(line[4])))

            elif line[3] == "not_stackable":
                if line[2] != "weapon":
                    items.append(Item(250,250,15,rarity_to_colour[line[2]],line[1],icon,line[2],line[0],False,int(line[4])))
                if line[2] == "common":
                    items_common.append(Item(250,250,15,rarity_to_colour[line[2]],line[1],icon,line[2],line[0],False,int(line[4])))
                elif line[2] == "rare":
                    items_rare.append(Item(250,250,15,rarity_to_colour[line[2]],line[1],icon,line[2],line[0],False,int(line[4])))
                elif line[2] == "epic":
                    items_epic.append(Item(250,250,15,rarity_to_colour[line[2]],line[1],icon,line[2],line[0],False,int(line[4])))
                elif line[2] == "legendary":
                    items_legendary.append(Item(250,250,15,rarity_to_colour[line[2]],line[1],icon,line[2],line[0],False,int(line[4])))
                elif line[2] == "weapon":
                    items_weapon.append(Item(250,250,15,rarity_to_colour[line[2]],line[1],icon,line[2],line[0],False,int(line[4])))
    print()

    for item in items:
        print(f"{item.name}")

    items = tuple(items)
    items_weapon = tuple(items_weapon)
    items_common = tuple(items_common)
    items_rare = tuple(items_rare)
    items_epic = tuple(items_epic)
    items_legendary = tuple(items_legendary)

    # PLAYER
    p = Player(50, 50, player["vel"], player["hp"], player["collision_damage"], player["width"], player["element"], orange)
    # HEALTHBAR (player)
    healthbar = Healthbar(screen.get_width()/22, screen.get_height()*17/20, screen.get_width()*2/5, screen.get_height()/24, [0,255,0])
    # WEAPON
    w = Weapon(p.element, weapon["fire_effect"], weapon["ice_effect"], weapon["poison_effect"], weapon["duration"], weapon["weapon_type"], weapon["bullet_damage"], weapon["laser_damage"], weapon["explosive_damage"],  weapon["shoot_delay"], weapon["bullet_size"], weapon["explosive_bullet_size"], weapon["laser_size"], weapon["bullet_vel"])
    # MAP 
    map = Map(map_stats["width"], map_stats["height"])
    # OPERATOR 
    o = Operator(operator["limit_enemies"], operator["max_enemies"], operator["total_max_enemies_increase"], operator["spawn_radius"])
    # COMPANION
    c = Companion(companion["vel"],companion["width"],companion["shoot_delay"])

    # TIME VARIABLE
    total_time = 0

    # BUTTONS FOR THE MENU 
    button_new_game = Interactable(screen.get_width()/20, screen.get_height()/6, 40, "circle", green, white, "New Game")
    button_load_game = Interactable(screen.get_width()/20, screen.get_height()/3, 40, "circle", green, white, "Load Game")
    button_controls = Interactable(screen.get_width()/20, screen.get_height()/2, 40, "circle", green, white, "Controls")
    button_item_codex = Interactable(screen.get_width()/20, screen.get_height()*2/3, 40, "circle", green, white, "Item Codex")
    button_quit = Interactable(screen.get_width()/20, screen.get_height()*5/6, 40, "circle", green, white, "Quit")

    buttons = [button_new_game, button_load_game, button_controls, button_item_codex, button_quit]

    state = "menu"
    display_menu = "none"

    # LOADING THE GAME OPTION

    while state == "menu":
        pygame.time.delay(20)
        screen.fill(black)
        for button in buttons:
            button.display_interactable_and_text(screen)

        keys = pygame.key.get_pressed()
        if button_new_game.check_interaction():
            map.create_map(screen,items_weapon)
            reset_files()
            state = "game"

        elif button_load_game.check_interaction():
            try:
                p.load_info(items, items_weapon)
                o.load_info()
                map.load_info()
                total_time = load_time()
                map.load_merchant_in_all_rooms(items, items_weapon, merchant_stats)
                state = "game"
            except Exception as ex:
                print("An error happened while loading the game, perhaps you do not have a saved set of files. Suggestion: start a new game.")
                print(ex)

        elif button_controls.check_interaction():
            display_menu = "controls"
    
        elif button_item_codex.check_interaction():
            display_menu = "item_codex"

        elif button_quit.check_interaction():
            sys.exit(0)

        if display_menu == "controls":
            show_controls(screen, controls)

        elif display_menu == "item_codex":
            show_item_codex(screen, items, items_weapon)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = "end"

        pygame.display.update()

    # GAME RELATED BUTTONS
    button_next_stage = Interactable(screen.get_width()/2, screen.get_height()/2, 35, "circle", green, white, f"Stage: {map.stage+1}")

    # ADDITIONAL INFO
    bullets = []
    explosions = []
    if len(map.rooms) > 0:
        map.explore_room()
        room = map.choose_room()
        room.finished = True

    # REST OF TIME VARIABLES
    time_start_game = t.time()
    time_text = "0"
    check_change1 = False
    initial_time = time_start_game
    current_time = 0

    while state == "game" and p.alive() == True:
        pygame.time.delay(20)
        time1 = t.time()
        screen.fill(black)

        # VARIABLES UPDATED EVERY REPETITION TO KEEP TRACK OF 'PER SECOND' PROCESSES
        before_change = current_time
        current_time = int(time1 - time_start_game)
        after_change = current_time
        if after_change - before_change != 0:
            total_time += 1
            if current_time > total_time:
                current_time = total_time
            check_change1 = True

        ## DISPLAYING LASER FIRST, SO THAT BULLETS CAN OVERRIDE IT AND BE SEEN
        for bullet in bullets:
            if bullet.type == "laser":
                bullet.create_bullet(screen)
                if bullet.linger <= 0:
                    bullets.remove(bullet)
                else:
                    bullet.linger -= 0.02
                bullet.can_damage = False

        # SETTING THE 'ROOM' TO THE CURRENT ROOM OBJECT
        room = map.choose_room()
        # CHECK IF THE MAP HAS FINISHED
        map.next_stage_on_map_completion(screen, o, merchant_stats, button_next_stage, items_weapon)
        map.update_explored()

        # CHECK IF ALL ENEMIES HAVE DIED AND THE ROOM WAS RECENTLY UNFINISHED
        if len(o.enemies) == 0 and room.finished == False:
            room.finished = True
            p.debuff_void[0] = False

        # SPAWN BOSS ON LAST ROOM
        if len(map.rooms_explored) == map.size_x*map.size_y and o.bosses_on_screen == 0 and o.can_spawn_boss == True:
            o.spawn_boss(screen,enemy_boss,map.stage,p)
    
        ### SHOW EXPLOSIONS/LASERS (display)
        for explosion in explosions:
            if explosion.linger <= 0:
                explosions.remove(explosion)
            else:
                explosion.create_explosion(screen)
                explosion.linger -= 0.02

        # APPLY ITEM EFFECTS
        for item in p.items:
            item.apply_effect(p, player, w, weapon, c, companion)

        map.movement(screen, p, o, enemy_melee, enemy_ranged, enemy_bonus, enemy_boss, elements, elements_list, bullets, items_weapon, items_common, items_rare, items_epic, items_legendary)

        ###############################################################################################################################
        ########################################## EFFECTS THAT HAPPEN PER TIME FRAME (second) ########################################
        ###############################################################################################################################
        if check_change1 == False:
            initial_time = time1
            check_change1 = True

        if repeat_process_new(initial_time, time1, 1) == True and check_change1 == True:
            for enemy in o.enemies:
                enemy.apply_debuff(w)
                enemy.debuff_expire_check()     
        
            # PLAYER DEBUFFS BEING APPLIED
            p.apply_debuff()
            # PLAYER CAN BUY ITEM (TO AVOID ACCIDENTAL PURCHASES)
            if p.can_interact[0] == False:
                p.can_interact[1] -= 10
            if p.can_interact[1]<=0:
                p.can_interact[0] = True

            print(p.vel)

            can_change_display = True
            check_change1 = False
        ###############################################################################################################################
        ###############################################################################################################################
        ###############################################################################################################################
    
        # PLAYER BUFFS BEING APPLIED AND DEBUFF EXPIRATION CHECK
        p.apply_item_buffs(screen, w)
        p.debuff_expire_check()
        p.check_items_to_scrap()
    
        # ELEMENT EFFECTS for player
        if p.check_fire():
            screen.blit(fire,(p.x-15, p.y-15))
        if p.check_ice():
            screen.blit(ice,(p.x+5, p.y-15))
        if p.check_poison():
            screen.blit(poison,(p.x+25, p.y-15))
        if p.check_void():
            screen.blit(void,(p.x+45, p.y-15))

        ### ALLOW BULLETS TO TRAVEL AND BE DISPLAYED
        ## DISPLAYING BULLETS AND DOING THE COLLISIONS ON COMPANION AND PLAYER
        for bullet in bullets:
            if bullet.type != "laser":
                bullet.travel(screen,bullets)
                bullet.create_bullet(screen)
            
            # ENEMY BULLETS ON COMPANION
            if c.exists:
                c.collided_bullet(bullet, bullets)
            if bullet.shot_by.type != "player" and bullet.shot_by.type != "companion":
                # ENEMY BULLETS ON PLAYER
                p.collided_bullet(bullet, bullets, healthbar, enemy_ranged, enemy_boss)

        ### MERCHANT AND SHOP ROOM
        if room.type == "shop" and room.finished == True:
            room.shop_initiate(screen, items, map.stage, merchant_stats, p, o)
            p.check_buy_item(room.merchant)

        ### ITEMS - DISPLAY AND CREATION
        for item in room.items:
            p.check_item_collision(item, room)
            item.create_item(screen)

        ##### SPAWNING ENEMIES AND DISPLAY
        for enemy in o.enemies:
            # CHECK IF ENEMY HAS TAKEN FATAL DAMAGE
            if enemy.alive() == False:
                room.items = enemy.on_death_spawn_item(items_common, items_rare, items_epic, items_legendary, room)
                if enemy.type == "boss":
                    o.bosses_on_screen = 0
                    room.finished = True
                    print("KILLED BOSS")
                o.enemies.remove(enemy)
                p.enrage()
                p.add_coins(enemy,map)

            if enemy.type == "boss":
                # BOSS ROTATION
                enemy.rotate(50*0.02)
                # ELEMENT OF BOSS BASED ON HEALTH
                enemy.check_health_percentage()

            #### SHOOTING - RANGED ENEMIES
            enemy.shooting(p, bullets)
            #### COLLISIONS
            p.collided_enemy(enemy, healthbar)
            ### BULLET COLLISION (projectile)
            for bullet in bullets:
                # PLAYER BULLETS ON ENEMIES
                if bullet.shot_by.type == "player" or bullet.shot_by.type == "companion":
                    bullet.collided_bullet(bullets, enemy, w, p, o, explosions, c, screen)

            enemy.update_healthbar()
            enemy.movement(screen, p)
            enemy.draw_enemy(screen)
            enemy.draw_healthbar(screen)
            enemy.display_debuffs(screen, fire, ice, poison)
        o.check_bosses()

        # PLAYER MOVEMENT
        p.movement_and_inputs()
        # DISPLAY PLAYER,COMPANION AND HEALTHBAR
        p.draw_player(screen)
        if c.exists:
            ### COMPANION SHOOTING
            if len(o.enemies)>0:
                enemy = random.choice(o.enemies)
                c.shooting(screen, o, w, p, enemy, bullets)
            # MOVEMENT AND DISPLAY OF COMPANION
            c.movement(p,w)
            c.create_companion(screen,p)
        healthbar.draw_healthbar(screen, p)

        #### SHOOTING - PLAYER
        p.shooting(screen, w, bullets)

        # DETECTING KEY PRESSES
        keys = pygame.key.get_pressed()
        # TESTING AREA (WHERE CODE AND INPUTS ARE TESTED)
        if keys[pygame.K_1]:
            # neutral element
            p.set_element(elements_list[0], elements, weapon)
        if keys[pygame.K_2] and p.can_change_fire == True:
            # fire element
            p.set_element(elements_list[1], elements, weapon)
        if keys[pygame.K_3] and p.can_change_ice == True:
            # ice element
            p.set_element(elements_list[2], elements, weapon)
        if keys[pygame.K_4] and p.can_change_poison == True:
            # poison element
            p.set_element(elements_list[3], elements, weapon)
        if keys[pygame.K_t]:
            # reset hp
            p.hp = p.max_hp
        if keys[pygame.K_l]:
            # kill all enemies
            for enemy in o.enemies:
                p.add_coins(enemy, map)
                o.enemies.remove(enemy)
        # weapon types
        if keys[pygame.K_RIGHTBRACKET] and p.can_change_explosive == True:
            w.type = "explosive"
        elif keys[pygame.K_LEFTBRACKET]:
            w.type = "bullet"
        elif keys[pygame.K_HASH] and p.can_change_laser == True:
            w.type = "laser"
        # item spawning
        if keys[pygame.K_LCTRL]:
            if keys[pygame.K_1]:
                choise = random.choice(items_common)
                if p.check_item_in_items(choise.name) == False:
                    p.items.append(choise)
                else:
                    p.add_one_to_item_amount(f"{choise.name}")
            elif keys[pygame.K_2]:
                choise = random.choice(items_rare)
                if p.check_item_in_items(choise.name) == False:
                    p.items.append(choise)
                else:
                    p.add_one_to_item_amount(f"{choise.name}")
            elif keys[pygame.K_3]:
                choise = random.choice(items_epic)
                if p.check_item_in_items(choise.name) == False:
                    p.items.append(choise)
                else:
                    p.add_one_to_item_amount(f"{choise.name}")
            elif keys[pygame.K_4]:
                choise = random.choice(items_legendary)
                if p.check_item_in_items(choise.name) == False:
                    p.items.append(choise)
                else:
                    p.add_one_to_item_amount(f"{choise.name}")
            elif keys[pygame.K_s]:
                p.save_info()
                map.save_info()
                o.save_info()
                save_time(total_time,current_time)
                save_merchant_in_all_rooms(map)

        # boss enemy spawn
        if keys[pygame.K_8]:
            can_spawn = True
        if keys[pygame.K_9] and can_spawn == True:
            o.spawn_boss(screen,enemy_boss,map.stage,p)
            can_spawn = False

        if keys[pygame.K_ESCAPE] and len(o.enemies) <= 0:
            save_game(map, p, o, total_time)
            state = "menu"

        ###### DISPLAY
        pygame.font.init()
        number_font = pygame.font.SysFont('arial', 30)

        time_text = number_font.render("Total time: "+str(total_time), False, white)
        screen.blit(time_text, (screen_size[0] - screen.get_width()/6, screen.get_height()/30))

        current_time_text = number_font.render("Current time: "+str(current_time), False, white)
        screen.blit(current_time_text, (screen_size[0] - screen.get_width()/6, screen.get_height()/10))

        string_stage = str(map.stage)
        stage_text = number_font.render(string_stage, False, orange)
        screen.blit(stage_text, (screen.get_width()/25, screen.get_height()/30))

        player_hp_display = str(round(p.hp))+"/"+str(p.max_hp)
        health_display = number_font.render(player_hp_display, False, white)
        screen.blit(health_display, (healthbar.x, healthbar.y))

        scraps = scrap_amount(p)
        scrap_display = number_font.render(f"Scrap amount: {scraps}", False, white)
        screen.blit(scrap_display, (screen.get_width()*3/5, screen.get_height()/30))

        coins = number_font.render(f"Coins: {int(p.coins)}", False, yellow)
        screen.blit(coins, (screen.get_width()/6, screen.get_height()/30))

        create_display(screen, p)

        # MAP 
        if keys[pygame.K_m]:
            map.draw_map(screen)
        # ITEMS
        check_mouse_on_item_display(screen, p, room)
        check_mouse_on_item_room(screen, room)
  
        if keys[pygame.K_TAB]:
            display_item_and_description(screen,p,healthbar)

        if keys[pygame.K_F11] and screen_size[0] < user32.GetSystemMetrics(0) and can_change_display == True:
            screen_size = initial_width, initial_height = int(user32.GetSystemMetrics(0)), int(user32.GetSystemMetrics(1))
            screen = pygame.display.set_mode(screen_size)
            healthbar.x, healthbar.y,healthbar.width,healthbar.height = screen.get_width()/22, screen.get_height()*9/10, screen.get_width()*2/5, screen.get_height()/24
            can_change_display = False
        elif keys[pygame.K_F11] and screen_size[0] >= user32.GetSystemMetrics(0) and can_change_display == True:
            screen_size = initial_width, initial_height = int(user32.GetSystemMetrics(0)*3/4), int(user32.GetSystemMetrics(1)*3/4)
            screen = pygame.display.set_mode(screen_size)
            healthbar.x, healthbar.y,healthbar.width,healthbar.height = screen.get_width()/22, screen.get_height()*9/10, screen.get_width()*2/5, screen.get_height()/24
            can_change_display = False
    
        # ON QUITTING GAME
        for event in pygame.event.get():
            if event.type == pygame.QUIT and len(o.enemies) <= 0:
                state = "end"

        if state == "end":
            save_game(map, p, o, total_time)

        pygame.display.update()
    pygame.quit()

game = True

if __name__ == "__main__":
    while game == True:
        main()
