import pygame
import random
import math
from pygame import mixer

pygame.init()

#score
score=0
font = pygame.font.Font("freesansbold.ttf", 32)
text_x=10
text_y=10
def show_score(x,y):
    score_1=font.render("score:" + str(score), True, "green")
    game_display.blit(score_1, (x,y))


#background music
mixer.music.load("background_m.mp3")
mixer.music.play(-1)
    
#game fornt 
game_font=pygame.font.Font("freesansbold.ttf", 80)

#game_display
size = [800, 800]
game_display = pygame.display.set_mode(size)

#game icon
icon=pygame.image.load("icon.png")
pygame.display.set_icon(icon)
#background 
background = pygame.image.load("background_3.jpg")

#game player
player=pygame.image.load("player.png")
player_x=400
player_y=660
player_change = 0

#game enemy
enemy=[]
enemy_x=[]
enemy_y=[]
enemy_x_change=[]
enemy_y_change=[]
number_of_enemy=7

for i in range(number_of_enemy):
    enemy.append(pygame.image.load("enemy.png"))
    enemy_x.append(random.randint(0, 760))
    enemy_y.append(random.randint(50, 200))
    enemy_x_change.append(1)
    enemy_y_change.append(20)


#game bullet
bullet = pygame.image.load("bullet.png")
bullet_x=0
bullet_y=660
bullet_x_change =0
bullet_y_change = 10
bullet_state="ready"

def game_over(x,y):
    game_over_text=game_font.render("GAME OVER", True, "red")
    game_display.blit(game_over_text, (x,y))

def player_1(x, y):
    game_display.blit(player, (x,y))
    
    
def enemy_1(x, y, i):
    game_display.blit(enemy[i], (x,y))


def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    game_display.blit(bullet, (x+16, y+10))

def iscollision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance=math.sqrt((math.pow(enemy_x-bullet_x, 2)) + (math.pow(enemy_y-bullet_y, 2)))
    if distance<27:
        return True
    else:
        return False

con = True
while con:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            con = False
            
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_RIGHT:
                player_change+=1
            if event.key==pygame.K_LEFT:
                player_change+=-1
            if event.key==pygame.K_SPACE:
                if bullet_state is "ready":
                     bullet_sound=mixer.Sound("shoot.wav")
                     bullet_sound.play()
                     bullet_x=player_x
                     fire_bullet(bullet_x, bullet_y)
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_RIGHT or event.key==pygame.K_LEFT:
                player_change=0
            
    game_display.blit(background, (0,0))
    
    
 #Enemy boundary and movement
    for i in range(number_of_enemy):
        #game_over
        if enemy_y[i]>600:
            for j in range(number_of_enemy):
                enemy_y[j]=2000
            game_over(140, 300)
            break
                
        enemy_x[i]+=enemy_x_change[i]
        if enemy_x[i]<0:
            enemy_x_change[i]=1
            enemy_y[i] += enemy_y_change[i]
        if enemy_x[i]>770:
            enemy_x_change[i]=-1
            enemy_y[i] += enemy_y_change[i]
            
            #collision
    
        collision=iscollision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            kill_sound=mixer.Sound("kill.wav")
            kill_sound.play()
            bullet_y =660
            bullet_state="ready"
            score+=1
            enemy_x[i]=random.randint(0, 760)
            enemy_y[i]=random.randint(50, 200)
            
        enemy_1(enemy_x[i], enemy_y[i], i)
    
    #player boundary
    player_x+=player_change
    if player_x<0:
        player_x=0
    if player_x>730:
        player_x=730
        
    #bullet movement
    
    #bullet replacement
    if bullet_y<0:
        bullet_y=660
        bullet_state="ready"
        
    #bullet fire
    if bullet_state in "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y-=bullet_y_change
        


    
    #calling function
    player_1(player_x, player_y)
    show_score(text_x, text_y)
    pygame.display.update()