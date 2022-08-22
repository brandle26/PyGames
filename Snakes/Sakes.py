import pygame
import random

#initialize pygame
pygame.init()

#set display
WINDOW_WIDTH=600
WINDOW_HEIGHT=600
display_surface=pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("~Snake~")

#Set FPS and clock
FPS=20
clock=pygame.time.Clock()

#Set game values
SNAKE_SIZE=20

head_x=WINDOW_WIDTH//2
head_y=WINDOW_HEIGHT//2 + 100

snake_dx=0
snake_dy=0

score=0

#Set colors
GREEN=(0,255,0)
DARKGREEN=(10,50,10)
RED=(255,0,0)
DARKRED=(150,0,0)
WHITE=(255,255,255)

#Set fonts
font=pygame.font.SysFont("gariola", 48)

#Set text
title_text=font.render("~~Snake~~", GREEN, DARKRED)
title_rect=title_text.get_rect()
title_rect.center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

score_text=font.render("Score: "+str(score), True, GREEN, DARKRED)
score_rect=score_text.get_rect()
score_rect.topleft=(10,10)

game_over_text=font.render("GAME OVER", True, RED, DARKGREEN)
game_over_rect=game_over_text.get_rect()
game_over_rect.center=(WINDOW_WIDTH//2,WINDOW_HEIGHT//2)

continue_text=font.render("Press any key to ply again", True, RED, DARKGREEN)
continue_rect=continue_text.get_rect()
continue_rect.center= (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 64)

#Set sounds and music
pick_up_sound=pygame.mixer.Sound("pick_up_sound.wav")

#Set images (in this case just use simple rets .... so just create their coordinates)
#for a rectangle you only need (top-left x, top-left y, width, height
apple_coord=(500,500,SNAKE_SIZE, SNAKE_SIZE)
apple_rect=pygame.draw.rect(display_surface, GREEN, apple_coord)

head_coord=(head_x,head_y, SNAKE_SIZE, SNAKE_SIZE)
head_rect=pygame.draw.rect(display_surface, RED, head_coord)

body_coords=[]

#maing game loop
running=True
while running:
    #Check to see if the user wants to quit
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running= False

    #move the snake
    if event.type==pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            snake_dx = -1*SNAKE_SIZE
            snake_dy=0
        if event.key == pygame.K_RIGHT:
            snake_dx=SNAKE_SIZE
            snake_dy=0
        if event.key == pygame.K_UP:
            snake_dx=0
            snake_dy=-1*SNAKE_SIZE
        if event.key==pygame.K_DOWN:
            snake_dx=0
            snake_dy=SNAKE_SIZE

    #Add the head coordinate to he first index of the body coordiate list
    #This will essentially move al the snake body by one position int he list
    body_coords.insert(0, head_coord)
    body_coords.pop()


    #update the (x,y) position of the snakehed and mak a new coordinate
    head_x+=snake_dx
    head_y+=snake_dy
    head_coord=(head_x,head_y,SNAKE_SIZE,SNAKE_SIZE)

    #check for game over
    if (head_rect.left <0) or (head_rect.right>WINDOW_WIDTH) or (head_rect.top <0) or (head_rect.bottom>WINDOW_HEIGHT) or (head_coord in body_coords):
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text,continue_rect)
        pygame.display.update()

        #pause the game until the playe presses akey, then reset the game
        is_pause=True
        while is_pause:
            for event in pygame.event.get():
                #the player wants to play again
                if event.type==pygame.KEYDOWN:
                    score=0

                    head_x=WINDOW_WIDTH//27
                    head_y=WINDOW_HEIGHT//2
                    head_coord=(head_x,head_y, SNAKE_SIZE, SNAKE_SIZE)

                    body_coords= []

                    snake_dx = 0
                    snake_dy = 0

                    is_pause=False

                if event.type==pygame.QUIT:
                    is_pause=False
                    running=False




    #check for collisions
    if head_rect.colliderect(apple_rect):
        score+=1
        pick_up_sound.play()

        apple_x=random.randint(0, WINDOW_WIDTH-SNAKE_SIZE)
        apple_y=random.randint(0, WINDOW_HEIGHT-SNAKE_SIZE)
        apple_coord=(apple_x,apple_y, SNAKE_SIZE, SNAKE_SIZE)

        body_coords.append(head_coord)

    #update HUD
    score_text=font.render("Score: "+str(score), True, GREEN, DARKRED)





    #fill the surface
    display_surface.fill(WHITE)

    #blit HUD
    display_surface.blit(title_text,title_rect)
    display_surface.blit(score_text,score_rect)

    #Blit assets
    for body in body_coords:
        pygame.draw.rect(display_surface, DARKGREEN, body)
    head_rect=pygame.draw.rect(display_surface, GREEN, head_coord)
    apple_rect=pygame.draw.rect(display_surface, RED, apple_coord)

    #Update display
    pygame.display.update()

    #set up fps or clock
    clock.tick(FPS)


#end the game
pygame.quit()