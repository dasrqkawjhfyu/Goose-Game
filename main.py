import pygame, sys
pygame.init()

screen = pygame.display.set_mode((700, 560))
framerate = pygame.time.Clock()
game_run = True
click = False

def createFont(font, size):
    new_font = pygame.font.Font(font, size)
    return new_font

font = createFont('res/font/FiraSans-Bold.ttf', 16)

def createText(font, text, color, pos):
    new_text = font.render(text, True, color)
    new_text_rect = new_text.get_rect()
    new_text_rect.topleft = pos
    return new_text, new_text_rect

database = {}
database['rect'] = pygame.Rect(5, 560 - 76 + 5, 50 + 35, 76 - 10), pygame.Rect(100, 240, 80, 80)

walk_text, walk_text_rect = createText(font, 'walk', (255, 255, 255), (30, 560 - 48))
clicked_walk_text, clicked_walk_text_rect = createText(font, 'walk', (12, 175, 170), (30, 560 - 48))

global animation_frames
animation_frames = {}

def load_animation(path,frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        animation_image = pygame.image.load(img_loc).convert()
        animation_image.set_colorkey((0, 0, 0))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data

def change_action(action_var,frame,new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var,frame

animation_database = {}
animation_database['walk'] = load_animation('res/player/walk',[5, 5, 5, 5, 5, 5])
animation_database['idle'] = load_animation('res/player/idle',[200, 5, 5, 2000, 5, 5])
animation_database['coin'] = load_animation('res/coin', [8, 8, 8, 8])

player_action = 'idle'
player_frame = 0
player_flip = False
player_rect = pygame.Rect(200, 264, 88, 91  )

player_walk_right = False
player_walk_left = False
player_walk_up = False
player_walk_down = False
player_speed = 3

coin_frame = 0
coin_action = 'coin'
coins = [pygame.Rect(100, 130, 40, 40), pygame.Rect(500, 460, 40, 40)]
collect_coins = False

def clip(surf,x,y,x_size,y_size):
    handle_surf = surf.copy()
    clipR = pygame.Rect(x,y,x_size,y_size)
    handle_surf.set_clip(clipR)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()

class Font():
    def __init__(self, path):
        self.spacing = 1
        self.character_order = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','.','-',',',':','+','\'','!','?','0','1','2','3','4','5','6','7','8','9','(',')','/','_','=','\\','[',']','*','"','<','>',';']
        font_img = pygame.image.load(path).convert()
        font_img.set_colorkey((0, 0, 0))
        current_char_width = 0
        self.characters = {}
        character_count = 0
        for x in range(font_img.get_width()):
            c = font_img.get_at((x, 0))
            if c[0] == 127:
                char_img = clip(font_img, x - current_char_width, 0, current_char_width, font_img.get_height())
                self.characters[self.character_order[character_count]] = char_img.copy()
                character_count += 1
                current_char_width = 0
            else:
                current_char_width += 1
        self.space_width = self.characters['A'].get_width()

    def render(self, surf, text, loc, scale_x, scale_y):
        x_offset = 0
        for char in text:
            if char != ' ':
                surf.blit(pygame.transform.scale(self.characters[char], (self.characters[char].get_width() * scale_x, self.characters[char].get_height() * scale_y)), (loc[0] + x_offset, loc[1]))
                x_offset += self.characters[char].get_width() * scale_x + self.spacing
            else:
                x_offset += self.space_width + self.spacing * scale_x

font = Font('res/font/large_font.png')

while game_run:

    screen.fill((85, 124, 85))
    mx, my = pygame.mouse.get_pos()

    moving = False

    if player_walk_left == True:
        player_flip = True
        player_action,player_frame = change_action(player_action,player_frame,'walk')
        player_rect.x -= player_speed
        moving = True
    if player_walk_right == True:
        player_flip = False
        player_action,player_frame = change_action(player_action,player_frame,'walk')
        player_rect.x += player_speed
        moving = True
    if player_walk_up == True:
        player_action,player_frame = change_action(player_action,player_frame,'walk')
        player_rect.y -= player_speed
        moving = True
    if player_walk_down == True:
        player_action,player_frame = change_action(player_action,player_frame,'walk')
        player_rect.y += player_speed
        moving = True
    if player_walk_left == True and player_walk_up == True:
        player_speed = 2.5
    elif player_walk_left == True and player_walk_down == True:
        player_speed = 2.5
    elif player_walk_right == True and player_walk_up == True:
        player_speed = 2.5
    elif player_walk_right == True and player_walk_down == True:
        player_speed = 2.5
    else:
        player_speed = 3

    if moving == False:
        player_action,player_frame = change_action(player_action,player_frame,'idle')

    for coin in coins:
        if player_rect.colliderect(coin):
            coins.remove(coin)

    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_img_id = animation_database[player_action][player_frame]
    player_img = animation_frames[player_img_id]
    screen.blit(pygame.transform.scale(pygame.transform.flip(player_img,player_flip,False), (player_img.get_width() + 50, player_img.get_height() + 50  )), (player_rect.x + 10, player_rect.y + 10))

    coin_frame += 1
    if coin_frame >= len(animation_database[coin_action]):
        coin_frame = 0
    coin_img_id = animation_database[coin_action][coin_frame]
    coin_img = animation_frames[coin_img_id]

    for i in range(len(coins)):
        screen.blit(pygame.transform.scale(coin_img, (40, 40)), (coins[i].x, coins[i].y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_LEFT:
                player_walk_left = True
            if event.key == pygame.K_RIGHT:
                player_walk_right = True
            if event.key == pygame.K_UP:
                player_walk_up = True
            if event.key == pygame.K_DOWN:
                player_walk_down = True
            if event.key == pygame.K_e:
                collect_coins = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player_walk_right = False
            if event.key == pygame.K_LEFT:
                player_walk_left = False
            if event.key == pygame.K_UP:
                player_walk_up = False
            if event.key == pygame.K_DOWN:
                player_walk_down = False
            if event.key == pygame.K_e:
                collect_coins = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                click = False

    pygame.display.update()
    framerate.tick(60)
