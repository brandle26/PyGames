from typing import Union

import pygame
import random

# initialize pygame
from pygame.surface import Surface, SurfaceType

pygame.init()

# set up display surface
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
display_surface: Union[Surface, SurfaceType] = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Monster Wrangler")

# set FPS and clock
FPS = 60
clock = pygame.time.Clock()


# Define Classes
class Game():
    """A class to control gameplay"""

    def __init__(self, my_player, my_monster_group):
        """Initialize the game object"""
        self.score = 0
        self.round_number = 0

        self.round_time = 0
        self.frame_count = 0

        self.player = my_player
        self.monster_group = my_monster_group

        # set sounds and music
        self.next_level_sound = pygame.mixer.Sound(r"resources\next_level.wav")

        # set font
        self.font = pygame.font.Font(r"resources\Abrushow.ttf", 24)

        # set images
        blue_image = pygame.image.load(r"resources\blue_monster.png")
        green_image = pygame.image.load(r"resources\green_monster.png")
        purple_image = pygame.image.load(r"resources\purple_monster.png")
        yellow_image = pygame.image.load(r"resources\yellow_monster.png")
        self.target_monster_images = [blue_image, green_image, purple_image, yellow_image]

        self.target_monster_type = random.randint(0, 3)
        self.target_monster_image = self.target_monster_images[self.target_monster_type]

        self.target_monster_rect = self.target_monster_image.get_rect()
        self.target_monster_rect.centerx = WINDOW_WIDTH // 2
        self.target_monster_rect.top = 30

    def update(self):
        """update or game object"""
        self.frame_count += 1
        if self.frame_count == FPS:
            self.round_time += 1
            self.frame_count = 0

        # check for collision
        self.check_collisions()
        self.draw()

    def draw(self):
        """Draw the HUD and other to the diplay"""
        # set colors
        WHITE = (255, 255, 255)
        BLUE = (20, 176, 235)
        GREEN = (87, 201, 47)
        PURPLE = (226, 73, 243)
        YELLOW = (243, 157, 20)

        # Add the monster colors to a list wher the index of the color matches target_monster_images
        colors = [BLUE, GREEN, PURPLE, YELLOW]

        # set text
        catch_text =self.font.render("Current Catch", True, WHITE)
        catch_rect = catch_text.get_rect()
        catch_rect.centerx = WINDOW_WIDTH // 2
        catch_rect.top = 5

        score_text = self.font.render("Score: " + str(self.score), True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.topleft = (5, 5)

        lives_text = self.font.render("Lives: " + str(self.player.lives), True, WHITE)
        lives_rect = lives_text.get_rect()
        lives_rect.topleft = (5, 35)

        round_text = self.font.render("Current Round: " + str(self.round_number), True, WHITE)
        round_rect = round_text.get_rect()
        round_rect.topleft = (5, 65)

        time_text = self.font.render("Round TIme: " + str(self.round_time), True, WHITE)
        time_rect = time_text.get_rect()
        time_rect.topright = (WINDOW_WIDTH - 10, 5)

        warp_text = self.font.render("Warps: " + str(self.player.warps), True, WHITE)
        warp_rect = warp_text.get_rect()
        warp_rect.topright = (WINDOW_WIDTH - 10, 35)

        #blit the HUD
        display_surface.blit(catch_text,catch_rect)
        display_surface.blit(score_text,score_rect)
        display_surface.blit(round_text, round_rect)
        display_surface.blit(lives_text,lives_rect)
        display_surface.blit(time_text,time_rect)
        display_surface.blit(warp_text,warp_rect)
        display_surface.blit(self.target_monster_image, self.target_monster_rect)

        pygame.draw.rect(display_surface, colors[self.target_monster_type], (WINDOW_WIDTH//2 - 32, 30, 64, 64), 2)
        pygame.draw.rect(display_surface, colors[self.target_monster_type],(0,100, WINDOW_WIDTH, WINDOW_HEIGHT-200),4)



    def check_collisions(self):
        """Check for collisions between player and monsters"""
        #check for collision between and an individual monster
        #we must test the type of the monster to see if it matches the type of our target monster
        collided_monster = pygame.sprite.spritecollideany(self.player, self.monster_group)

        #we collided with a monster
        if collided_monster:
            #Caught the correct monster
            if collided_monster.type == self.target_monster_type:
                self.score += 100*self.round_number
                #remove caught monster
                collided_monster.remove(self.monster_group)
                if (self.monster_group):
                    #There are more monster to catch
                    self.player.catch_sound.play()
                    self.choose_new_target()
                else:
                    #the round is complete
                    self.player.reset()
                    self.start_new_round()
            #caught the wrong monster
            else:
                self.player.die_sound.play()
                self.player.lives -= 1
                #check for game over
                if self.player.lives <= 0:
                    self.pause_game("Final Score: "+ str(self.score),"Press Enter to play again")
                    self.reset_game()
                self.player.reset()


    def start_new_round(self):
        """Populate board with new monster"""
        #provide a score bonus based on how quickly the round was finished
        self.score += int(10000* self.round_number/(1 + self.round_time))

        #resset round values
        self.round_time = 0
        self.frame_count = 0
        self.round_number += 1
        self.player.warps += 1

        #remove any remaning monster form a game reset
        for monster in self.monster_group:
            self.monster_group.remove(monster)

        #add monster to the monster group
        for i in range(self.round_number):
            self.monster_group.add(Monster(random.randint(0, WINDOW_WIDTH - 64), random.randint(100, WINDOW_HEIGHT- 164), self.target_monster_images[0],0))
            self.monster_group.add(Monster(random.randint(0, WINDOW_WIDTH - 64), random.randint(100, WINDOW_HEIGHT- 164), self.target_monster_images[1],1))
            self.monster_group.add(Monster(random.randint(0, WINDOW_WIDTH - 64), random.randint(100, WINDOW_HEIGHT- 164), self.target_monster_images[2],2))
            self.monster_group.add(Monster(random.randint(0, WINDOW_WIDTH - 64), random.randint(100, WINDOW_HEIGHT- 164), self.target_monster_images[3],3))


        #choose a new target monster
        self.choose_new_target()

        self.next_level_sound.play()



    def choose_new_target(self):
        """Choose a new target monster for the player"""
        target_monster = random.choice(self.monster_group.sprites())
        self.target_monster_type = target_monster.type
        self.target_monster_image= target_monster.image

    def pause_game(self, main_text, sub_text):
        """Pause the game"""
        global running

        #Set color
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)

        #create the main pause text
        main_text = self.font.render(main_text, True, WHITE)
        main_rect = main_text.get_rect()
        main_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

        #create the wub pause text
        sub_text = self.font.render(sub_text, True, WHITE)
        sub_rect = sub_text.get_rect()
        sub_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 64)

        #display the pause text
        display_surface.fill(BLACK)
        display_surface.blit(main_text, main_rect)
        display_surface.blit(sub_text, sub_rect)
        pygame.display.update()

        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_paused = False
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False



    def reset_game(self):
        """Reset the game"""
        self.scorea = 0
        self.round_number = 0

        self.player.lives = 5
        self.player.warps = 2
        self.player.reset()

        self.start_new_round()


class Player(pygame.sprite.Sprite):
    """A player class that the user can control"""

    def __init__(self):
        """"initialize the player"""
        super().__init__()
        self.image = pygame.image.load(r"resources\knight.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT

        self.lives = 5
        self.warps = 2
        self.velocity = 8

        self.catch_sound = pygame.mixer.Sound(r"resources\catch.wav")
        self.die_sound = pygame.mixer.Sound(r"resources\die.wav")
        self.warp_sound = pygame.mixer.Sound(r"resources\warp.wav")

    def update(self):
        """Update the player"""
        keys = pygame.key.get_pressed()

        # move the player within the bound of the screen
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.velocity
        if keys[pygame.K_UP] and self.rect.top > 100:
            self.rect.y -= self.velocity
        if keys[pygame.K_DOWN] and self.rect.bottom < WINDOW_HEIGHT - 100:
            self.rect.y += self.velocity

    def warp(self):
        """Warp the player to the bottom safe zone"""
        if self.warps > 0:
            self.warps -= 1
            self.warp_sound.play()
            self.rect.bottom = WINDOW_HEIGHT

    def reset(self):
        """Resets the player's position"""
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT


class Monster(pygame.sprite.Sprite):
    """A class to create enemy objects"""

    def __init__(self, x, y, image, monster_type):
        """Initialize the monster """
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Monster type is an int 0 -> blue, 1 -> green, 2 -> purple, 3 -> yellow
        self.type = monster_type

        # Set random motion
        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])
        self.velocity = random.randint(1, 5)

    def update(self):
        """Update the monster"""
        self.rect.x += self.dx * self.velocity
        self.rect.y += self.dy * self.velocity

        # bounce the monster off the display
        if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
            self.dx = -1 * self.dx
        if self.rect.top <= 100 or self.rect.bottom >= WINDOW_HEIGHT - 100:
            self.dy = -1 * self.dy


# create a Player group and Player object
my_player_group = pygame.sprite.Group()
my_player = Player()
my_player_group.add(my_player)

# create a monster group
my_monster_group = pygame.sprite.Group()


# Create a game object
my_game = Game(my_player, my_monster_group)
my_game.pause_game("Monster Wrangler ", "Press 'Enter' to begin")
my_game.start_new_round()

# main game loop
running = True
while running:
    # check if user wants to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #player wants to warp
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_player.warp()

    # Fill the dislay
    display_surface.fill((0, 0, 0))

    # update and draw sprite groups
    my_player_group.update()
    my_player_group.draw(display_surface)

    my_monster_group.update()
    my_monster_group.draw(display_surface)

    # Update and draw the game
    my_game.update()
    my_game.draw()

    # Update display and clock
    pygame.display.update()
    clock.tick(FPS)

# end game
pygame.quit()
