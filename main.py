import math
import numpy
import pygame
from pygame.locals import *
import pygame_gui
import random
import sys

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
DARK_GREEN = (8, 76, 8)
DARK_BLUE = (29, 80, 255)

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
main_bg = pygame.image.load('images/bg_main.png')

pygame.display.set_caption("Fake Doodle Jump")
pygame.display.set_icon(dock_icon)

# set background
display.fill(GRAY)

# creates surface with same size as window - draw/create shapes on it
background = pygame.Surface(display_size)
display.blit(background, (0, 0))

pygame.display.update()

# quickly create objects (rects)
def text_objects(text, font, colour):

	text_surf = font.render(text, True, colour)
	return text_surf, text_surf.get_rect()

# basic game functions
def quit_game():
	pygame.quit()
	sys.exit()
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
	# 	Button("RETURN", 450, 450, 100, 50, Orange, BrightOrange, Introduction)
	# 	Button("QUIT", 650, 450, 100, 50, Red, BrightRed, quit_game)

	# 	pygame.display.update()
	# 	Clock.tick(15)

	pass

# go back to previous window/screen when p pressed on keyboard
def return_to_prev_screen(prev_screen, curr_screen):

	if prev_screen is None:
		return 'intro', prev_screen, curr_screen

	elif prev_screen == 'instructions':
		return 'instructions', prev_screen, curr_screen

	elif prev_screen == 'intro':
		return 'intro', prev_screen, curr_screen
	
	elif prev_screen == 'main':
		return 'main', prev_screen, curr_screen

	else:
		return 'intro', prev_screen, curr_screen

# run window/screen based on user's choices
def screen_to_run(wdw, prev_screen, curr_screen):

	if wdw is False:
		quit_game()

	elif wdw == 'intro':
		return Introduction(prev_screen, curr_screen).display_screen()

	elif wdw == 'instructions':
		return Instructions(prev_screen, curr_screen).display_screen()
	
	elif wdw == 'main':
		return Main(prev_screen, curr_screen).display_screen()

	elif wdw == 'return_to_prev_screen':
		return return_to_prev_screen(prev_screen, curr_screen)

	else:
		return Introduction(prev_screen, curr_screen).display_screen()

	return wdw, prev_screen, curr_screen

# parent class for all screens
class Screen:
	def __init__(self, prev_screen, curr_screen):

		self.prev_screen = prev_screen
		self.curr_screen = curr_screen

	def set_prev_curr_screen(self, curr):
		
		try:
			self.prev_screen = self.curr_screen

		except UnboundLocalError:
			self.prev_screen = 'intro'

		self.curr_screen = curr
	
	def clear_screen(self):

		# set window + clear screen
		self.manager = pygame_gui.UIManager(display_size, 'themes/button_themes.json')

	def draw_text(self, text, size, x, y):

			# title Fake Doodle Jump at top of the screen
			title_text_font = pygame.font.Font('fonts/Montserrat-Bold.ttf', size)
			text_surf, text_rect = text_objects(text, title_text_font, BLACK)
			text_rect.center = (x, y)
			display.blit(text_surf, text_rect)

	def clock_sync(self):

		# don't load faster than needed
		clock.tick(60) / 1000
		self.time_delta = clock.tick(60) / 1000

# screen game opens with
class Introduction(Screen):
	def create_buttons(self):

		# instructions button under title
		self.instructions_btn = pygame_gui.elements.UIButton(
		relative_rect = pygame.Rect((300, 200), (200, 100)),
		text = 'Instructions', manager = self.manager, object_id = '#instructions')

		# play game button
		self.play_game_btn = pygame_gui.elements.UIButton(
		relative_rect = pygame.Rect((100, 400), (200, 100)),
		text = 'Play Game', manager = self.manager, object_id = '#play_game')

		# quit button
		self.quit_btn = pygame_gui.elements.UIButton(
		relative_rect = pygame.Rect((500, 400), (200, 100)),
		text = 'Quit', manager = self.manager, object_id = '#quit')

	def display_screen(self):
		
		self.set_prev_curr_screen('intro')
		self.clear_screen()

		display.fill(GRAY)

		self.create_buttons()
		self.draw_text('FAKE DOODLE JUMP', 50, (display_width / 2), (display_height / 8))

		while True:

			self.clock_sync()

			for event in pygame.event.get():

				# red x on top left of every window = quit
				if event.type == pygame.QUIT:
					quit_game()

				if event.type == pygame.KEYDOWN:
					# press escape to quit
					if event.key == pygame.K_ESCAPE:
						quit_game()

					# press i to see instructions
					if event.key == pygame.K_i:
						# instructions(prev_screen, curr_screen)
						return 'instructions', self.prev_screen, self.curr_screen

					# press p to go to previous screen/window
					if event.key == pygame.K_BACKSPACE:
						return 'return_to_prev_screen', self.prev_screen, self.curr_screen

				if event.type == pygame.USEREVENT:
					# where to go when buttons clicked
					if event.user_type == pygame_gui.UI_BUTTON_PRESSED:

						if event.ui_element == self.instructions_btn:
							return 'instructions', self.prev_screen, self.curr_screen
						
						if event.ui_element == self.play_game_btn:
							return 'main', self.prev_screen, self.curr_screen

						if event.ui_element == self.quit_btn:
							quit_game()

				self.manager.process_events(event)
			self.manager.update(self.time_delta)

			# display.blit(background, (0, 0))
			self.manager.draw_ui(display)
			pygame.display.flip()

# screen with instruction
class Instructions(Screen):
	def display_screen(self):

		self.set_prev_curr_screen('instructions')
		self.clear_screen()

		display.fill(DARK_GREEN)

		while True:

			# don't load faster than needed
			clock.tick(60) / 1000
			time_delta = clock.tick(60) / 1000

			# red x on top left of every window = quit
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					quit_game()

				if event.type == pygame.KEYDOWN:

					# press escape to quit
					if event.key == pygame.K_ESCAPE:
						quit_game()

					# press p to go to previous screen/window
					if event.key == pygame.K_BACKSPACE:
						return 'return_to_prev_screen', self.prev_screen, self.curr_screen

					# press m to go the intro screen
					if event.key == pygame.K_m:
						return 'intro', self.prev_screen, self.curr_screen

				self.manager.process_events(event)
			self.manager.update(time_delta)

			# instructions' text
			text_line_font = pygame.font.Font('fonts/Montserrat-Regular.ttf', 25)
			text_line_0 = text_line_font.render('Controls:', 1, YELLOW)
			controls_text = ['- To quit, either click the red button at the top left, or press', '   esc on the keyboard.', '- To go back to the previous page you were on, press', '   backspace on the keyboard.', '- To open up this page again, press i on the keyboard.', '- To go back to the main page, press m on the keyboard.', '- To move the main sprite, use the arrow keys.', '- To pause the game, press p on the keyboard.', '- You can click on any buttons - buttons always light up when ', '   they are hovered over.']

			# display.blit(background, (0, 0))

			# put instructions on the screen
			display.blit(text_line_0, (5, (27 * 0)))

			for i in range(len(controls_text)):
				display.blit(text_line_font.render(controls_text[i], 1, WHITE), (5, (27 * (i + 1))))

			self.manager.draw_ui(display)
			pygame.display.flip()

# main gameplay screen
class Main(Screen):
	def display_screen(self):

		self.set_prev_curr_screen('main')
		self.clear_screen()

		display.blit(main_bg, (0, 0))

		while True:

			self.clock_sync()

			for event in pygame.event.get():

				# red x on top left of every window = quit
				if event.type == pygame.QUIT:
					quit_game()

				if event.type == pygame.KEYDOWN:
					# press escape to quit
					if event.key == pygame.K_ESCAPE:
						quit_game()

					# press i to see instructions
					if event.key == pygame.K_i:
						# instructions(prev_screen, curr_screen)
						return 'instructions', self.prev_screen, self.curr_screen

					# press p to go to previous screen/window
					if event.key == pygame.K_BACKSPACE:
						return 'return_to_prev_screen', self.prev_screen, self.curr_screen
					
					# press m to go the intro screen
					if event.key == pygame.K_m:
						return 'intro', self.prev_screen, self.curr_screen

				self.manager.process_events(event)
			self.manager.update(self.time_delta)

			# display.blit(background, (0, 0))
			self.manager.draw_ui(display)
			pygame.display.flip()


# used to choose which screen to run
user_wdw, user_prev, user_curr = True, prev_screen, curr_screen

# driver code
if __name__ == "__main__":

	# first initialization - start on intro page
	user_wdw, user_prev, user_curr = Introduction(user_prev, user_curr).display_screen()

	# choose which screen to run as long as not quitting
	while user_wdw is not False:
		user_wdw, user_prev, user_curr = screen_to_run(user_wdw, user_prev, user_curr)

# close everything
quit_game()
