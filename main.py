import pygame, sys
from pygame.locals import *
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
animation_database['idle'] = load_animation('res/player/idle',[80, 5, 5, 200, 5, 5])

player_action = 'idle'
player_frame = 0
player_flip = False

while game_run:

    screen.fill((168, 35, 76))
    mx, my = pygame.mouse.get_pos()

    text1, text_rect1 = createText(font, 'FPS: ' + str(int(framerate.get_fps())), (255, 255, 255), (2, 2))
    screen.blit(text1, text_rect1)

    # walk rect and text
    pygame.draw.rect(screen, (12, 175, 170), database['rect'][0])
    screen.blit(walk_text, walk_text_rect)
    if database['rect'][0].collidepoint(mx, my):
        if click == True:
            pygame.draw.rect(screen, (255, 255, 255), database['rect'][0])
            screen.blit(clicked_walk_text, clicked_walk_text_rect)
            player_action,player_frame = change_action(player_action,player_frame,'walk')
        else:
            player_action,player_frame = change_action(player_action,player_frame,'idle')

    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
    	player_frame = 0
    player_img_id = animation_database[player_action][player_frame]
    player_img = animation_frames[player_img_id]
    current_anim, current_anim_rect = createText(font, 'current animation: ' + str(player_action), (255, 255, 255), (95, 560 - 16 - 5))
    screen.blit(current_anim, current_anim_rect)
    screen.blit(pygame.transform.scale(pygame.transform.flip(player_img,player_flip,False), (player_img.get_width() + 50, player_img.get_height() + 50)),(700 / 2 - (player_img.get_width() / 2 + 25), 560 / 2 - (player_img.get_height() / 2 + 25)))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                click = False

    pygame.display.update()
    framerate.tick(60)
