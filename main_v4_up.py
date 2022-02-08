# Import
import pygame
import my_module
import random
from my_module import PacMan
from os import path
import os

# Initialize the game engine
pygame.init()
# Define the colors we will use in RGB format
WHITE = (255, 255, 255)

numbers_bombs = 35

# Pacman parameters
x_position_pacman = 500
y_position_pacman = 900
step_pacman = 30

# Health
health = 3
health_position_x = 950
health_position_y = 25

# Set the height and width of the screen
H = 1000
W = 1000
size = [H, W]
# Creating screen with a given size
screen = pygame.display.set_mode(size)

# Set the caption display
pygame.display.set_caption("My PacMan")

win_image = pygame.image.load('images'+os.sep+'win_post.png')
win_image_position = win_image.get_rect(center=(500, 500))

health_image = pygame.image.load('images'+os.sep+'health.png')
health_image_position = health_image.get_rect(center=(health_position_x, health_position_y))

lose_image = pygame.image.load('images'+os.sep+'lose.png')
lose_image_position = lose_image.get_rect(center=(500, 500))

# Background music, load and play
pygame.mixer.music.load('sounds'+os.sep+'mortal_combat.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(1000)

# Sound boom
boom_dir = path.join(path.dirname(__file__))
booms_sound = pygame.mixer.Sound(path.join(boom_dir, 'sounds'+os.sep+'boom.wav'))
# Sound lose
lose_dir = path.join(path.dirname(__file__))
lose_sound = pygame.mixer.Sound(path.join(lose_dir, 'sounds'+os.sep+'lose_sound.wav'))
play_lose_sound = True
# Sound win
win_dir = path.join(path.dirname(__file__))
win_sound = pygame.mixer.Sound(path.join(win_dir, 'sounds'+os.sep+'win_sound.wav'))
play_win_sound = True

# Booms image
explosion_image = pygame.image.load('images'+os.sep+'explosion.png')

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()
#  Create PacMan
pac1 = PacMan('1', x_position_pacman, y_position_pacman, 'images'+os.sep+'PC.png', step_pacman)
#  Create bombs
list_bombs = my_module.set_bombs(numbers_bombs)

while not done:

    # This limits the wile loop to a max of 30 times per second
    # Leave this out, and we will use all CPU we can
    clock.tick(20)

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:  # That's all is script users do
            if event.key == pygame.K_UP:
                pac1.move_up()
            elif event.key == pygame.K_DOWN:
                pac1.move_down()
            elif event.key == pygame.K_LEFT:
                pac1.move_left()
            elif event.key == pygame.K_RIGHT:
                pac1.move_right()
            elif event.key == pygame.K_ESCAPE:  # Click ESC fo exit
                done = True
            elif event.key == pygame.K_r and health <= 0 or pac1.y_position < 100 and event.key == pygame.K_r:  # Script restart game
                health = 3
                pygame.mixer.music.load('sounds'+os.sep+'mortal_combat.mp3')
                pygame.mixer.music.set_volume(0.1)
                pygame.mixer.music.play(1000)
                pac1.x_position = x_position_pacman
                pac1.y_position = y_position_pacman
                for i in range(len(list_bombs)):
                    list_bombs[i].speed = 20
                pac1.speed = step_pacman
                play_lose_sound = True
                play_win_sound = True

    # All drawing code happens after the for loop and but
    # inside the main while done==False loop.

    # Clear the screen and set the screen background
    screen.fill(WHITE)

    # Print all bombs on screen
    for i in range(len(list_bombs)):
        list_bombs[i].print_it(screen)
    for i in range(len(list_bombs)):
        list_bombs[i].move()

    # Script win game
    if pac1.y_position < 100:
        screen.blit(win_image, win_image_position)
        pygame.mixer.music.stop()
        for i in range(len(list_bombs)):
            list_bombs[i].speed = 0
        pac1.speed = 0
        if play_win_sound:
            win_sound.play()
            play_win_sound = False

    if health > 0 and pac1.y_position >= 100:
        pac1.print_it(screen)

    # Script lose game
    if health <= 0:
        screen.blit(lose_image, lose_image_position)
        pygame.mixer.music.stop()
        for i in range(len(list_bombs)):
            list_bombs[i].speed = 0
        pac1.speed = 0
        if play_lose_sound:
            lose_sound.play()
            play_lose_sound = False

    # Script encounter PacMan with bomb
    # 30 - radius circle PacMan image
    # 20 - radius bombs image
    for i in range(len(list_bombs)):
        x = my_module.boom(pac1.x_position, pac1.y_position, 30, list_bombs[i].x_position, list_bombs[i].y_position, 20)
        if x:
            explosion_image_position = explosion_image.get_rect(
                center=(list_bombs[i].x_position, list_bombs[i].y_position))
            screen.blit(explosion_image, explosion_image_position)
            booms_sound.play(loops=0)
            list_bombs[i].x_position = random.randint(50, 900)
            list_bombs[i].y_position = random.randint(50, 900)
            health -= 1

    # Sorry for this, but I don't know how create while
    if health == 3:
        screen.blit(health_image, health_image.get_rect(center=(health_position_x, health_position_y)))
        screen.blit(health_image, health_image.get_rect(center=(health_position_x - 50, health_position_y)))
        screen.blit(health_image, health_image.get_rect(center=(health_position_x - 100, health_position_y)))

    if health == 2:
        screen.blit(health_image, health_image.get_rect(center=(health_position_x, health_position_y)))
        screen.blit(health_image, health_image.get_rect(center=(health_position_x - 50, health_position_y)))

    if health == 1:
        screen.blit(health_image, health_image.get_rect(center=(health_position_x, health_position_y)))
    # I'm really sorry

    # Update a screen after drawing, last command in while
    pygame.display.flip()
