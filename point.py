import pygame
import random
import time
import os 
from os import listdir
from os.path import isfile, join 

# Setting window sizes and character speed

window_x = 720
window_y = 480
character_speed = 15

# Set vars to colors
violet = pygame.Color(238, 130, 238, 255)
purple = pygame.Color (160, 32, 240, 255)
white = pygame.Color (255, 255, 255)
black = pygame.Color(0, 0, 0)
red = pygame.Color (255, 0, 0)
blue = pygame.Color (0, 0, 255)
green = pygame.Color (0, 255, 0)

pygame.init()

# Set main window
main_game_window = pygame.display.set_mode((window_x, window_y))
pygame.display.set_caption('Simple Pygame Game')
# Game clock
fps = pygame.time.Clock()

# Initialize character's position (x, y)
character_position = [100, 50]

# Set function to load sprites
def load_sprites(dir1, dir2, width, height, direction = False):
    
    def flip (sprites):
        return [pygame.transform.flip(sprite, True, False) for sprite in sprites] # Flipping image.

    path = join ("assets", dir1, dir2) # Set path for file
    images_available = [f for f in listdir(path) if isfile (join(path, f))] # loads all files that are inside that directory.

    all_available_sprites = {} # Dictionary Key is animation style and val is all the images in animation.

    for image in images_available:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = [] # List
        # Get individual pictures
        for i in range (sprite_sheet.get_width()//width): 
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32) # SRCALPHA allows transparent background
            rect = pygame.Rect(i * width, 0, width, height) # Rect(i * width) is the location in our acatual image where we want to grab the frame from. Then 0, then width and height of my image.
            surface.blit(sprite_sheet, (0,0), rect) # Draw my sprite_sheet at (0,0) and only draw the portion that is my rectangle.
            sprites.append(pygame.transform.scale2x(surface))
        if direction: 
            all_available_sprites [image.replace(".png", "") + "_right"] = sprites
            all_available_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_available_sprites [image.replace(".png", "")] = sprites
    
    return all_available_sprites

# Load background image
background_image = pygame.image.load('pond.png')
scaled_background_image = pygame.transform.scale(background_image, (window_x // 1, window_y // 1)) # Making image smaller

# Set character image
character_image = load_sprites("MainCharacters", "NinjaFrog", 32, 32, True)
character_current_image = character_image["idle_right"][0]

# Set insect 
insect_image = load_sprites("Menu", "Levels", 32, 32, True)
insect_current_image = insect_image ["myflyidle_right"][0]

# scaled_insect_image = pygame.transform.scale(insect_current_image, (16, 10))

# Set fruits position
insect_position = [random.randrange(1,(window_x // 10)) * 10, random.randrange(1, (window_y // 10) * 10 )]
insect_spawn = True

# Set direction to right to ensure program runs to the right of the screen 
direction = 'RIGHT'
change_to = direction

# Keeping score
score = 0 

def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    # Create display surface object
    score_surface = score_font.render ('Score : ' + str (score), True, color)
    # Rectangular object for the text surface
    score_rect = score_surface.get_rect()
    # Display the text 
    main_game_window.blit(score_surface, score_rect)

# Create game over function

def game_over():
    # Create font object
    my_font = pygame.font.SysFont("times new roman", 50)
    # Create text surface where text is drawn
    game_over_surface = my_font.render("Player's score is : " + str (score), True, violet)
    # Create rectangular object for the text surface object. 
    game_over_rect = game_over_surface.get_rect()
    # Set location for the text
    game_over_rect.midtop = (window_x / 2 , window_y / 4)
    # Draw text on screen
    main_game_window.blit(game_over_surface, game_over_rect)
    #
    pygame.display.flip() 
    # Quit program after 3 seconds
    time.sleep(3)
    pygame.quit()
    quit()
    
def main_function():
    global direction, change_to, insect_position, insect_spawn, score, character_position
    
    while True:
        # Keys
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = "UP"
                if event.key == pygame.K_DOWN:
                    change_to = "DOWN"
                if event.key == pygame.K_LEFT:
                    change_to = "LEFT"
                if event.key == pygame.K_RIGHT:
                    change_to = "RIGHT"
                        
        # Do not allow two keys being pressed simultaneously    
        if change_to == "UP" and direction != "DOWN":
            direction = "UP"
        if change_to == "DOWN" and direction != "UP":
            direction = "DOWN"
        if change_to == "LEFT" and direction != "RIGHT":
            direction = "LEFT"
        if change_to == "RIGHT" and direction != "LEFT":
            direction = "RIGHT"
            
        # Move the character
        if direction == "UP":
            character_position[1] -= 10
        if direction == "DOWN":
            character_position[1] += 10
        if direction == "LEFT":
            character_position[0] -= 10
        if direction == "RIGHT":
            character_position [0] += 10
                
        # Get points by eating insects
        character_rect = pygame.Rect(character_position[0], character_position[1], 64, 64)  # Adjust size based on your character's size
        insect_rect = pygame.Rect(insect_position[0], insect_position[1], 64, 64)

        if character_rect.colliderect(insect_rect):
            score += 10
            insect_spawn = False
        else:
            insect_spawn = True
                
        if not insect_spawn:
            insect_position = [random.randrange(1, (window_x // 10)) * 10, random.randrange(1,(window_x // 10)) * 10]
        
        insect_spawn = True
        
        main_game_window.fill(black)
        
        # Background
        main_game_window.blit(scaled_background_image, (0,0))
        
        # Show character on screen 
        main_game_window.blit(character_current_image, (character_position[0], character_position[1]))
        
        # pygame.draw.rect(main_game_window, purple, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))
        
        main_game_window.blit(insect_current_image, (insect_position[0], insect_position[1]))
           
            # Check for collisions 
        if character_position [0] < 0 or character_position [0] > window_x - 10:
            game_over()
        if character_position [1] < 0 or character_position[1] > window_y - 10:
            game_over()
                
            # Show score
        show_score (1, violet, "times new roman", 20)
            # Refresh
        pygame.display.update()
        fps.tick(character_speed)
        
if __name__ == "__main__":
    main_function()
    
            