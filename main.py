import pygame
from pygame.locals import *
import pygame_gui
import math
import numpy
import random

# Define some colors
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255,255,0)
WHITE = (255, 255, 255)
BRIGHTORANGE = (255, 174, 0)
SILVER = (192,192,192)
GRAY = (128,128,128)
MAROON = (128,0,0)
PURPLE = (128,0,128)
CORN_FLOWER_BLUE = (100,149,237)

is_paused = False
# initialize variables

# used to identify where to go when previous screen button pressed
curr_screen = None
prev_screen = None

# pygame initialization
pygame.init()
clock = pygame.time.Clock()

# set window + dock icon
display_height = 800
display_width = 800
display_size = (display_width, display_height)
display = pygame.display.set_mode(display_size, 0, 32)
manager = pygame_gui.UIManager(display_size, 'themes/button_themes.json')
dock_icon = pygame.image.load('images/dock_icon.png')
pygame.display.set_icon(dock_icon)
pygame.display.set_caption("Fake Doodle Jump")

# set background
display.fill(GRAY)

# creates surface with same size as window - draw/create shapes on it
background = pygame.Surface(display_size)
display.blit(background, (0, 0))

pygame.display.update()

def quit_game():
	pygame.quit()
	quit()

def unpause():
	global is_paused
	is_paused = False

def pause():

	# LargeText = pygame.font.SysFont("Keyboard.ttf", 115)
	# TextSurf, TextRect = TextObjects("Paused", LargeText)
	# TextRect.center = ((display_width/2), (display_height/2))
	# GameDisplay.blit(TextSurf, TextRect)


	# while is_paused:
	# 	for event in pygame.event.get():
	# 		#print(event)
	# 		if event.type == pygame.QUIT:
	# 			pygame.quit()
	# 			quit()

	# 	#GameDisplay.fill(Blue)

	# 	Button("CONTINUE", 250, 450, 100, 50, Green, BrightGreen, unpause)
	# 	Button("RETURN", 450, 450, 100, 50, Orange, BrightOrange, game_introduction)
	# 	Button("QUIT", 650, 450, 100, 50, Red, BrightRed, quit_game)

	# 	pygame.display.update()
	# 	Clock.tick(15)

  pass


