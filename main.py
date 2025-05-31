import pygame
import random
from sys import exit
from pygame import mixer

#initialize modules
pygame.init()
all_scores=[]
screen=pygame.display.set_mode((1080,1920))
start_time=0
clock=pygame.time.Clock()
font=pygame.font.Font('Font3.ttf',140)
font1=pygame.font.Font('Font3.ttf',60)
power_up_available=False
game_active=True
selected_player_left=False
selected_player_right=True
jump_left=False
jump_right=True
jump_active=False
max_height=False
current_score=stopping_score=0
obstacle_timer=pygame.USEREVENT + 1
orb_timer=pygame.USEREVENT + 2
x=0
pygame.time.set_timer(obstacle_timer,1200)
pygame.time.set_timer(orb_timer,5000)

#loading the bg music
mixer.music.load('resources/music.mp3')
mixer.music.play(-1)

#score
def score(start_time):
    global game_active
    if game_active is False:return 0
    else:
        current_time=pygame.time.get_ticks()-start_time
        score=(current_time//100)
        score_surface=font.render(f'{score}',False,'White')
        score_rect=score_surface.get_rect(center=(655,95))
        screen.blit(score_surface,score_rect)
        return score
    
#animations
def player_right_animation():
    global player_right_surface,player_right_index
    player_right_index+=0.25
    if player_right_index>=len(player_right_frames):player_right_index=0
    player_right_surface=player_right_frames[int(player_right_index)]

def player_left_animation():
    global player_left_surface,player_left_index
    player_left_index+=0.25
    if player_left_index>=len(player_left_frames):player_left_index=0
    player_left_surface=player_left_frames[int(player_left_index)]

def jump_left_animation():
    global jump_left_surface,jump_left_index
    jump_left_index+=0.25
    if jump_left_index>=len(jump_left_frames):jump_left_index=0
    jump_left_surface=jump_left_frames[int(jump_left_index)]

def jump_right_animation():
    global jump_right_surface,jump_right_index
    jump_right_index+=0.25
    if jump_right_index>=len(jump_right_frames):jump_right_index=0
    jump_right_surface=jump_right_frames[int(jump_right_index)]

def obstacle_animation():
    global obs_surface,obs_index
    obs_index+=0.5
    if obs_index>=len(obs_frames):obs_index=0
    obs_surface=obs_frames[int(obs_index)]

def power_animation():
    global power_surface,power_index
    power_index+=0.5
    if power_index>=len(power_frames):power_index=0
    power_surface=power_frames[int(power_index)]

#bg image
bg=pygame.image.load("bg.jpg").convert_alpha()
bg_rect=bg.get_rect(center=(540,1100))

#game_over image
game_over_image=pygame.image.load("resources/game_over.png").convert_alpha()
game_over_rect=game_over_image.get_rect(center=(535,1200))

#player images
#right side animation :
player_right_0=pygame.image.load("player/right/frame_0.png").convert_alpha()
player_right_1=pygame.image.load("player/right/frame_1.png").convert_alpha()
player_right_2=pygame.image.load("player/right/frame_2.png").convert_alpha()
player_right_3=pygame.image.load("player/right/frame_3.png").convert_alpha()
player_right_4=pygame.image.load("player/right/frame_4.png").convert_alpha()
player_right_5=pygame.image.load("player/right/frame_5.png").convert_alpha()
player_right_frames=[player_right_0,player_right_1,player_right_2,player_right_3,player_right_4,player_right_5]
player_right_index=0
player_right_surface=player_right_frames[player_right_index]
player_right_rect=player_right_surface.get_rect(center=(930,1300))

#left side animation :
player_left_0=pygame.image.load("player/left/frame_0.png").convert_alpha()
player_left_1=pygame.image.load("player/left/frame_1.png").convert_alpha()
player_left_2=pygame.image.load("player/left/frame_2.png").convert_alpha()
player_left_3=pygame.image.load("player/left/frame_3.png").convert_alpha()
player_left_4=pygame.image.load("player/left/frame_4.png").convert_alpha()
player_left_5=pygame.image.load("player/left/frame_5.png").convert_alpha()
player_left_frames=[player_left_0,player_left_1,player_left_2,player_left_3,player_left_4,player_left_5]
player_left_index=0
player_left_surface=player_left_frames[player_left_index]
player_left_rect=player_left_surface.get_rect(center=(145,1300))

#jump left animation :
jump_0=pygame.image.load("player/jump/frame_0.gif").convert_alpha()
jump_1=pygame.image.load("player/jump/frame_1.gif").convert_alpha()
jump_2=pygame.image.load("player/jump/frame_2.gif").convert_alpha()
jump_3=pygame.image.load("player/jump/frame_3.gif").convert_alpha()
jump_left_frames=[jump_0,jump_1,jump_2,jump_3]
jump_left_index=0
jump_left_surface=jump_left_frames[jump_left_index]
jump_left_rect=jump_left_surface.get_rect(center=(145,1300))

#jump right animation :
jump_0r=pygame.image.load("player/jump_right/frame_0.png").convert_alpha()
jump_1r=pygame.image.load("player/jump_right/frame_1.png").convert_alpha()
jump_2r=pygame.image.load("player/jump_right/frame_2.png").convert_alpha()
jump_3r=pygame.image.load("player/jump_right/frame_3.png").convert_alpha()
jump_right_frames=[jump_0r,jump_1r,jump_2r,jump_3r]
jump_right_index=0
jump_right_surface=jump_right_frames[jump_right_index]
jump_right_rect=jump_right_surface.get_rect(center=(930,1300))

#obstacles
obs_0=pygame.image.load('obs/0.gif').convert_alpha()
obs_1=pygame.image.load('obs/1.gif').convert_alpha()
obs_2=pygame.image.load('obs/2.gif').convert_alpha()
obs_3=pygame.image.load('obs/3.gif').convert_alpha()
obs_4=pygame.image.load('obs/4.gif').convert_alpha()
obs_5=pygame.image.load('obs/5.gif').convert_alpha()
obs_frames=[obs_0,obs_1,obs_2,obs_3,obs_4,obs_5]
obs_index=0
obs_surface=obs_frames[obs_index]
obs_rect=obs_surface.get_rect(center=(950,200))
obs_rect2=obs_surface.get_rect(center=(100,-350))
obstacle_rect_list=[] 

#score image
score_img = pygame.image.load('resources/score.png').convert_alpha()
score_img_rect=score_img.get_rect(center=(480,80))

#rasengan images
power_1=pygame.image.load('power/1.gif').convert_alpha()
power_2=pygame.image.load('power/2.gif').convert_alpha()
power_3=pygame.image.load('power/3.gif').convert_alpha()
power_4=pygame.image.load('power/4.gif').convert_alpha()
power_5=pygame.image.load('power/5.gif').convert_alpha()
power_6=pygame.image.load('power/6.gif').convert_alpha()
power_7=pygame.image.load('power/7.gif').convert_alpha()
power_8=pygame.image.load('power/8.gif').convert_alpha()
power_9=pygame.image.load('power/9.gif').convert_alpha()
power_10=pygame.image.load('power/10.gif').convert_alpha()
power_11=pygame.image.load('power/11.gif').convert_alpha()
power_12=pygame.image.load('power/12.gif').convert_alpha()
power_13=pygame.image.load('power/13.gif').convert_alpha()
power_frames=[power_1,power_2,power_3,power_4,power_5,power_6,power_7,power_8,power_9,power_10,power_11,power_12,power_13]
power_index=0
power_surface=power_frames[power_index]
power_rect=power_surface.get_rect(center=(550,1900))
abilities_used=[]

#button
button_surface=pygame.image.load('resources/button.png').convert_alpha()
button_rect=button_surface.get_rect(center=(530,2000))

#orb
orb_surface=pygame.image.load('resources/orb.png').convert_alpha()
orbs=[]
meter=[]
temp=[]

#game loop
while True:
    #check for exit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        #restarting game
        if game_active is False:
            if event.type==pygame.MOUSEBUTTONDOWN:
                start_time=pygame.time.get_ticks()
                abilities_used=[]
                obstacle_rect_list=[]
                orbs=[]
                meter=[]
                mouse_x,mouse_y=pygame.mouse.get_pos()
                if mouse_x in range(300,460) and mouse_y in range(1300,1450):game_active=True
                if mouse_x in range(600,750) and mouse_y in range(1300,1450):
                    pygame.quit()
                    quit()
        #checking for orb
        if event.type==orb_timer and power_up_available is False:
            orbs.append(orb_surface.get_rect(center=(540,random.randint(-300,-200))))
        #checking for jump
        if event.type == pygame.MOUSEBUTTONDOWN and game_active is True and button_rect.collidepoint(pygame.mouse.get_pos()) is False:
            jump_active=True
        #checking for power used
        if event.type == pygame.MOUSEBUTTONDOWN and jump_active is False and game_active is True and button_rect.collidepoint(pygame.mouse.get_pos()) is True:
            if selected_player_right:
                abilities_used.append(power_surface.get_rect(center=(940,1050)))
            else:
                abilities_used.append(power_surface.get_rect(center=(100,1050)))
        if event.type == obstacle_timer:
            if random.randint(0,1):obstacle_rect_list.append(obs_surface.get_rect(center=(950,random.randint(-200,100))))
            else:obstacle_rect_list.append(obs_surface.get_rect(center=(100,random.randint(-200,100))))
    #display bg
    screen.blit(bg, bg_rect)
    #jump mechanism
    if game_active is True:
        if jump_active is True:
            if jump_right is True:
                selected_player_right=False
                jump_right_animation()
                screen.blit(jump_right_surface,jump_right_rect)
                jump_right_rect.x-=10
                if max_height is False:jump_right_rect.y-=5
                if jump_right_rect.y==1000:max_height=True
                if max_height is True:jump_right_rect.y+=5
                if jump_right_rect.x<=70 and jump_right_rect.y>=1000:
                    jump_active=False
                    jump_right_rect.x=805
                    jump_right_rect.y=1175
                    max_height=False
                    selected_player_left=True
                    jump_left,jump_right=jump_right,jump_left
        if jump_active is True:          
            if jump_left is True:
                selected_player_left=False
                jump_left_animation()
                screen.blit(jump_left_surface,jump_left_rect)
                jump_left_rect.x+=10
                if max_height is False:jump_left_rect.y-=5
                if jump_left_rect.y==1000:max_height=True
                if max_height is True:jump_left_rect.y+=5
                if jump_left_rect.x>=800 and jump_left_rect.y>=1000:
                    jump_active=False
                    jump_left_rect.x=20
                    jump_left_rect.y=1175
                    max_height=False
                    selected_player_right=True
                    jump_left,jump_right=jump_right,jump_left
                    
        if selected_player_right is True:
            player_right_animation()
            screen.blit(player_right_surface,player_right_rect)
        if selected_player_left is True:
            player_left_animation()
            screen.blit(player_left_surface,player_left_rect) 
        
        #displaying obstacles
        obstacle_animation()
        for obstacle in obstacle_rect_list:
            obstacle.y+=10
            screen.blit(obs_surface,obstacle)
        
        #collision detection
        for obstacle in obstacle_rect_list:
            if selected_player_left is True:
                if obstacle.collidepoint(player_left_rect.centerx,player_left_rect.centery):
                    game_active=False
            if selected_player_right is True:
                if obstacle.collidepoint(player_right_rect.centerx,player_right_rect.centery):
                    game_active=False

        #orb mechanism
        for orb in orbs:
            orb.y+=10
            screen.blit(orb_surface,orb)
        
        #orb storing
        for orb in orbs:
            if orb.colliderect(jump_left_rect) or orb.colliderect(jump_right_rect):
                orb.x=-9000
                meter.append(1)

        #score mechanism
        screen.blit(score_img,score_img_rect)
        score(start_time)  
        s=score(start_time)
        if s not in all_scores:all_scores.append(s)
        high_score=max(all_scores)
        high_score_surf=font1.render(f'{high_score}',False,'#afdecc')
        high_score_rect=high_score_surf.get_rect(center=(380,970))
        
        #rasengan mechanism
        if len(meter)>=3:
            power_up_available=True
            if s not in temp:temp.append(s)
        if len(temp)>150:
            meter=[]
            temp=[]
            power_up_available=False

       
        if power_up_available:
            screen.blit(button_surface,button_rect)
            power_animation()
            for ability in abilities_used:
                ability.y-=10
                screen.blit(power_surface,ability)
            #collision detection with shurikens
            for ability in abilities_used:
                for obstacle in obstacle_rect_list:
                    if ability.collidepoint(obstacle.centerx,obstacle.centery):
                        obstacle.x=9000
                        obstacle.y=9000 
    #checking for gameover
    if game_active is False:
        screen.blit(game_over_image,game_over_rect)
        screen.blit(high_score_surf,high_score_rect)
    # updating the display
    pygame.display.update()
    clock.tick(90)
        
